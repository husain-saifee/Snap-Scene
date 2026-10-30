import json
from pathlib import Path
import unittest


class TestSceneStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[2]

    def test_project_structure_exists(self):
        self.assertTrue((self.root / "backend").is_dir(), "backend directory must exist")
        self.assertTrue((self.root / "backend" / "workers").is_dir(), "workers directory must exist")
        self.assertTrue((self.root / "backend" / "assets").is_dir(), "assets directory must exist")
        self.assertTrue((self.root / "shared").is_dir(), "shared directory must exist")

    def test_scene_schema_definition(self):
        schema_file = self.root / "shared" / "schemas" / "scene.json"
        if schema_file.exists():
            with open(schema_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, dict, "Scene schema must be a valid JSON dictionary")

    def test_motion_json_validation(self):
        motion_json = self.root / "backend" / "workers" / "image_gen.json"
        if motion_json.exists():
            with open(motion_json, "r", encoding="utf-8") as f:
                scenes = json.load(f)
            self.assertIsInstance(scenes, list, "image_gen.json must contain a list of scenes")
            for scene in scenes:
                self.assertIn("scene_id", scene)
                self.assertIn("duration", scene)
                self.assertIn("characters", scene)


if __name__ == "__main__":
    unittest.main()
