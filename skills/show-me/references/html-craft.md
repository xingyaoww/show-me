# html-craft — how to build the page

Shared craft for every show-me dimension. One self-contained, offline, editorial HTML
page with hand-drawn SVG figures and code-grounded claims.

## The look (editorial document, light theme)

Calm, readable, document-like — not a dark dashboard. Skeleton:

```html
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{Title}}</title>
<style>
  :root{
    --fg:#1a1a1a; --muted:#5a5a5a; --bg:#fdfdfb; --accent:#2b4eaa; --accent-soft:#e6ecfa;
    --rule:#e2e2dc; --code-bg:#f3f1ec; --warn:#b25b0e; --ok:#2f7a3a; --crit:#a02020;
    --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;
  }
  *{box-sizing:border-box} html,body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans)}
  body{line-height:1.6;font-size:16px}
  .wrap{display:grid;grid-template-columns:240px minmax(0,1fr);gap:48px;max-width:1180px;margin:0 auto;padding:32px 28px 96px}
  nav.toc{position:sticky;top:24px;align-self:start;font-size:13px}
  nav.toc h2{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
  nav.toc ol{list-style:none;padding:0;margin:0;counter-reset:toc}
  nav.toc li{counter-increment:toc;margin:4px 0}
  nav.toc li::before{content:counter(toc) ". ";color:var(--muted)}
  nav.toc a{color:var(--fg);text-decoration:none} nav.toc a:hover{color:var(--accent)}
  header.title{border-bottom:1px solid var(--rule);padding-bottom:22px;margin-bottom:28px}
  header.title .eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700}
  header.title h1{font-size:34px;margin:6px 0 4px;letter-spacing:-.01em}
  header.title .sub{color:var(--muted);max-width:740px}
  h2{font-size:22px;margin:44px 0 10px} h2 .num{color:var(--muted);font-weight:500;margin-right:8px}
  h3{font-size:16px;margin:22px 0 8px}
  code{font-family:var(--mono);font-size:.88em;background:var(--code-bg);padding:1px 5px;border-radius:3px}
  pre{font-family:var(--mono);font-size:13px;background:var(--code-bg);padding:14px 16px;border-radius:6px;overflow-x:auto;border:1px solid var(--rule)}
  pre code{background:transparent;padding:0}
  .kw{color:#7048a8}.str{color:#2f7a3a}.com{color:#8a8a82;font-style:italic}
  table{border-collapse:collapse;width:100%;font-size:14px;margin:12px 0}
  th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
  th{font-weight:600;background:var(--code-bg)}
  .callout{border-left:3px solid var(--accent);background:var(--accent-soft);padding:10px 14px;margin:14px 0;border-radius:0 4px 4px 0;font-size:14.5px}
  .callout.warn{border-color:var(--warn);background:#fbf1e6} .callout.note{border-color:var(--muted);background:#f3f1ec}
  .fig{margin:18px 0 22px}
  .fig svg{display:block;max-width:100%;height:auto;background:#fff;border:1px solid var(--rule);border-radius:6px}
  .fig figcaption{font-size:13px;color:var(--muted);margin-top:6px;text-align:center}
  a.src{font-family:var(--mono);font-size:12px;color:var(--accent);text-decoration:none;border-bottom:1px dotted var(--accent)}
  details{border:1px solid var(--rule);border-radius:6px;margin:12px 0}
  details>summary{cursor:pointer;padding:8px 12px;color:var(--muted);font-size:13px;list-style:none}
  details>summary::before{content:"▸ "} details[open]>summary::before{content:"▾ "}
  .ba{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}
  @media(max-width:760px){.wrap{grid-template-columns:1fr}.ba{grid-template-columns:1fr}}
</style></head><body>
<div class="wrap">
  <nav class="toc"><h2>Contents</h2><ol>
    <li><a href="#sec1">…</a></li>
  </ol></nav>
  <main>
    <header class="title"><div class="eyebrow">{{kind}}</div><h1>{{Title}}</h1>
      <p class="sub">{{one-paragraph mental model — the big picture in 2-3 sentences}}</p></header>
    <section id="sec1"><h2><span class="num">1</span>…</h2> … </section>
  </main>
</div></body></html>
```

Numbered sticky TOC + one-paragraph mental model up top + sectioned body. No JS needed
for this shell.

## Hand-drawn SVG figures (the diagrams that carry the argument)

Draw bespoke inline `<svg viewBox="0 0 W H">` with a `<defs>` for arrow markers and a
scoped `<style>`. You place every box → before/after stays aligned, legible, and the
delta is unmistakable. Semantic class system:

```html
<svg viewBox="0 0 960 460" role="img" aria-label="...">
 <defs>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 Z" fill="#2b4eaa"/></marker>
  <marker id="arr-chg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 Z" fill="#b25b0e"/></marker>
  <style>
    .existing{fill:#f3f1ec;stroke:#8a8a82;stroke-width:1.4;stroke-dasharray:5 3}  /* before / pre-existing */
    .ex-title{font:700 13px sans-serif;fill:#5a5a5a} .ex-detail{font:11.5px sans-serif;fill:#5a5a5a}
    .new{fill:#e6ecfa;stroke:#2b4eaa;stroke-width:2}                              /* after / added */
    .new-title{font:800 13px sans-serif;fill:#2b4eaa} .detail{font:11.5px sans-serif;fill:#1a1a1a}
    .edge{stroke:#2b4eaa;stroke-width:1.5;fill:none}
    .edge-chg{stroke:#b25b0e;stroke-width:1.8;fill:none;stroke-dasharray:5 3}     /* the changed / new flow */
    .lbl{font:600 10.5px sans-serif;fill:#2b4eaa} .gap{font:700 11.5px sans-serif;fill:#b25b0e}
  </style>
 </defs>
 <rect class="existing" x="40" y="60" width="180" height="74" rx="6"/>
 <text class="ex-title" x="130" y="90" text-anchor="middle">moduleA.fn()</text>
 <text class="ex-detail" x="130" y="110" text-anchor="middle">old behavior · a.py:42</text>
 <rect class="new" x="300" y="60" width="180" height="74" rx="6"/>
 <text class="new-title" x="390" y="90" text-anchor="middle">moduleA.fn()</text>
 <path class="edge-chg" d="M220,97 L300,97" marker-end="url(#arr-chg)"/>
 <text class="gap" x="260" y="88" text-anchor="middle">new path</text>
</svg>
```

**The before/after encoding (use consistently):**
- **dashed gray** (`.existing`, `.edge` muted) = what was there before / unchanged context.
- **solid accent** (`.new`) = what this change adds / the after-state.
- **orange dashed** (`.edge-chg`, `.gap`) = the *delta* — the new/changed flow, the gap being filled. This is what the eye should land on.

Node boxes carry a **title (real symbol) + a detail line (behavior + `file:line`)**, so the
diagram is already half-grounded to code.

Two ways to show before/after:
1. **Side-by-side figures** in a `.ba` grid — `<figure>` "Before" | `<figure>` "After". Best when layouts differ a lot.
2. **One overlaid figure** — existing nodes dashed-gray, new nodes/edges solid-accent + orange delta, in the same coordinate space. Best when the change is *additive* to an existing structure (most legible "what's new" read).

## Ground every claim to code (clickable)

A picture the human can't verify is a liability. Make claims droppable to source:

- Resolve the repo's web base once: `gh repo view --json url` → `https://github.com/<o>/<r>/blob/<sha>/<path>#L<n>`. Pin the **commit SHA** (or branch) so links don't rot.
- Render locations as `<a class="src" href="{{blobURL}}">path:line</a>` in node detail lines, section text, and a per-component "source" link.
- For local-only / unpushed work, link `file://` absolute paths or just show `path:line` plainly.
- Rule: if a box can't be tied to a symbol+location, it's a *concept* box — style it differently and say so; don't fake a link.

### Grounding discipline (borrowed from DeepWiki)

DeepWiki-style wikis enforce grounding hard — worth copying:

- **Source manifest per section.** Open each major section / component card with a small
  collapsed list of the exact files it's built from:
  `<details><summary>Sources</summary> path/a.py · path/b.py …</details>`. The reader sees
  what the claim rests on before trusting it.
- **Cite after every substantive claim, diagram, table, and snippet.** Inline format:
  `Sources: [path:start-end]` (range) or `[path:line]` (single), multiple allowed. A
  section with no citations is a smell — either ground it or cut it.
- **Solely from the code. Do not invent.** Every statement, box, edge, and number must be
  derived from files you actually read — not from how "similar systems usually work." If
  something important isn't in the code, say so explicitly rather than guessing. Mark genuine
  inferences as inferences.
- **Breadth check.** A "comprehensive" page that cites only 1-2 files is probably shallow —
  pull in the related files (callers, callees, config, tests) until the picture is real.

## Code excerpts (when shown)

Keep them short and hand-highlight with spans (no JS highlighter): wrap keywords
`<span class="kw">`, strings `<span class="str">`, comments `<span class="com">`.
**HTML-escape first** (`&`→`&amp;` `<`→`&lt;` `>`→`&gt;`), then wrap — source text is
untrusted; unescaped `<...>` injects. Put long diffs/code inside `<details>` (collapsed).

## Self-contained & offline

- One `.html` file. Inline all CSS and SVG. No build, no framework.
- CDN only if truly needed (e.g. Mermaid fallback `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js`); the page must still be useful if a diagram fails to load.
- Must open by double-click and survive copy to another machine.

## Mermaid (quick / auxiliary only)

For throwaway or simple graphs where layout doesn't need to be exact, Mermaid is faster
than hand-SVG. `mermaid.initialize({startOnLoad:true, theme:'neutral'})`. Node text in
`["..."]`; escape `"` as `&quot;`. But for the **carrying** before/after diagram, hand-SVG
wins — auto-layout drifts and breaks the side-by-side alignment that makes the delta readable.

## Serve for cross-machine viewing

```bash
cd <dir> && (python3 -m http.server <port> >/dev/null 2>&1 &)
ip -4 addr show | grep -oP 'inet \K[0-9.]+' | grep -v 127.0.0.1   # LAN / overlay IPs
command -v tailscale >/dev/null && tailscale ip -4 | head -1       # tunnel IP (cross-net)
```

`http.server` binds `0.0.0.0`, so hand back `http://<LAN-or-tunnel-IP>:<port>/` (not just
localhost — the human is often on another machine). If it won't open, it's usually a firewall.
