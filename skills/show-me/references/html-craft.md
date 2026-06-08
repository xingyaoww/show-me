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

## Dependency / relationship graphs (typed edges)

A common ask is "draw the dependency graph" — who imports whom, who calls whom, who
shares a store. A plain box-and-arrow blob fails here: the reader can't tell *what kind*
of dependency each arrow is, and an all-to-all graph degenerates into a hairball. The
technique that works: **color the edge by its KIND, and make the kind legible from a
legend.** The arrow's existence is half the information; its *type* is the other half.

**Encode edge kind, not just direction.** Pick a small fixed vocabulary of dependency
kinds and give each one a distinct stroke. A typical set for a software graph:

```html
<defs>
 <marker id="m-imp" .../> <marker id="m-call" .../> <marker id="m-store" .../>
 <style>
  .imp  {stroke:#2b4eaa;stroke-width:2;fill:none}                 /* code import / compile-time type dep */
  .call {stroke:#b25b0e;stroke-width:1.6;fill:none}              /* runtime service call (HTTP/RPC/queue) */
  .store{stroke:#2f7a3a;stroke-width:1.4;fill:none;stroke-dasharray:5 3} /* shared datastore: write→store→read */
  .build{stroke:#8a8a82;stroke-width:1.5;fill:none;stroke-dasharray:2 2} /* build / deploy / codegen */
 </style>
</defs>
```

The exact kinds depend on the system — adapt them (e.g. `inherits`, `event`, `config`,
`generates`). The rule is: **one stroke style per kind, defined once, shown in a legend
the reader can't miss.** A graph with three arrow colors and no legend is a worse graph
than one with prose.

**Discipline for a readable dep graph:**
- **Distinguish nodes too.** Color/shape nodes by group (layer, owner, runtime, package)
  so clusters read at a glance. Give stores/externals a different shape than code units.
- **Direction = "depends on".** Be consistent: arrow points from the dependent to the
  thing it needs. State the convention in the legend (people assume both directions).
- **Kill the hairball.** If everything depends on everything, you're drawing at the wrong
  altitude — collapse leaf nodes into their package, or split into two figures (e.g. a
  runtime-dependency figure and a build/deploy figure, which often point opposite ways).
  Don't draw an edge that's true of *every* node (e.g. "everything logs") — it's noise.
- **Ground the edges, not just the nodes.** The high-value move: back the graph with a
  small **dependency matrix** table — `from → to · kind · path:line` — where each row links
  to the import statement / call site / config that *proves* the edge. The picture shows
  shape; the table lets the reader verify any single edge.
- **Call out the load-bearing edge.** Often one or two edges are the real coupling (a hard
  compile-time dependency) while the rest are decoupled (calls/stores). Make those visually
  loudest and say so — that's the insight a newcomer actually needs.
- A relationship you can't tie to a real import/call/config is a *conjecture* — style it
  differently (lighter / dotted) and label it, or leave it out.

Mermaid can do a quick `graph LR` for a throwaway dep sketch, but it can't color edges by
kind cleanly or hold a hand-tuned layout — for the carrying dependency figure, hand-SVG wins.

## Deployment / network topology (trust boundaries)

When the repo ships to a real environment — anything with public ingress, TLS, load
balancers, a VPN/overlay, multiple hosts/clusters, managed datastores — *how it's deployed
and what's reachable from where* is part of understanding it, and a security-relevant part.
Draw it as a left-to-right **topology with an explicit trust boundary**:

```
[ public ]  │  [ internal / overlay ]
 client → DNS → edge (TLS / LB / WAF) │ → cluster ingress → service → datastore
                                      ▲ trust boundary (draw it as a line)
```

What makes this diagram useful rather than decorative:
- **Draw the trust boundary as a literal line** (dashed, loud color) separating "public /
  untrusted" from "internal / overlay / private". The single most important thing a reader
  takes away is *what is exposed vs. what is not*.
- **Tier the path the way packets actually flow:** DNS (which provider, which record →
  which IP) → edge (reverse proxy / LB / CDN, where TLS terminates) → internal transport
  (VPN / overlay / private subnet) → cluster ingress → workload → datastore. One column per
  tier reads cleanly.
- **Mark exposure and auth at each boundary**, not just connectivity: which hostnames are
  public, where TLS terminates, which ingress is behind an auth gateway/SSO vs. open, what
  is reachable *only* on the internal network. A glyph legend works (🔒 authed · 🔑
  self-auth · ⚠ open).
- **State the exposed surface explicitly, and the NOT-exposed set explicitly.** A short
  table — `hostname · backend · auth · manifest` — plus a list of "internal-only" datastores
  and admin ports. Readers (and auditors) need the negative space as much as the positive.
- **Ground to the deploy source, not the app code.** Edges and boundaries cite the things
  that actually define them: ingress/Service manifests, IaC (DNS records, LB config), reverse
  proxy config, firewall/security-group rules. Pin them like any other claim.
- **Never copy a secret into the page.** Deploy/edge configs often contain credentials —
  reference the file and the *mechanism* (e.g. "creds via env/secret store"), never the
  value. If you find a plaintext secret while reading, report it to the user out-of-band;
  do not render it.

This is its own figure, distinct from the architecture diagram (logical components) and the
dependency graph (who-needs-whom): it answers *where does this run and what can reach it*.

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

## Hand it to the human

The page is useless if the reader can't open it. Two ways; **prefer the GitHub link** — a
plain clickable URL needs no network reachability to *your* machine and no local download.

### Preferred: push to GitHub → htmlpreview link

Because the page is **self-contained**, GitHub can render it through `htmlpreview.github.io`
(it fetches the raw HTML and serves it with the right content-type — plain `raw.githubusercontent.com`
won't, it returns `text/plain`). Push the file, then build the link:

```bash
# commit the html somewhere in a repo you can push (a branch, a .pr/ or docs/ dir is fine)
git add path/to/page.html && git commit -m "show-me page" && git push origin <branch>
# link template:
#   https://htmlpreview.github.io/?https://github.com/<owner>/<repo>/blob/<branch>/<path>.html
```

Example shape:
`https://htmlpreview.github.io/?https://github.com/OWNER/REPO/blob/BRANCH/dir/page.html`

Anyone clicks it and sees the rendered page — no download, no server, works across machines.
Caveats: works best for self-contained pages (inline CSS/SVG — what this skill produces);
CDN `<script>` (e.g. Mermaid) still load over the network but render fine; private repos
need the viewer to be authed to GitHub. (GitHub Pages on the repo is an alternative if you
want a stable URL without the `htmlpreview` prefix.)

### Local alternative: serve over HTTP

When you can't/shouldn't push (unpushed work, private context), serve it and hand back a
LAN / tunnel IP — not `localhost`, since the human is often on another machine:

```bash
cd <dir> && (python3 -m http.server <port> >/dev/null 2>&1 &)
ip -4 addr show | grep -oP 'inet \K[0-9.]+' | grep -v 127.0.0.1   # LAN / overlay IPs
command -v tailscale >/dev/null && tailscale ip -4 | head -1       # tunnel IP (cross-net)
```

`http.server` binds `0.0.0.0` → `http://<LAN-or-tunnel-IP>:<port>/`. If it won't open, it's
usually a firewall.
