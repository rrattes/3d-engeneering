# Engineering-owned design freedom

For a physical refinement/redesign, engineering identifies locked parts, datums,
interfaces and clearance regions before exterior changes. Record editable space as
explicit permissions, not as whatever styling happens to leave untouched.

Contract field `design_freedom` is a pinned JSON reference. The enclosing engineering
policy approval includes this reference. `evaluate_design.py` checks the map live
and the existing selector inherits its result; FAIL or NOT_EVALUATED blocks selection.
Omitting/changing a contracted map changes the approved policy. Do not weaken it for style.
Older contracts without a map retain their prior behavior; they do not acquire this check.

Map schema `product-design-freedom-v1`: `units: mm`, `coordinate_frame:
comparison_local_mm`, `baseline_revision`, engineering_source reference,
nonnegative `margin_mm`, and `parts`. Each part: id, pinned source STEP, explicit
locked/pose_locked booleans, editable_regions and protected_regions. Regions have
id and bounds_mm [[xmin,ymin,zmin],[xmax,ymax,zmax]], positive extents. Protected
regions also name their engineering reason. Source paths must match the comparison's
before-model map. The comparison configuration must use include_delta_bounds: true.

The comparator subtracts atomic solids after its explicit pose normalization,
then bounds the changed material. Changed boxes touching protected boxes fail;
they must fit inside one editable box with the declared margin. Missing provenance,
frames, delta geometry or permission stays NOT_EVALUATED. A locked pose cannot move.
This is conservative: two separated changes may produce one encompassing box and
cause a false rejection. Seek finer evidence/engineering disposition instead of
relaxing protection. This does not certify arbitrary surfaces or continuous clearance.

Do not infer physical validation from the map. For render-only work, retain the
existing model and technical status; a new spatial map is unnecessary.

## Authoritative frames and detection limits

Every mapped part also provides `before_pose` (six finite translation/rotation
values) approved with the map; it must match the before pose used by the comparison.
The map's comparison_policy explicitly pins positive linear_tolerance_mm,
volume_tolerance_mm3 and angular_tolerance_deg. The comparison config and report
must match these limits. Moving both frames or increasing detection thresholds
cannot silently expand editable space. A pose_locked part compares declared frame
values directly; a sub-tolerance declared move is still a prohibited pose change.

comparison_policy.non_detection_policy is mandatory: require_identical_source
requires identical STEP bytes for a part with no detected shape change; reexported
but different bytes remains NOT_EVALUATED. accept_approved_thresholds accepts only
the engineering-authorized detection coverage and explicitly leaves smaller changes
outside it. Choose that policy only where engineering judges the thresholds adequate;
it does not prove absolutely unchanged material or exclude tiny local changes.
Invalid intermediate/fragments or inconsistent delta volume make CAD evidence
NOT_EVALUATED; the comparator cannot discard bad fragments and certify the remainder.

## Optional v2: exact BREP regions

`product-design-freedom-v2`, mode `brep_regions`, units mm, frame comparison_local_mm.
Use this only when engineering supplies pinned region STEPs. Policy declares
baseline_revision, engineering_source, nonnegative margin_mm, margins_embedded=true,
and comparison_policy with positive linear/volume/angular tolerances matching the
comparison. Physical margins must already be modeled into the regions; numerical
volume tolerance is not clearance.

Each part declares id, source of baseline STEP, before_pose/after_pose, locked and
pose_locked, and explicit lists protected_material, protected_void, editable_volumes.
Each region has id, source {path,sha256}, pose (six values, inverse transformation
into comparison frame). Region poses and both part frames belong to the authorized
engineering policy, not the candidate. Lists may be empty only by explicit policy.

The existing kernel recomputes comparison and checks retained material, free space
and added/removed material within the union of editable volumes. Opposite-side
changes need not fail because their combined bounding box crosses the core.
A preserved core never excuses occupation of a protected drawer path. Invalid or
mixed solid/free topology, stale sources and inconclusive operations fail closed.
No fallback to v1 boxes. This bounded mode supports explicit same-part correspondence
(max32 parts,32 regions/list,256 imported solids,8192 Boolean cuts per part).
New/deleted part identities require an engineering remap. Existing v1 is unchanged.
