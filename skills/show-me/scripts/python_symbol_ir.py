#!/usr/bin/env python3
"""Build a Python symbol IR for show-me semantic PR reports.

This is intentionally a small stdlib-only helper. It extracts enough structure to
make omissions visible: changed Python files, classes, functions, methods,
branches, call edges, and a coverage gate for generated HTML/Markdown reports.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Branch:
    kind: str
    condition: str
    line: int


@dataclass(frozen=True)
class Symbol:
    id: str
    path: str
    kind: str
    name: str
    qualname: str
    line: int
    end_line: int
    parent: str | None
    status: str
    signature: dict[str, Any]
    docstring: str | None
    decorators: list[str] = field(default_factory=list)
    branches: list[Branch] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    called_by: list[str] = field(default_factory=list)
    body_shape: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class FileIR:
    path: str
    old_path: str | None
    status: str
    imports: list[dict[str, Any]]
    symbols: list[str]


def run_git(repo: Path, args: list[str], *, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.strip() or "git command failed")
    return proc.stdout


def changed_python_files(repo: Path, base: str, head: str, diff_operator: str) -> list[dict[str, str | None]]:
    sep = "..." if diff_operator == "three-dot" else ".."
    out = run_git(repo, ["diff", "--name-status", f"{base}{sep}{head}", "--", "*.py"])
    files: list[dict[str, str | None]] = []
    for line in out.splitlines():
        parts = line.split("\t")
        if not parts:
            continue
        code = parts[0]
        status = code[0]
        if status == "R" and len(parts) >= 3:
            files.append({"status": "renamed", "old_path": parts[1], "path": parts[2]})
        elif status == "A" and len(parts) >= 2:
            files.append({"status": "added", "old_path": None, "path": parts[1]})
        elif status == "D" and len(parts) >= 2:
            files.append({"status": "deleted", "old_path": parts[1], "path": parts[1]})
        elif status in {"M", "C"} and len(parts) >= 2:
            files.append({"status": "modified", "old_path": parts[1], "path": parts[1]})
    return files


def show_file(repo: Path, ref: str, path: str | None) -> str | None:
    if not path:
        return None
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else None


def source_segment(source: str, node: ast.AST) -> str:
    segment = ast.get_source_segment(source, node)
    if segment is None:
        return ast.unparse(node) if hasattr(ast, "unparse") else type(node).__name__
    return " ".join(segment.strip().split())


def call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return call_name(node.func)
    return None


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    args = []
    for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]:
        item = {"name": arg.arg}
        if arg.annotation is not None:
            item["annotation"] = ast.unparse(arg.annotation)
        args.append(item)
    if node.args.vararg:
        args.append({"name": "*" + node.args.vararg.arg})
    if node.args.kwarg:
        args.append({"name": "**" + node.args.kwarg.arg})
    return {
        "inputs": args,
        "returns": ast.unparse(node.returns) if node.returns is not None else None,
        "async": isinstance(node, ast.AsyncFunctionDef),
    }


def class_signature(node: ast.ClassDef) -> dict[str, Any]:
    return {"bases": [ast.unparse(base) for base in node.bases]}


NESTED_SYMBOL_TYPES = (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)


def walk_symbol_body(node: ast.AST):
    stack = list(ast.iter_child_nodes(node))
    while stack:
        child = stack.pop()
        if isinstance(child, NESTED_SYMBOL_TYPES):
            continue
        yield child
        stack.extend(ast.iter_child_nodes(child))


def branch_nodes(node: ast.AST, source: str) -> list[Branch]:
    branches: list[Branch] = []
    for child in walk_symbol_body(node):
        line = getattr(child, "lineno", None)
        if line is None:
            continue
        if isinstance(child, ast.If):
            branches.append(Branch("if", source_segment(source, child.test), line))
        elif isinstance(child, (ast.For, ast.AsyncFor)):
            condition = f"{source_segment(source, child.target)} in {source_segment(source, child.iter)}"
            branches.append(Branch("for", condition, line))
        elif isinstance(child, ast.While):
            branches.append(Branch("while", source_segment(source, child.test), line))
        elif isinstance(child, ast.Try):
            handlers = [source_segment(source, h.type) for h in child.handlers if h.type is not None]
            branches.append(Branch("try", ", ".join(handlers) or "except", line))
        elif isinstance(child, ast.Match):
            branches.append(Branch("match", source_segment(source, child.subject), line))
    return branches


def call_nodes(node: ast.AST) -> list[str]:
    calls = []
    for child in walk_symbol_body(node):
        if isinstance(child, ast.Call):
            name = call_name(child.func)
            if name:
                calls.append(name)
    return sorted(set(calls))


def decorators(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> list[str]:
    return [ast.unparse(item) for item in node.decorator_list]


def body_shape(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> list[str]:
    shape = []
    for stmt in node.body:
        if isinstance(stmt, ast.Expr) and isinstance(getattr(stmt, "value", None), ast.Constant):
            if isinstance(stmt.value.value, str):
                continue
        shape.append(type(stmt).__name__)
    return shape


def symbol_source(source: str, node: ast.AST) -> str:
    lines = source.splitlines()
    start = max(1, getattr(node, "lineno", 1))
    end = getattr(node, "end_lineno", start)
    return "\n".join(lines[start - 1:end])


def collect_symbols(path: str, source: str) -> dict[str, dict[str, Any]]:
    tree = ast.parse(source)
    symbols: dict[str, dict[str, Any]] = {}

    def visit_body(body: list[ast.stmt], parents: list[str]) -> None:
        for node in body:
            if isinstance(node, ast.ClassDef):
                qualname = ".".join([*parents, node.name])
                item = {
                    "node": node,
                    "path": path,
                    "kind": "class",
                    "name": node.name,
                    "qualname": qualname,
                    "parent": ".".join(parents) if parents else None,
                    "signature": class_signature(node),
                    "docstring": ast.get_docstring(node),
                    "decorators": decorators(node),
                    "branches": branch_nodes(node, source),
                    "calls": call_nodes(node),
                    "body_shape": body_shape(node),
                    "source": symbol_source(source, node),
                }
                symbols[qualname] = item
                visit_body(node.body, [*parents, node.name])
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qualname = ".".join([*parents, node.name])
                item = {
                    "node": node,
                    "path": path,
                    "kind": "function" if not parents else "method",
                    "name": node.name,
                    "qualname": qualname,
                    "parent": ".".join(parents) if parents else None,
                    "signature": function_signature(node),
                    "docstring": ast.get_docstring(node),
                    "decorators": decorators(node),
                    "branches": branch_nodes(node, source),
                    "calls": call_nodes(node),
                    "body_shape": body_shape(node),
                    "source": symbol_source(source, node),
                }
                symbols[qualname] = item
                visit_body(node.body, [*parents, node.name])

    visit_body(tree.body, [])
    return symbols


def collect_imports(source: str) -> list[dict[str, Any]]:
    tree = ast.parse(source)
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.append({
                "line": node.lineno,
                "module": None,
                "names": [alias.name for alias in node.names],
            })
        elif isinstance(node, ast.ImportFrom):
            imports.append({
                "line": node.lineno,
                "module": "." * node.level + (node.module or ""),
                "names": [alias.name for alias in node.names],
            })
    return imports


def status_for(qualname: str, head_item: dict[str, Any] | None, base_item: dict[str, Any] | None) -> str:
    if head_item is None:
        return "deleted"
    if base_item is None:
        return "added"
    return "unchanged" if head_item["source"] == base_item["source"] else "modified"


def relation_target(call: str, symbols_by_short_name: dict[str, list[str]]) -> str:
    candidates = symbols_by_short_name.get(call.rsplit(".", 1)[-1], [])
    if len(candidates) == 1:
        return candidates[0]
    for candidate in candidates:
        if candidate.endswith(f"::{call}") or candidate.endswith(f".{call}"):
            return candidate
    return f"unresolved::{call}"


def build_ir(repo: Path, base: str, head: str, diff_operator: str) -> dict[str, Any]:
    changed = changed_python_files(repo, base, head, diff_operator)
    files: list[FileIR] = []
    symbols: dict[str, Symbol] = {}
    raw_calls: dict[str, list[str]] = {}

    for file_info in changed:
        path = str(file_info["path"])
        old_path = file_info["old_path"]
        status = str(file_info["status"])
        base_source = show_file(repo, base, old_path or path)
        head_source = None if status == "deleted" else show_file(repo, head, path)
        base_symbols = collect_symbols(str(old_path or path), base_source) if base_source else {}
        head_symbols = collect_symbols(path, head_source) if head_source else {}
        imports = collect_imports(head_source or base_source or "")
        file_symbol_ids = []
        for qualname in sorted(set(base_symbols) | set(head_symbols)):
            head_item = head_symbols.get(qualname)
            base_item = base_symbols.get(qualname)
            item = head_item or base_item
            if item is None:
                continue
            node = item["node"]
            item_path = item["path"]
            symbol_id = f"{item_path}::{qualname}"
            symbol_status = status_for(qualname, head_item, base_item)
            symbol = Symbol(
                id=symbol_id,
                path=item_path,
                kind=item["kind"],
                name=item["name"],
                qualname=qualname,
                line=getattr(node, "lineno", 1),
                end_line=getattr(node, "end_lineno", getattr(node, "lineno", 1)),
                parent=item["parent"],
                status=symbol_status,
                signature=item["signature"],
                docstring=item["docstring"],
                decorators=item["decorators"],
                branches=item["branches"],
                calls=item["calls"],
                body_shape=item["body_shape"],
            )
            symbols[symbol_id] = symbol
            raw_calls[symbol_id] = item["calls"]
            file_symbol_ids.append(symbol_id)
        files.append(FileIR(path=path, old_path=old_path, status=status, imports=imports, symbols=file_symbol_ids))

    short_names: dict[str, list[str]] = {}
    for symbol_id, symbol in symbols.items():
        if symbol.status == "deleted":
            continue
        short_names.setdefault(symbol.name, []).append(symbol_id)

    relations = []
    called_by: dict[str, set[str]] = {symbol_id: set() for symbol_id in symbols}
    for source_id, calls in raw_calls.items():
        for call in calls:
            target_id = relation_target(call, short_names)
            relations.append({"kind": "calls", "from": source_id, "to": target_id})
            if target_id in called_by:
                called_by[target_id].add(source_id)

    for file_ir in files:
        for symbol_id in file_ir.symbols:
            relations.append({"kind": "contains", "from": file_ir.path, "to": symbol_id})
        for item in file_ir.imports:
            target = item["module"] or ",".join(item["names"])
            relations.append({"kind": "imports", "from": file_ir.path, "to": target, "line": item["line"]})

    symbol_rows = []
    for symbol_id in sorted(symbols):
        symbol = symbols[symbol_id]
        row = asdict(symbol)
        row["called_by"] = sorted(called_by.get(symbol_id, set()))
        row["location"] = f"{symbol.path}:{symbol.line}"
        symbol_rows.append(row)

    required = [row["id"] for row in symbol_rows if row["status"] != "deleted"]
    return {
        "schema_version": "show-me.semantic-pr-ir.v0",
        "repo": {
            "root": str(repo),
            "base": base,
            "head": head,
            "diff_operator": diff_operator,
        },
        "files": [asdict(file_ir) for file_ir in files],
        "symbols": symbol_rows,
        "relations": relations,
        "coverage": {"required_symbol_ids": required},
    }


def write_ir(ir: dict[str, Any], output: Path | None) -> None:
    data = json.dumps(ir, indent=2, sort_keys=True) + "\n"
    if output:
        output.write_text(data)
    else:
        print(data, end="")


def check_coverage(ir: dict[str, Any], artifact: Path, mode: str) -> int:
    text = artifact.read_text(errors="replace")
    missing = []
    for symbol in ir["symbols"]:
        if symbol["status"] == "deleted":
            continue
        needles = [symbol["id"]] if mode == "id" else [symbol["id"], symbol["qualname"], symbol["name"]]
        if not any(needle in text for needle in needles):
            missing.append(symbol["id"])
    if missing:
        print("Missing symbols from report:", file=sys.stderr)
        for symbol_id in missing:
            print(f"  - {symbol_id}", file=sys.stderr)
        return 1
    print(f"Coverage OK: {len(ir['coverage']['required_symbol_ids'])} symbols found in {artifact}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True, help="PR base ref or commit")
    parser.add_argument("--head", default="HEAD", help="PR head ref or commit")
    parser.add_argument("--diff-operator", choices=["three-dot", "two-dot"], default="three-dot")
    parser.add_argument("--output", type=Path, help="Write semantic IR JSON here")
    parser.add_argument("--check-coverage", type=Path, help="HTML/Markdown report that must mention every symbol")
    parser.add_argument(
        "--coverage-mode",
        choices=["id", "name"],
        default="id",
        help="id requires stable symbol ids; name also accepts qualname/name mentions",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo = args.repo.resolve()
    ir = build_ir(repo, args.base, args.head, args.diff_operator)
    if args.output:
        write_ir(ir, args.output)
    elif not args.check_coverage:
        write_ir(ir, None)
    if args.check_coverage:
        return check_coverage(ir, args.check_coverage, args.coverage_mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
