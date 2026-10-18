# Measured fit calibration and preliminary structural screening

These opt-in APIs do not write presets or modify the supplied records. A report's analytical `PASS` is distinct from physical fit or load validation, which remains `NOT_EVALUATED`.

## Fit calibration

```python
from fit_calibration import derive_fit_calibration
identity = {
    'printer': 'machine-serial-or-unique-id',
    'nozzle_mm': 0.4,
    'material': 'material-and-lot-id',
    'process_sha256': '<64 lowercase hex digest of the actual process settings>',
    'orientation': 'coupon-specific orientation identifier',
}
payload = {
    'identity': identity,
    'confirmed_measured': True,
    'measured_at': '<actual ISO8601 measurement time including timezone>',
    'valid_until': '<explicit ISO8601 expiry including timezone>',
    'evidence': {'path': 'evidence/coupon-measurements.csv',
                 'sha256': '<64 lowercase hex digest of that local evidence file>'},
    'measurements': [
        {'feature': 'hole-10', 'nominal_mm': 10, 'actual_mm': 10.2, 'uncertainty_mm': 0.05},
        {'feature': 'hole-10', 'nominal_mm': 10, 'actual_mm': 10.4, 'uncertainty_mm': 0.05},
    ],
}
report = derive_fit_calibration(payload, expected_identity=identity, project_root='.')
```

The values above are synthetic API examples, not evidence for any printer or material. Evidence must resolve inside the project, including through symlinks; absolute paths and escaped project paths are rejected. SHA256 is checked against file bytes. Dates must include a timezone and the current UTC time must be inside the declared interval. Missing confirmation, identity, evidence or dates cannot produce a calibrated result. Valid differing identities, expired records, future measurements, escaped evidence and changed evidence hashes fail. Invalid/missing fields remain explicit unknowns or raise validation errors for malformed numeric records.

Identity equality includes all provided keys. At minimum it requires exact printer, nozzle, material, process hash and orientation. The caller must independently supply the intended identity; passing the measured identity as the expected identity, as in the minimal example, checks completeness but does not establish an independent manufacturing match. Include additional lot/revision/conditioning fields when these matter. The API verifies the supplied process digest format and equality; the caller is responsible for deriving that digest from the actual process settings.

For each feature all samples must share the exact nominal size; different sizes require distinct feature identifiers. Bias means `actual − nominal`; the reported offset recommendation is `−mean_bias`. Sample lower and upper dimensions are the extrema of `actual ± uncertainty`, so the envelope includes measurement uncertainty and observed sample spread rather than merely mean error. The example yields mean bias +0.3 mm, bias interval [+0.15,+0.45] mm and an observed actual dimension interval [10.15,10.45] mm. Returned `tolerance_dimensions` use the existing signed tolerance evaluator's `nominal_mm/min_mm/max_mm/basis/source` contract and carry the evidence hash.

These are observed sample envelopes, not statistical confidence bounds, worst-case bounds of a future manufacturing population, or proof of retention/clearance. Offset recommendations need a newly printed and measured coupon before being accepted. The payload's confirmation and file provenance are declarations: hashing records their integrity but does not independently inspect instruments, confirm real measurements, parse arbitrary evidence documents, or audit transcription. Dates and identity constrain applicability, not metrological truth. No preset is overwritten.

## Structural screening

```python
from structural_screening import cantilever_screen
record = {
    'id': 'example-beam',
    'model': 'rectangular_cantilever_end_load', 'units': 'N-mm-MPa',
    'length_mm': 100, 'width_mm': 20, 'thickness_mm': 10, 'load_n': 10,
    'elastic_modulus_mpa': 2000, 'allowable_stress_mpa': 12,
    'max_deflection_mm': 2, 'safety_factor': 2,
    'provenance': {
        'elastic_modulus_mpa': {'basis': 'assumed', 'source': 'synthetic arithmetic example'},
        'allowable_stress_mpa': {'basis': 'assumed', 'source': 'synthetic arithmetic example'},
    },
    'assumptions': {
        'fixed_support': True, 'transverse_tip_load': True,
        'prismatic_solid_section': True, 'linear_elastic_homogeneous': True,
    },
}
report = cantilever_screen(record)
```

Both material properties and their provenance are mandatory. Provenance basis is `measured`, `supplier` or `assumed`; assumptions produce `WARNING` when the supplied analytical limits are met, while a limit failure remains `FAIL`. Missing inputs/provenance/model confirmation return `NOT_EVALUATED`. Unsupported models/units and negative, boolean, nonfinite or otherwise invalid numeric values raise `ValueError`. No default polymer strength, modulus, safety factor or allowable deflection is supplied. The user must determine suitable values for orientation, process, temperature, aging, load duration and intended use.

`thickness_mm` is the cross-section dimension in the bending direction and `width_mm` is transverse to it. The implementation uses `I = width × thickness³ / 12`, maximum moment `M = P × L`, bending stress magnitude `σ = M × thickness / (2I)` and tip deflection `δ = P × L³ / (3EI)`. N/mm² equals MPa. Stress is compared with `allowable_stress_mpa / safety_factor`; nominal deflection is compared with `max_deflection_mm` at the supplied service load. `achieved_stress_safety_factor` is allowable/stress, or null at zero stress. A supplied allowable that already includes design factors will be divided by the requested safety factor again; choose it deliberately.

The synthetic example yields I = 1666.6667 mm⁴, σ = 3 MPa, δ = 1 mm, stress limit = 6 MPa and nominal stress safety factor = 4. Its assumed material provenance keeps overall status `WARNING`. An otherwise identical record with documented measured/supplier provenance passes only the arithmetic screen.

The 5% deflection/span and 10:1 span/thickness thresholds are explicit review heuristics, not certified model-validity boundaries. Crossing either adds a warning even if the user's numerical limits pass. The model does not resolve shear deformation, anchorage, joint failure, holes/notches/stress concentrations, buckling, fatigue, creep, temperature dependence, nonlinear deformation or the anisotropy/infill of printed parts. An FDM part requires a justified effective model and corresponding properties; the homogeneous solid calculation itself cannot establish those.

Primary formula sources checked on 2026-10-17:

- [MIT 1.050, end-loaded cantilever displacement, page 2](https://ocw.mit.edu/courses/1-050-solid-mechanics-fall-2004/fd4eff39aec922b8c07660006f40686e_pset04_11.pdf).
- [MIT, David Roylance, Stresses in Beams, equations 5–7, pages 3–4](https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/96d839b02e4a6c63cf8031800e89cccd_MIT3_11F99_bstress.pdf).

## Execution evidence

Both scripts ran using the existing `cad3d-engineering:1.7.0` image (`sha256:4d7d07da15f97fb04f3d59ca4f7ffe864f394e55a1b558dbee4d76e981d13b0a`) and a read-only `/candidate` source mount. No CAD host package or dependency installation was used.

- [Calibration expected initial failure](calibration-red.log): 6 tests fail because the module is absent.
- [Structural expected initial failure](structure-red.log): 6 tests fail because the module is absent.
- [Calibration final run](calibration-green.log): 6 tests pass, including identity mismatch, integrity, local evidence confinement, validity, numeric rejection, distinct nominal scope, unchanged input and observed envelope checks.
- [Structural final run](structure-green.log): 6 tests pass, including independent hand-calculated values, cubic thickness sensitivity, limits, assumed/missing provenance, unsupported models/units, invalid numbers, zero load and linear-model warnings.

Tests establish software behavior for synthetic records, not measured calibration or physical qualification of a manufactured part. Shared CLI integration and full platform regression are tracked by the parent implementation task.
