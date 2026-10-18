# Product aesthetic review

## Engineering precedence

Record affected technical requirements and their assessment alongside visual
findings. A visual PASS cannot accept a proposal with engineering degradation or
unresolved relevant technical impact. Mark that proposal **blocked for product
acceptance**, cite the finding and specify the redesign or evidence required.
Preserve independent visual observations as scoped findings, not overall approval.

## Evidence first

Identify the brief/design direction, product revision and images to inspect. For a
CAD delivery, prefer views from the selected run and record its identifier. A loose
image may be reviewed as an image with unknown model provenance; mark that limit.
Open actual images. File existence, filenames and image generation logs are not
visual inspection. If image viewing is unavailable, provide the review plan and
leave visual conclusions NOT_EVALUATED.

Use matching views and framing to compare alternatives. Individual part galleries
may auto-scale: do not infer relative dimensions from them. Use orthographic or
measured CAD information for proportions. A perspective view communicates form,
not reliable dimensions. Record whether color, texture and finish are simulated.

## Choose useful views

| Question | Useful evidence |
|---|---|
| Identity and main silhouette | Opaque overall view plus a second revealing angle |
| Proportion and alignment | Front/top/side views or dimensional geometry |
| Installed appearance and scale | Context view with known scale or dimensions |
| Seams, controls and fixings | Detail of the relevant visible interface |
| Internal or service appearance | Targeted section/exploded view, with the relevant components identified |
| Texture, gloss and real color | Declared render setup; physical sample when appearance depends on process |

Select views according to the task. A missing decisive view prevents a conclusion
on that criterion; it does not require generating every possible view.

## Criterion-specific findings

Assess only applicable criteria, tied to the brief:

- Silhouette and massing: recognizable hierarchy, use context and meaningful volume distribution.
- Proportion and rhythm: relationships of body/base, openings, repeated details and negative space.
- Surface language: consistent intentional radii, chamfers, facets or curvature transitions.
- Construction coherence: seams, fasteners, panel breaks, service cues and visible assembly.
- Interaction: visible controls, handling cues, contact edges and cleaning access; ergonomics remains physically unverified.
- CMF: consistent material/color/finish proposal and honest representation of actual manufacturing capability.
- Detail discipline: intentional branding, vents and accents; identify visual clutter or unresolved intersections with specific evidence.

Adapt criteria to the product. A basket does not need electronics controls, and
an unseen internal support does not need a decorative exterior treatment.

## Review record

Use this compact structure in the project's review document:

```markdown
Direction and criteria: [link to current design intent]
Revision/run: [known model identifier or explicitly unknown]
Images actually viewed: [file links]

| Criterion | Evidence and observation | State | Correction or next evidence |
|---|---|---|---|

Priority corrections: [affected part/feature and intended visible result]
Technical rechecks needed: [affected constraints for engineering]
User acceptance: [explicit decision/reference, or pending]
```

State meanings:

- **PASS:** viewed evidence supports the stated criterion within the recorded scope.
- **WARNING:** a concrete reservation remains, such as simulated finish or an unresolved preference.
- **FAIL:** viewed evidence contradicts a declared criterion; cite where and how.
- **NOT_EVALUATED:** required evidence or criterion is missing/ambiguous.

Do not average these into a beauty score or hide FAIL/NOT_EVALUATED behind an overall
PASS. An overall summary should identify what was reviewed and what remains open.
User acceptance requires the user's actual decision, separately from this assessment.

## Correction and iteration

Prioritize changes that affect silhouette and proportion before local decoration.
For each finding, identify whether it comes from geometry, camera/lighting/material
rendering, or an undecided preference. A rendering artifact calls for better evidence;
a geometry defect calls for a CAD change with technical checks; a preference conflict
calls for a scoped choice using existing authorization when sufficient.

Record implemented changes and view the resulting images before claiming resolution.
Preserve the earlier revision or comparison evidence. Render-only paint cannot close
a modeled feature defect. Aesthetic findings cannot close thermal, structural, fit,
water-protection or manufacturing risks. Physical finish and comfort remain pending
until appropriate samples or user evaluation exist.

## Machine-readable acceptance record

For the own-flow selector, engineering sets a nonempty `visual_criteria` list of IDs
in the contract before approval (for example silhouette, service_seams). The reviewer
records JSON with schema `product-design-visual-review-v1`, `revision`, `reviewer`,
`contract_sha256`, `candidate_sha256`, `status`, `images` and `criteria`. Hashes of
contract/candidate are canonical JSON; image references use raw file SHA256.

Each criterion has `id`, `status`, `image_paths` (a nonempty subset of referenced
images), `finding` and `resolution`. PASS means the scoped criterion was reviewed
and closed, not that the product is physically proven. Record camera/projection,
scale, lighting, rendered material and model/run provenance alongside each image.
These extra descriptive fields remain reviewer evidence, not automatic visual checks.
The selector checks presence, hashes and closure; it cannot establish that a human
or agent actually viewed an image. Never populate PASS from filenames or tool success.

A separate decision JSON records `authority: user`, `decision: APPROVED`,
`contract_sha256`, `candidate_sha256`, `visual_review_sha256` (raw review file hash),
and the contract's `target_scope`. Create this record only from actual user approval.
Changed evidence or a changed candidate requires a new corresponding review/decision.

```sh
python3 scripts/select_candidate.py --project /path/to/product \
  --contract design/product-design/contract.json \
  --candidate reports/product-design/candidate.json \
  --visual-review reports/product-design/visual-review.json \
  --user-decision design/product-design/user-decision.json
```

The command updates only `design/product-design/accepted.json` on ACCEPTED (exit 0).
BLOCKED returns 3 and preserves the previous pointer. Invalid CLI input returns 2.
A stale `.lock` after process termination requires checking for a live selector
before removing the lock. This local record/lock is not an authentication system,
a transaction across externally editable evidence or a gate on CAD3D publication.

For automated matched-camera STEP images, see [productivity.md](productivity.md).
Automatic framing records geometry and camera evidence; open the images before
closing visual findings. It does not certify quality, color, comfort or manufacture.
