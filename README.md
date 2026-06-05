# show-me

A skill for turning **code** and **changes** into a single self-contained HTML page that
a human can read to *get it fast* — the big picture of a system, or the **before → after
core difference** of a change — with every claim grounded to the actual code, one click away.

Prose is slow and raw diffs are noise. A carefully drawn, code-grounded picture is fast.
`show-me` is the methodology for producing that picture.

## What it does

It's a **progressive-disclosure** skill: [`SKILL.md`](SKILL.md) is an **index** that routes
to the right visualization dimension, and the dimension references say what to put in the
page. The shared craft (look, hand-drawn SVG, before/after technique, code grounding,
serving) lives in one place.

| Dimension | When | Output |
|---|---|---|
| **[Understand a new repo](references/repo-explainer.md)** | First time in a codebase — don't know what it is or how it works | Comprehensive report: mental model → architecture → flows → components, grounded to files |
| **[Understand a change](references/pr-explainer.md)** | Already know the repo; a PR / diff / branch needs explaining | Change report: big-picture impact + **before/after** diagrams of the affected logic, diffs collapsed, grounded to code |

Shared craft: **[references/html-craft.md](references/html-craft.md)**.

## The form

- **One self-contained HTML file** — no build, opens by double-click, survives copy to another machine.
- **Editorial document**, light theme: readable width, numbered sticky table of contents, sections, callouts — read top to bottom, not a dashboard of widgets.
- **Hand-drawn inline SVG** for the diagrams that carry the argument — you control layout, so before/after stays aligned and the *delta* is unmistakable (dashed-gray = before/context, solid-accent = after, orange = the change). Mermaid only for quick auxiliary graphs.
- **Grounded to code** — every box names a real symbol + `path:line` and links back to the source (GitHub blob at a pinned SHA, or local file). Picture → code in one click.
- **Served for cross-machine viewing** — handed back as a LAN / tunnel IP URL.

## Principles

1. Big picture first; depth on demand (collapsed / linked).
2. Show the *difference*, not just the after-state.
3. Ground everything to real code.
4. Hand-draw the diagrams that carry the argument.
5. Self-contained & offline.
6. Editorial, not dashboard.

## Install (as a Claude Code skill)

Place this repo's contents under a skills directory the agent discovers, e.g.:

```bash
git clone https://github.com/xingyaoww/show-me ~/.claude/skills/show-me
```

Then ask the agent: **"show me this repo"**, **"show me what this PR changes (before vs after)"**,
or **"visualize how this works"**.

## License

MIT
