---
name: product-design
description: Use when defining the industrial design of physical products, choosing a visual style, redesigning CAD form, or reviewing product aesthetics against a brief. Applies to physical products rather than web interfaces or standalone illustration.
---

# Product design

Develop a recognizable product through silhouette, proportions, construction,
surfaces and color/material/finish (CMF). Engineering constrains every aesthetic
choice: function, safety, performance, margins, retention, tolerances, maintenance
and manufacture. Redesign or reject styling that worsens those requirements.
Unresolved relevant technical impact blocks acceptance as the product solution.

## Optional final stage in the engineering workflow

Within a 3d-engineering project, run product-design only as an optional final stage,
after engineering has produced the CAD and scoped technical checks. Activate this
stage when the user requests appearance, a style study or aesthetic redesign; omit
it otherwise. Engineering can complete independently of this skill. Use the existing
CAD as the reference and retain its unresolved findings and validation scope.

Physical design changes return to the affected engineering checks before reviewing
the changed result and updating the delivery. A purely visual review or simulated
color study does not require regenerating unchanged CAD. Do not alter other skills
to enforce this routing.

## Choose the work actually requested

| Mode | Deliverable |
|---|---|
| `cmf_study` | Color/finish study identified as simulated; geometry can remain unchanged |
| `visual_review` | Findings tied to actual images viewed, scope and proposed corrections |
| `refinement` | Implemented changes to targeted parts/features and affected technical checks |
| `redesign` | Concrete form/construction changes, CAD evidence and review of affected requirements |

Use the current brief and prior accepted decisions. Distinguish requests from
proposals and unknowns. Ask only for information that materially changes the result.
A simple part or chosen style needs a proportionate solution, not mandatory multiple
concepts, moodboards or approval loops. A color change alone cannot close redesign.

## Protect engineering before styling geometry

Identify technical requirements and the reference revision, including what is still
unvalidated. Compare affected indicators using compatible units, operating conditions,
uncertainty, scope and current evidence. An unvalidated baseline cannot qualify the
candidate; a geometry PASS cannot establish thermal performance. Added area at one
opening does not prove compensation for reduced area at another.

For a physical change, use [engineering_guardrails.md](references/engineering_guardrails.md)
to record protected requirements and run the independent engineering gate. Limits
come from engineering; never weaken them or omit a requirement to obtain PASS.
A blocked proposal can remain an exploratory artifact, labelled accordingly, and
cannot replace the accepted reference. Gate scripts do not intercept external tools:
call the gate explicitly before acceptance. Aesthetic/user approval does not close
an engineering finding. The tools check recorded evidence, not its physical authenticity.

## Develop and implement form

Read the relevant style in [styles.md](references/styles.md): minimalista, gamer,
industrial, orgânico, retrô or a custom direction. A mixture needs a dominant grammar
and named secondary traits. Translate style into observable decisions, not decoration.
For open consequential choices, compare materially different massing/construction
concepts; if direction is chosen, refine it directly.

Use [concept_development.md](references/concept_development.md) for silhouette,
spatial budget, seams, visible fixings, openings, interactions and service cues.
Give each proposed change a part/feature, intended result and affected technical
requirement. Preserve useful volume and maintenance. Apply the authorized changes
in the product's existing CAD workflow; missing CAD remains explicitly unimplemented.
Other skills and their tools/configuration are outside this skill's edit scope.

For refinement/redesign, use [geometry_evidence.md](references/geometry_evidence.md).
The optional comparator uses the existing CAD container and explicit part frames.
STEP hash changes, equal volumes or boxes, and rigid repositioning alone do not prove
redesign. Never present concept art or a render-only alteration as exported geometry.

## Optional resources for concept depth and productivity

Use [concept_productivity.md](references/concept_productivity.md) for substyles,
reference cards and identity across parts. `scripts/style_brief.py` reads only the
selected vocabulary and references; custom directions remain valid. Actual images
must be viewed before recording visual findings.

When engineering defines editable/protected space, read
[design_freedom.md](references/design_freedom.md). A contracted map is checked by
the existing gate and selector, including explicit poses and changed-material bounds.
Use [parametric_features.md](references/parametric_features.md) for optional CAD
recipes; integrate them into existing geometry and recheck affected requirements.
Use [productivity.md](references/productivity.md) for matched STEP comparisons,
declared dependency reuse and a compact live change report. Cached outputs never
approve engineering, aesthetic review or user acceptance. Do not load every resource
or generate alternatives when a simple chosen direction is sufficient.

## Review the actual result

Use [visual_review.md](references/visual_review.md). Open relevant real images;
compare revision, camera, projection, scale and lighting. Separate render defects,
geometry, preference and missing evidence. Record criterion → image/part → finding
→ correction → evidence of resolution. Missing views stay NOT_EVALUATED.

Use [manufacturing_appearance.md](references/manufacturing_appearance.md) when form
or finish depends on printing, seams, supports, materials, texture or assembly.
Rendering a surface does not demonstrate its manufacturing feasibility or comfort.
Review changed CAD images before closing findings. Beauty has no universal score.

## Deliver and accept within scope

Reuse the project's brief/decision/review documents instead of duplicating them.
If needed use `docs/DIRECAO_DE_DESIGN.md` and `reports/REVISAO_ESTETICA.md`. Keep
engineering eligibility, visual findings, user acceptance and physical validation
separate. Only the user's actual decision can record their acceptance.

The own-flow selector in [engineering_guardrails.md](references/engineering_guardrails.md)
rechecks live evidence and requires a bound user-decision record plus visual review
before updating its local accepted-design pointer. Use it only after actual user
approval. It does not approve CAD manufacturing or physical operation.

Load only relevant references; put detailed logs on disk. Reuse valid artifacts
with provenance. Do not generate variants, tools or renders automatically for file
queries. No new CAD engine, database, image generator or service is required.
