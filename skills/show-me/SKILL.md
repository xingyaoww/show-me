---
name: show-me
description: >
  Visualize a codebase or a change as a single self-contained HTML page so a human
  grasps the big picture fast — and, when something changed, sees the before/after
  core difference clearly, grounded to the actual code. Not limited to PRs. Use when
  the user says "show me", "visualize this", "help me understand this repo / this PR",
  "draw the architecture", "what changed and how", "I don't want to read the code,
  just show me", or asks for a diagram / walkthrough / presentation of code.
---

# show-me — visualize code & changes for humans

When a human needs to *understand* code — a whole repo, a system, or a change — prose
and raw diffs are slow. A well-drawn picture grounded to the code is fast. This skill
is the methodology for producing that picture: a **single self-contained HTML page**
that conveys the **big picture** and, when relevant, the **before → after core
difference**, with every claim **clickable back to the real code**.

This file is an **index**. Read the dimension that matches the task, then read
[`references/html-craft.md`](references/html-craft.md) for how to actually build the page.

## Pick the dimension

| Situation | Read | Produces |
|---|---|---|
| **New repo / system** — first time seeing it, don't know what it does or how it works | [`references/repo-explainer.md`](references/repo-explainer.md) | A comprehensive HTML report: what it is, the mental model, architecture, data/control flow, key components — enough to orient before touching code |
| **A change** — already understand the repo; a PR / diff / branch / uncommitted edit needs explaining | [`references/pr-explainer.md`](references/pr-explainer.md) | A change report: big-picture impact + **before/after** diagrams of the affected logic, diffs collapsed, grounded to code |

Both share the same craft (look, self-containment, before/after technique, code
grounding, serving) — that lives in [`references/html-craft.md`](references/html-craft.md).

## Non-negotiable principles (all dimensions)

1. **Big picture first.** Lead with the one-paragraph mental model and a top-level
   diagram. Detail comes after, and only on demand (collapsed / linked).
2. **Show the difference, not just the after.** Whenever something changed, draw
   **before** and **after** side by side and make the *delta* visually loud (color +
   line style). The point is the core difference, not a redraw of the end state.
3. **Ground everything to code.** Every box, node, and claim names a real
   symbol + `path:line` and, when possible, is a clickable link back to the source
   (GitHub blob URL or local file). The human must be able to drop from picture to code
   in one click.
4. **Hand-draw the important diagrams.** For the diagrams that carry the argument,
   prefer **bespoke inline SVG** — you control layout, and before/after stays aligned
   and legible. Mermaid is fine for quick/auxiliary graphs, but auto-layout fights you
   on careful comparisons.
5. **Self-contained & offline.** One HTML file. No build. Inline CSS/SVG; CDN only if
   unavoidable. It must open by double-click and survive being copied to another machine.
6. **Editorial, not dashboard.** Calm document aesthetic (see craft ref): readable
   width, numbered sticky table of contents, sections, callouts — a thing a person
   reads top to bottom, not a wall of widgets.
7. **Serve it for cross-machine viewing.** People often look from a different machine —
   after generating, serve over `python3 -m http.server` and hand back a LAN / tunnel
   IP URL, not just `localhost`.

## Anti-patterns

- ❌ Dumping the raw diff / file tree and calling it "visualized" — adds nothing over the host.
- ❌ Empty nodes ("process data", "handle request") — every node is a real symbol + location.
- ❌ Only the after-state when something changed — the user wants the *contrast*.
- ❌ A build step, a framework, or a dozen CDN scripts — keep it one openable file.
- ❌ Pretty but ungrounded — if a box doesn't map to code, cut it or label it as a concept.
