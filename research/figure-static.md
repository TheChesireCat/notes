---
title: Figure pipeline test, committed SVGs
short_title: Static test
description: Throwaway page for issue #77, testing script-generated committed figures (no CI Python).
---

Throwaway test page for issue #77 (option (c)). `research/scripts/degree_plot.py` is run
locally and writes `research/img/degree-*.{svg,png}`, which are committed. CI needs no Python.

## 1. Figure plus the script in a dropdown

:::{figure} ./img/degree-transparent.svg
:label: fig-ba-degree-static
:alt: Log-log degree distribution of a Barabási–Albert graph with the k^-3 guide line.
:width: 80%
Degree distribution of a BA graph ($N=5000$, $m=3$) against $p_k = 2m^2k^{-3}$.
Transparent SVG.
:::

::::{dropdown} Source: `research/scripts/degree_plot.py`
:::{literalinclude} ./scripts/degree_plot.py
:language: python
:::
::::

Only the plotting lines, using `:lines:`:

::::{dropdown} Plotting lines only
:::{literalinclude} ./scripts/degree_plot.py
:language: python
:start-at: fig, ax = plt.subplots
:end-before: for bg in
:::
::::

## 2. Dark mode, committed images

::::{grid} 2

:::{figure} ./img/degree-white.svg
SVG, white background.
:::

:::{figure} ./img/degree-transparent.svg
SVG, transparent background.
:::

:::{figure} ./img/degree-white.png
PNG, white background.
:::

:::{figure} ./img/degree-transparent.png
PNG, transparent background.
:::

::::

## 3. Dark mode, swapping two variants by class

The theme CSS has `dark:hidden` and `dark:block`. The light variant has
`:class: dark:hidden`; the dark variant has `:class: hidden dark:block`.

```{image} ./img/degree-white.svg
:class: dark:hidden
:width: 60%
```

```{image} ./img/degree-dark.svg
:class: hidden dark:block
:width: 60%
```

## 4. Dark mode, custom CSS

`site.options.style: research/figures.css` adds
`.dark img.invert-dark { filter: invert(1) hue-rotate(180deg) }`.

```{image} ./img/degree-transparent.svg
:class: invert-dark
:width: 60%
```

## 5. Option (b): embedding a figure from a committed companion notebook

`research/figure-companion.ipynb` is executed locally by `research/scripts/make_companion.py`
and committed with outputs. This page has no `kernelspec`; it embeds the notebook's labelled cell.

:::{figure} #fig-companion-ws
:label: fig-companion-ws-embedded
Watts–Strogatz $C(p)/C(0)$ and $L(p)/L(0)$, $N=1000$, $k=10$, embedded from the companion notebook.
:::
