# semantic-pr-explainer - turn a PR into reverse-spec code

**Situation:** the reader wants to understand an entire PR at the function/class level,
not just a summary of the diff. Produce a self-contained HTML report whose primary
artifact is a **Semantic PR IR**: a structured, natural-language-adjacent description of
every changed file's classes and functions, their relationships, branches, inputs,
outputs, and before/after behavior.

This is the "reverse spec" mode of show-me:

```text
PR diff -> symbol manifest -> Semantic PR IR -> coverage-checked HTML
```

Build per [`html-craft.md`](html-craft.md). This file is *what to extract, how to
represent it, and how to prove nothing was skipped*.

## When to use this instead of `pr-explainer`

Use this mode when the user asks for any of:

- "visualize the whole PR architecture"
- "show every function/class"
- "translate this PR into structured natural-language code"
- "make sure no function or class is omitted"
- "reverse-spec this change"
- "help me review the PR by understanding the structure first"

Use [`pr-explainer.md`](pr-explainer.md) for a concise, human-authored summary of the
main delta. Use this file when **symbol-level completeness** is the product.

## Semantic PR IR

The IR is a small structured language. It is intentionally closer to code than prose:
every node maps to a real symbol, every edge maps to a real relation, and every claim
has source evidence.

Top-level shape:

```yaml
schema_version: show-me.semantic-pr-ir.v0
repo:
  root: /path/to/repo
  base: <base sha or ref>
  head: <head sha or ref>
files:
  - path: code_review_agent/agentic/environment.py
    status: modified
    role: Runtime environment for one or more agentic review episodes.
    imports:
      - module: code_review_agent.agentic.runner
        names: [run_code_review_agent, AgenticRunError]
    symbols:
      - code_review_agent/agentic/environment.py::run_episode
symbols:
  - id: code_review_agent/agentic/environment.py::run_episode
    kind: function
    name: run_episode
    qualname: run_episode
    location: code_review_agent/agentic/environment.py:215
    signature:
      inputs: [task, llm, config, policy]
      returns: AgenticReviewEpisode
    role: Runs one review episode and persists raw runtime artifacts.
    calls:
      - code_review_agent/agentic/runner.py::run_code_review_agent
      - code_review_agent/agentic/environment.py::write_episode_events
    called_by:
      - code_review_agent/agentic/environment.py::run_batch
    branches:
      - condition: config.dry_run
        effect: Writes an empty raw event list and returns dry_run status.
        evidence: code_review_agent/agentic/environment.py:270
    change:
      status: modified
      before: Derived comments, ctx_comments, score, and breakdown in the runtime.
      after: Persists raw events and leaves scoring to downstream processing.
      evidence:
        - code_review_agent/agentic/environment.py:286
relations:
  - kind: calls
    from: code_review_agent/agentic/environment.py::run_episode
    to: code_review_agent/agentic/runner.py::run_code_review_agent
    evidence: code_review_agent/agentic/environment.py:278
coverage:
  required_symbol_ids:
    - code_review_agent/agentic/environment.py::run_episode
```

### Primitives

Use this vocabulary consistently:

| Primitive | Meaning | Required fields |
|---|---|---|
| `File` | A changed source file. | `path`, `status`, `role`, `symbols`, `imports` |
| `Class` | A class definition. | `id`, `name`, `qualname`, `location`, `bases`, `methods`, `change` |
| `Function` | A function or method. | `id`, `name`, `qualname`, `location`, `signature`, `calls`, `branches`, `change` |
| `Branch` | A control-flow decision inside a function/method. | `kind`, `condition`, `effect`, `evidence` |
| `Relation` | A typed edge between files or symbols. | `kind`, `from`, `to`, `evidence` |
| `Change` | The before/after semantic delta for a symbol. | `status`, `before`, `after`, `evidence` |
| `Evidence` | A source location proving a claim. | `path:line`, or a pinned blob URL |

Allowed relation kinds:

- `contains`: file -> class/function, class -> method
- `imports`: file -> module/symbol
- `calls`: function/method -> function/method or unresolved call name
- `instantiates`: function/method -> class
- `reads`: symbol -> file/config/env/store
- `writes`: symbol -> file/config/env/store
- `raises`: symbol -> exception
- `persists`: symbol -> durable artifact path

If a relation cannot be resolved, keep it explicit:

```yaml
relations:
  - kind: calls
    from: pkg/a.py::run
    to: unresolved::client.submit
    evidence: pkg/a.py:42
```

Do not invent a target just to make the graph prettier.

## Symbol Coverage Rule

Semantic PR reports must pass a coverage gate.

1. Build a symbol manifest for every changed source file.
2. Include every class, function, and method in the manifest.
3. Every symbol must appear in the HTML as a card, table row, or graph node.
4. Every HTML symbol instance must carry the stable `symbol.id`, preferably as
   `data-symbol-id="path.py::qualname"` and visibly as `path.py::qualname`.
5. Every symbol must link to source evidence.
6. Deleted symbols must appear in a "removed symbols" section unless the user asks to
   hide deletions.
7. If a symbol is intentionally excluded, add an explicit exclusion table with reason and
   evidence. Do not silently omit it.

Run the coverage helper when available:

```bash
python skills/show-me/scripts/python_symbol_ir.py \
  --base origin/main \
  --head HEAD \
  --output semantic-ir.json

python skills/show-me/scripts/python_symbol_ir.py \
  --base origin/main \
  --head HEAD \
  --check-coverage pr-semantic.html
```

The helper is a Python-first MVP. For non-Python files, create the same IR manually and
state that parser coverage is manual.

## Function/Class Card Format

Each symbol card should be short and regular enough to skim like code:

```html
<article class="symbol-card" data-symbol-id="pkg/review.py::ReviewRunner.run">
  <h3>ReviewRunner.run <a class="src" href="...">pkg/review.py:88</a></h3>
  <p><strong>Role.</strong> Runs one review pass and returns raw SDK events.</p>
  <table>
    <tr><th>Inputs</th><td>task, llm, config</td></tr>
    <tr><th>Output</th><td>AgenticRunResult</td></tr>
    <tr><th>Calls</th><td>prepare_workspace, run_code_review_agent, write_events</td></tr>
    <tr><th>Called by</th><td>run_batch</td></tr>
    <tr><th>Side effects</th><td>writes events JSON</td></tr>
  </table>
  <h4>Branches</h4>
  <ol>
    <li><code>config.dry_run</code> -> persist empty event list and skip LLM.</li>
    <li><code>AgenticRunError</code> -> persist partial trace and return error status.</li>
  </ol>
  <h4>Before -> After</h4>
  <p>Before: derived scoring fields inside the runtime. After: stores raw events only.</p>
</article>
```

Keep cards dense. This is a code review surface, not marketing copy.

## Report Sections

1. **Semantic Delta First** - one paragraph explaining the architectural move, backed by
   the top changed symbols and source links.
2. **Coverage Matrix** - every changed file and every symbol. Columns:
   `symbol id`, `kind`, `status`, `role`, `calls`, `called by`, `branches`, `covered`.
3. **Architecture Before/After** - an overview SVG where nodes are real files/classes/
   functions and edges are `Relation.kind`. Changed nodes/edges are orange.
4. **File Relationship Graph** - file-level import/call/persist edges. Back it with an
   edge table: `from -> to · kind · evidence`.
5. **Symbol Cards** - one card per function/class/method, ordered by file and source line.
6. **Removed Symbols** - deleted classes/functions/methods and what replaces them, if known.
7. **Unresolved Relations** - unresolved calls/imports with source evidence. This is a
   useful limitation, not a failure, as long as it is explicit.
8. **Raw Diff** - collapsed, for verification only.

## Visual Encoding

- File nodes: rectangles grouped by directory/module.
- Class nodes: rectangles nested inside file bands.
- Function/method nodes: compact pills/cards inside their owning file/class.
- `contains`: thin gray edge or nesting.
- `calls`: solid accent edge.
- `imports`: blue edge.
- `persists`/`writes`: green dashed edge to an artifact/store node.
- `raises`: red/orange dashed edge to an exception node.
- Added symbols: solid accent.
- Removed symbols: dashed red/gray, in a removed section.
- Modified symbols: orange border or stripe.
- Unchanged symbols in changed files: muted, but still present for coverage.

Avoid one giant graph if the PR touches many symbols. Use a small overview plus the
coverage matrix and per-file symbol cards.

## Reverse-Spec Discipline

- The IR is descriptive, not aspirational. It says what the code does now and what changed.
- Use code-derived facts first. LLM-written role/behavior summaries must be grounded to
  AST facts, source links, or diff evidence.
- Prefer `unknown` / `unresolved` over guessing.
- Keep abstraction close to code. This is "structured natural-language code", not a PRD.
- A symbol with no card is a bug in the visualization.
- A card with no source link is not grounded; cut it or fix it.

## Validation

At minimum:

```bash
python skills/show-me/scripts/python_symbol_ir.py --base <base> --head <head> --output semantic-ir.json
python skills/show-me/scripts/python_symbol_ir.py --base <base> --head <head> --check-coverage <html>
```

Also run normal repo tests when the PR changes behavior. The semantic report explains the
change; it does not replace correctness checks.
