# NETS notes

MyST Markdown site of PhD-level notes for Northeastern NETS core courses, deployed to
GitHub Pages (https://thechesirecat.github.io/notes/) on every push to `main`.
Build locally with `myst start`.

## Courses

| Course | Folder | Source |
|---|---|---|
| NETS 5116, Network Science I (Barabási) | `NETS Bar/`, `NETS 101/` | `network-science-textbook` skill |
| NETS 6116, Network Science II (Krioukov) | — | `network-science-textbook` skill |
| PHYS 7335, Dynamical Processes on Complex Networks | — | https://mobs-lab.github.io/phys7335/ |
| NETS 7332, Machine Learning with Graphs (Eliassi-Rad) | `NETS 7332/` | https://eliassi.org/fa25nets.html; intro lectures follow Leskovec's CS224W |

## Writing notes

- Audience is a NETS PhD student. Be rigorous: precise definitions, derivations, key results, assumptions.
- Optimise for later recall: a short summary at the top, scannable headings, key results in
  admonitions, and cross-links to related pages in other courses.
- Synthesise and cite sources; don't reproduce textbook text verbatim.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues on TheChesireCat/notes, using the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
