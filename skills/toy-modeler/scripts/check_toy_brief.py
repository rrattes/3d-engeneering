#!/usr/bin/env python3
"""Check the play-experience contract in a toy_brief JSON file."""

import argparse
import json
from pathlib import Path
import sys


REQUIRED_TEXT = ("name", "intended_player", "context", "play_promise")
LOOP_FIELDS = ("invitation", "action", "response", "next_possibility")


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["$: expected a JSON object"]
    for key in REQUIRED_TEXT:
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key}: expected non-empty text")
    loop = data.get("play_loop")
    if not isinstance(loop, dict):
        errors.append("play_loop: expected an object")
    else:
        for key in LOOP_FIELDS:
            if not isinstance(loop.get(key), str) or not loop[key].strip():
                errors.append(f"play_loop.{key}: expected non-empty text")
    patterns = data.get("play_patterns")
    if not isinstance(patterns, list) or not patterns or any(not isinstance(x, str) or not x.strip() for x in patterns):
        errors.append("play_patterns: expected at least one non-empty label")
    interactions = data.get("interaction_map")
    if not isinstance(interactions, list) or not interactions:
        errors.append("interaction_map: expected at least one player action and toy response")
    else:
        for i, item in enumerate(interactions):
            if not isinstance(item, dict):
                errors.append(f"interaction_map[{i}]: expected an object")
                continue
            for key in ("part", "player_action", "toy_response", "play_value"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"interaction_map[{i}].{key}: expected non-empty text")
    mechanisms = data.get("mechanisms")
    if not isinstance(mechanisms, list):
        errors.append("mechanisms: expected an array")
    else:
        for i, item in enumerate(mechanisms):
            if not isinstance(item, dict):
                errors.append(f"mechanisms[{i}]: expected an object")
                continue
            for key in ("name", "role_in_play", "prototype_question"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"mechanisms[{i}].{key}: expected non-empty text")
    for key in ("prototype_observations", "open_questions"):
        if not isinstance(data.get(key), list):
            errors.append(f"{key}: expected an array")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.brief.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        print("Toy brief needs attention:\n- " + "\n- ".join(errors))
        return 1
    print("Toy brief structure valid; this does not validate CAD or physical behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
