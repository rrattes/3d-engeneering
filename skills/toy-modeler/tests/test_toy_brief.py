import json
from pathlib import Path
import sys
import unittest

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from check_toy_brief import validate  # noqa: E402


class ToyBriefTests(unittest.TestCase):
    def setUp(self):
        self.brief = json.loads((SKILL_DIR / "assets/toy_brief.example.json").read_text())

    def test_example_has_a_play_loop_and_interaction_purpose(self):
        self.assertEqual(validate(self.brief), [])

    def test_mechanism_without_play_purpose_is_rejected(self):
        self.brief["mechanisms"][0]["role_in_play"] = "  "
        self.assertIn("mechanisms[0].role_in_play: expected non-empty text", validate(self.brief))

    def test_interaction_without_toy_response_is_rejected(self):
        self.brief["interaction_map"][0].pop("toy_response")
        self.assertIn("interaction_map[0].toy_response: expected non-empty text", validate(self.brief))

    def test_decorative_object_without_play_interaction_is_rejected(self):
        self.brief["interaction_map"] = []
        self.assertIn("interaction_map: expected at least one player action and toy response", validate(self.brief))


if __name__ == "__main__":
    unittest.main()
