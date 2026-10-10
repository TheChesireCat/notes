# NETS notes

MyST Markdown site of PhD-level notes for Northeastern NETS core courses, deployed to
GitHub Pages (https://thechesirecat.github.io/notes/) on every push to `main`.
Build locally with `myst start`.

## Courses

| Course | Folder | Source |
|---|---|---|
| NETS 5116, Network Science I | `nets-5116/` (`barabasi/`, `barabasi/summaries/`, `newman/` hold chapter notes) | Barabási, *Network Science* (`network-science-textbook` skill) for intuition; Newman, *Networks* (2nd ed.) for the maths. Topic pages go directly in `nets-5116/` and combine both. |
| NETS 6116, Network Science II (Krioukov) | `nets-6116/` | `network-science-textbook` skill |
| PHYS 7335, Dynamical Processes on Complex Networks | `phys-7335/` | https://mobs-lab.github.io/phys7335/ ; Barrat, Barthélemy & Vespignani (2008) |
| NETS 7332, Machine Learning with Graphs (Eliassi-Rad) | `nets-7332/basics/`, `nets-7332/readings/` | https://eliassi.org/fa25nets.html ; basics follow Leskovec's CS224W (2021) |

Each course folder has an `index.md` landing page. Navigation is the explicit `toc:` in `myst.yml`:
a new page must be added there, either explicitly or through an existing `pattern:`. URLs follow
folders (`site.options.folders: true`), and a numeric filename prefix (`03-`) sets order and is
dropped from the URL. Use descriptive filenames that are unique within their folder.

## Writing notes

- Audience is a NETS PhD student. Be rigorous: precise definitions, derivations, key results, assumptions.
- Optimise for later recall: a short summary at the top, scannable headings, key results in
  admonitions, and cross-links to related pages in other courses.
- Synthesise and cite sources; don't reproduce textbook text verbatim.
- Start every page from `TEMPLATE.md` and keep its section order. `nets-7332/readings/01-representations.md` is the reference example.
- Use the symbols in `notation.md`; add a symbol there before using it on more than one page.
- Check numbers in worked examples by computing them, rather than copying them.
- Vocabulary for pages and sections is defined in `CONTEXT.md`.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues on TheChesireCat/notes, using the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
