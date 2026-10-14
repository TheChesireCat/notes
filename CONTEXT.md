# NETS notes

A public site of PhD-level reference notes for Northeastern's Network Science core courses. It is written so the material can be recalled and cross-referenced long after the courses end.

## Language

### Site structure

**Course**:
One of the four NETS core courses covered by the site: NETS 5116, NETS 6116, PHYS 7335, NETS 7332.
_Avoid_: class, module

**Page**:
One MyST Markdown file that renders as one page of the site and follows the note template.
_Avoid_: note, doc, chapter (unless it really is a textbook chapter)

**Topic page**:
A page organised around one concept and combining several sources, e.g. random graphs from Barabási and Newman.
_Avoid_: chapter summary

**Basics page**:
A NETS 7332 page on foundational graph-ML material taught before the paper readings, modelled on Leskovec's CS224W.
_Avoid_: intro lecture, tutorial

**Reading page**:
A NETS 7332 page covering one syllabus topic and its assigned papers.
_Avoid_: paper summary, review

**Source**:
The textbook chapter, lecture notes, slides or paper a page is synthesised from, cited on the page.
_Avoid_: reference (reserve that for the bibliography entry)

**Note template**:
The fixed section order every page follows: TL;DR, setup and definitions, core ideas, key results, worked example, assumptions and limitations, connections, self-test.
_Avoid_: format, layout

### Page sections

**TL;DR**:
The 3–5 bullets at the top of a page holding the claims worth remembering in a year.
_Avoid_: summary, abstract

**Key result**:
A theorem, threshold, scaling law or complexity bound stated precisely, with a derivation sketch hidden in a dropdown.
_Avoid_: main finding

**Connection**:
An explicit link from a page to related material in another course, saying how the two relate.
_Avoid_: see also

**Self-test**:
Recall questions at the end of a page, with the answers hidden.
_Avoid_: quiz, exercises

### Figures

**Figure**:
A numbered, captioned visual on a page, generated from Python code so it can be reproduced and adjusted.
_Avoid_: image, picture, plot (a plot is one kind of figure)

**Sweep figure**:
A figure showing how a quantity changes as one model parameter varies, drawn as overlaid curves or a row of small panels.
_Avoid_: parameter plot, animation

**Model sample**:
A figure drawing one random graph from a model at stated parameters, so the reader sees what the ensemble produces.
_Avoid_: example network, visualisation

**Diagram**:
A schematic of how concepts, steps or models relate, made of boxes and arrows, with no data in it.
_Avoid_: figure (when there is no data), flowchart

**Figure list**:
The ranked set of figures planned for one page, each with what it shows and why it helps recall.
_Avoid_: figure backlog, wishlist
