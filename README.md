# show-me

A skill for turning **code** and **changes** into a single self-contained HTML page that
a human can read to *get it fast* — the big picture of a system, the **before → after
core difference** of a change, or the exact trace of a tricky mechanism — with every claim
grounded to the actual code, one click away.

Prose is slow and raw diffs are noise. A carefully drawn, code-grounded picture is fast.
`show-me` is the methodology for producing that picture. The guiding constraint is human
attention: spend extra agent effort so the result is skimmable, verifiable, and easy to act on.

## What it does

It's a **progressive-disclosure** skill: [`SKILL.md`](skills/show-me/SKILL.md) is an **index** that routes
to the right visualization dimension, and the dimension references say what to put in the
page. The shared craft (look, hand-drawn SVG, before/after technique, code grounding,
serving) lives in one place.

| Dimension | When | Output |
|---|---|---|
| **[Understand a new repo](skills/show-me/references/repo-explainer.md)** | First time in a codebase — don't know what it is or how it works | Comprehensive report: mental model → architecture → flows → components, grounded to files |
| **[Understand a mechanism](skills/show-me/references/mechanism-explainer.md)** | One pipeline, parser, resolver, scheduler, state machine, ranking rule, or other branchy logic is confusing | Focused walkthrough: boundary → rules → worked trace → non-examples → validation |
| **[Understand a change](skills/show-me/references/pr-explainer.md)** | Already know the repo; a PR / diff / branch needs explaining | Change report: big-picture impact + **before/after** diagrams of the affected logic, diffs collapsed, grounded to code |

Shared craft: **[references/html-craft.md](skills/show-me/references/html-craft.md)**.

## The form

- **One self-contained HTML file** — no build, opens by double-click, survives copy to another machine.
- **Skimmable first screen** — conclusion, mental model, where to jump, and evidence are visible before the reader commits to a full read.
- **Editorial document**, light theme: readable width, numbered sticky table of contents, sections, callouts — read top to bottom, not a dashboard of widgets.
- **Hand-drawn inline SVG** for the diagrams that carry the argument — you control layout, so before/after stays aligned and the *delta* is unmistakable (dashed-gray = before/context, solid-accent = after, orange = the change). Mermaid only for quick auxiliary graphs.
- **Grounded to code** — every box names a real symbol + `path:line` and links back to the source (GitHub blob at a pinned SHA, or local file). Evidence sits beside the claim it proves. Picture → code in one click.
- **Served for cross-machine viewing** — preferably an `htmlpreview.github.io` link to
  a pushed self-contained page, with LAN / tunnel HTTP as the local fallback.

## Principles

1. Optimize for scarce human attention: skimmable, verifiable, decision-first.
2. Big picture first; depth on demand (collapsed / linked).
3. Show the *difference*, not just the after-state.
4. Ground every claim to real code, adjacent to the claim.
5. Hand-draw the diagrams that carry the argument.
6. Self-contained & offline.
7. Editorial, not dashboard.

## Install

This repo is **both a Claude Code plugin marketplace and the plugin itself** (the
`.claude-plugin/` manifests at the root). Pick the path for your agent.

### Claude Code — via the `/plugin` UI (recommended)

No clone, no paths to wire. In a Claude Code session:

```text
/plugin marketplace add xingyaoww/show-me
/plugin install show-me@show-me
```

`/plugin` opens the UI to browse/enable it; `show-me@show-me` is `<plugin>@<marketplace>`
(both named `show-me`). Update later with `/plugin marketplace update show-me`. Same
commands work from the CLI as `claude plugin marketplace add xingyaoww/show-me` etc.

### Codex — clone into the skills directory

Codex has no plugin marketplace, so install the skill by directory. The skill lives at
`skills/show-me/` in this repo:

```bash
git clone https://github.com/xingyaoww/show-me /tmp/show-me \
  && cp -r /tmp/show-me/skills/show-me ~/.codex/skills/show-me
# update: re-run; uninstall: rm -rf ~/.codex/skills/show-me
```

(Project-level: copy into `.codex/skills/show-me` inside your repo instead.)

### Claude Code without the marketplace (manual skill)

If you'd rather drop the raw skill in (no plugin):

```bash
git clone https://github.com/xingyaoww/show-me /tmp/show-me \
  && cp -r /tmp/show-me/skills/show-me ~/.claude/skills/show-me
```

## Use

Once installed, just ask in natural language — the agent routes via `SKILL.md`:

- **"show me this repo"** / "help me understand this codebase" → new-repo report
- **"show me what this PR changes — before vs after"** / "visualize this diff" → change report
- **"visualize how X works"** → targeted diagram, grounded to code

The agent generates a self-contained HTML page and hands back a clickable link — ideally a
`htmlpreview.github.io/?<github-blob-url>` link (push the page, click to view rendered, no
download or local server), or a LAN / tunnel URL when pushing isn't an option.

## License

MIT
