"""Derive envelope evidence from the most recent CAD3D validation artifact."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
validation_path = root / "build/outputs/validation.json"
validation = json.loads(validation_path.read_text())
limit = [180.0, 120.0, 70.0]
params = {}
in_organizer = False
for line in (root / ".cad3d/params.yaml").read_text().splitlines():
    if line.strip() == "organizer:":
        in_organizer = True
        continue
    if in_organizer and line and not line.startswith(" "):
        break
    if in_organizer and ":" in line:
        key, value = line.strip().split(":", 1)
        try:
            params[key] = float(value.strip())
        except ValueError:
            continue
mins = [float("inf")] * 3
maxs = [float("-inf")] * 3
unsupported_rotation = False
for component in validation["assembly"]["components"]:
    part = component["component"]
    if part == "base":
        expected_dims = [params["base_length"], params["base_width"], params["base_thickness"]]
        local_min = [-params["base_length"] / 2, -params["base_width"] / 2, 0]
        local_max = [params["base_length"] / 2, params["base_width"] / 2, params["base_thickness"]]
    else:
        prefix = part.removeprefix("module_")
        category = f"category_{prefix}"
        module_l, module_w = params[f"{category}_length"], params[f"{category}_width"]
        module_h = params[f"{category}_height"]
        expected_dims = [module_l, module_w, module_h + params["pin_engagement"]]
        local_min = [-module_l / 2, -module_w / 2, -params["pin_engagement"]]
        local_max = [module_l / 2, module_w / 2, module_h]
    cad_dims = component["dimensions_mm"]
    dimensions_match = all(abs(float(a) - float(b)) < 1e-6 for a, b in zip(expected_dims, cad_dims))
    position = component["position_mm"]
    rotation = component.get("rotation_deg", [0, 0, 0])
    if any(abs(float(angle)) > 1e-9 for angle in rotation):
        unsupported_rotation = True
    for axis in range(3):
        mins[axis] = min(mins[axis], float(position[axis]) + local_min[axis])
        maxs[axis] = max(maxs[axis], float(position[axis]) + local_max[axis])
span = [maxs[i] - mins[i] for i in range(3)]
inside = (not unsupported_rotation and dimensions_match and all(span[i] <= limit[i] for i in range(3))
          and validation["assembly"]["status"] == "PASS")
payload = {
    "envelope": {
        "inside": inside,
        "limit_mm": limit,
        "assembly_bbox_min_mm": mins,
        "assembly_bbox_max_mm": maxs,
        "assembly_span_mm": span,
        "calculation": "axis-aligned union from parametric local datums and placed instances; compared with CAD3D measured dimensions; rotations must be zero",
        "cad_dimensions_match_parameters": dimensions_match,
        "source_validation_sha256": hashlib.sha256(validation_path.read_bytes()).hexdigest(),
    }
}
output = root / "build/outputs/design-evidence.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps(payload, indent=2))
