---
# Copy this file to start a new page. It is excluded from the site build.
title: Full descriptive title
short_title: Sidebar name        # ≤ 3 words
subject: NETS 7332 · Reading     # "<course> · <Topic | Basics | Reading>"
description: One sentence saying what this page lets you recall.
tags: [tag-one, tag-two]
---

<!--
Page contract
- Audience: a network-science PhD student re-reading this months later.
- Synthesise; don't transcribe. Paraphrase sources and cite them; short quotes only.
- Every non-obvious claim has a source. Mark your own commentary as such.
- Use the shared symbols from notation.md; list page-specific symbols under "Notation".
- Label anything you might link to: (sec-…)=, :label: def-… / thm-…, equations with (eq-…).
- Delete the guidance comments when the page is written; keep the section order.
-->

:::{tip} TL;DR
- 3–5 bullets: the claims, results and formulas worth remembering in a year.
- Each bullet should stand on its own without the rest of the page.
:::

- **Source.** [](doi:10.xxxx/xxxxx) <!-- or a URL / textbook chapter -->
- **Builds on.** [](#label-of-prerequisite-page)
- **Notation.** Shared symbols as in [](#notation); page-specific symbols defined below.

(sec-template-setup)=
## Setup and definitions

<!-- Problem statement and the objects involved. One prf:definition per concept. -->

:::{prf:definition} Name of concept
:label: def-template-concept

Precise statement, with symbols.
:::

## Core ideas

<!-- Models, methods, arguments: the body of the page. Short paragraphs, tables
     for comparisons, figures only if they explain something prose can't. -->

## Key results

<!-- Theorems, thresholds, scaling laws, algorithm complexities. Number equations
     you will refer to. Put derivations in dropdowns so the result stays scannable. -->

:::{prf:theorem} Name of result
:label: thm-template-result

$$
\lambda_c = \frac{\langle k \rangle}{\langle k^2 \rangle}
$$ (eq-template-result)
:::

:::{dropdown} Derivation sketch
Steps, with the assumption used at each step stated explicitly.
:::

## Worked example

<!-- A small concrete case with numbers you have checked. -->

## Assumptions and limitations

<!-- When does this break? What does it ignore? Known critiques (cite them). -->

## Connections

<!-- Cross-course links: "same object as …", "generalises …", "contrasts with …". -->
- **NETS 5116.** …
- **NETS 6116.** …
- **PHYS 7335.** …
- **NETS 7332.** …

## Self-test

<!-- 3–6 questions you should be able to answer from memory. Answers hidden. -->

:::{dropdown} Q1. Question text?
Answer.
:::
