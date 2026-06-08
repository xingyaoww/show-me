# repo-explainer — make sense of a whole repo

**Situation:** someone opens a repo they've never seen and needs to understand *what it
is* and *how it works* before touching code. Produce a comprehensive, self-contained HTML
report that orients them — the mental model first, then architecture, flows, and the
components, every claim grounded to real files.

Build per [`html-craft.md`](html-craft.md). This file is *what to put in it*.

## Workflow

1. **Map the surface.** README, docs, `pyproject`/`package.json`/manifest, entrypoints,
   top-level dirs, dependency list, configs, tests. Identify language(s), frameworks,
   how it's run/deployed.
2. **Find the spine.** Locate entry points (`main`, server bootstrap, CLI, job/cron) and
   trace the primary path of execution / data once, end to end. That spine is the report's
   backbone — everything else hangs off it.
3. **Explore in parallel for big repos.** Fan out read-only subagents by subsystem
   ("map the data layer", "map the API layer", "map the job pipeline") to gather
   structured notes + `file:line` anchors. *You* synthesize and draw — subagents collect,
   they don't author the diagrams.
4. **Decide the mental model.** One paragraph a newcomer could repeat: what problem it
   solves, the core abstraction, the shape (e.g. "event pipeline", "layered service",
   "compiler"). This leads the page.
5. **Draw, then write.** Top-level architecture SVG first; then per-section detail.

## Report sections (adapt; cut what doesn't apply)

1. **What it is** — the one-paragraph mental model + a 1-line "you are here" for each
   top-level dir. The reader should be oriented before scrolling.
2. **Architecture** — a hand-SVG of the major components and how they talk (processes,
   layers, services, stores). Each box = a real module/dir + `path` link. Show the
   primary data/control direction with arrows.
3. **The mental model / core abstractions** — the 2-4 types or concepts everything is
   built on (the central data structures, the key interface). Name them + link the
   defining file. This is usually the highest-leverage section.
4. **Lifecycle / main flow** — the spine from step 2 as a sequence or flow SVG: request
   in → … → result out, or job trigger → phases → outputs. Ground each step to the
   function that does it.
5. **Components** — short subsection per major piece: its job, key entry symbol, what it
   depends on, `path:line`. A table works well.
6. **Dependency graph** — *who depends on whom*, drawn as a typed-edge graph (color the
   edges by kind: import vs runtime call vs shared store vs build/deploy — see the
   dependency-graph technique in [`html-craft.md`](html-craft.md)). Back it with a
   `from → to · kind · path:line` matrix so every edge is verifiable. Most valuable for
   multi-package or multi-service codebases where the *coupling structure* (which one hard
   dependency couples everything vs. what's decoupled behind calls/stores) is the insight.
   For a single tightly-coupled package this collapses into section 5 — cut it.
7. **Deployment & network topology** *(if the repo ships to a real environment)* — where it
   runs and what can reach it: DNS → edge (TLS / LB) → internal transport → cluster ingress
   → workload → datastore, with an explicit **trust boundary** (public vs internal) and
   exposure/auth marked at each hop. Back it with an exposed-surface table (`hostname ·
   backend · auth · manifest`) and an explicit internal-only list. Ground to deploy sources
   (ingress manifests, IaC, proxy/firewall config), and **never render a secret** — see the
   deployment-topology technique in [`html-craft.md`](html-craft.md). Skip for a pure
   library / CLI with no deploy surface.
8. **Where to start (reading guide)** — rank the handful of files a newcomer should read
   first, by *importance*, not directory order. Approximate importance by fan-in (how many
   modules import/call it), centrality on the spine, and size of responsibility — the
   entrypoint, the core type, the orchestrator. Then "want to change X? start at `file`"
   task→location pointers so the reader can act after reading. (DeepWiki-style tools rank
   this with PageRank over the import graph; a careful manual read of "what does everything
   depend on" gets you the same top-5.)
9. **(optional) Notable choices / gotchas** — non-obvious design decisions or sharp edges
   worth flagging, only if you actually found them in code/docs.

## Emphasis

- **Big picture first, depth on demand.** Lead with the model + architecture diagram;
  push deep detail into later sections, tables, or `<details>`.
- **Ground relentlessly.** Every component, abstraction, and flow step links to its file
  (`path:line`, clickable via the repo blob URL — see craft ref). A newcomer's first move
  after the picture is to open the code; make that one click.
- **One architecture SVG beats five paragraphs.** Spend effort on the top-level diagram —
  it's what the reader screenshots and remembers.
- **Don't invent.** If the code doesn't show it, don't claim it. Mark inferences as such.
- **Match depth to the ask.** Default to *comprehensive* (every major subsystem gets a
  section + diagram). If the reader wants a fast orientation, do a *concise* pass: just the
  mental model, the one architecture diagram, and the reading guide — skip per-component
  detail. State which mode you produced.
