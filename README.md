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

## Install

`show-me` is a single skill: a `SKILL.md` (the index/router) plus a `references/` folder.
Both Claude Code and Codex discover skills by directory — installing is just cloning this
repo into the agent's skills directory under the name `show-me`.

### Claude Code

User-level (available in every session):

```bash
git clone https://github.com/xingyaoww/show-me ~/.claude/skills/show-me
```

Project-level (only in one repo, and shareable with the team via git):

```bash
git clone https://github.com/xingyaoww/show-me .claude/skills/show-me
```

Start (or `/reload`) Claude Code and the `show-me` skill is picked up automatically from
its `SKILL.md` frontmatter — no config to edit.

### Codex

User-level:

```bash
git clone https://github.com/xingyaoww/show-me ~/.codex/skills/show-me
```

Project-level:

```bash
git clone https://github.com/xingyaoww/show-me .codex/skills/show-me
```

Codex loads skills from its skills directory on session start; the cloned `SKILL.md`
becomes available the same way.

### Update / uninstall

```bash
git -C ~/.claude/skills/show-me pull      # update (swap path for your install)
rm -rf ~/.claude/skills/show-me           # uninstall
```

> Tip: to keep one clone and share it across both agents, clone once and symlink:
> `ln -s ~/.claude/skills/show-me ~/.codex/skills/show-me`.

## Use

Once installed, just ask in natural language — the agent routes via `SKILL.md`:

- **"show me this repo"** / "help me understand this codebase" → new-repo report
- **"show me what this PR changes — before vs after"** / "visualize this diff" → change report
- **"visualize how X works"** → targeted diagram, grounded to code

The agent generates a self-contained HTML page and serves it back at a LAN / tunnel URL.

## License

MIT
