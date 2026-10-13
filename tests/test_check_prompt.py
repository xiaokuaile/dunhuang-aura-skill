#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_prompt.py"


class PromptCheckerTests(unittest.TestCase):
    def run_checker(self, name: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                str(ROOT / "tests" / name),
                "--mode",
                "text-free",
                "--ratio",
                "5:2",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_prompt_passes_without_warnings(self) -> None:
        result = self.run_checker("valid-text-free.txt")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Result: PASS (0 warning(s))", result.stdout)

    def test_vague_prompt_fails(self) -> None:
        result = self.run_checker("invalid-vague.txt")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("aspect ratio 5:2 is missing", result.stdout)
        self.assertIn("text-free mode requires", result.stdout)
        self.assertIn("possible vague quality words", result.stdout)

    def run_text(self, text: str, *args: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prompt.txt"
            path.write_text(text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(CHECKER), str(path), *args],
                capture_output=True, text=True, check=False,
            )

    def test_commercial_defaults_match_explicit_commercial_output(self) -> None:
        path = str(ROOT / "tests" / "valid-text-free.txt")
        default = subprocess.run([sys.executable, str(CHECKER), path], capture_output=True, text=True)
        explicit = subprocess.run(
            [sys.executable, str(CHECKER), path, "--scene", "commercial", "--mode", "text-free", "--ratio", "5:2"],
            capture_output=True, text=True,
        )
        self.assertEqual(default.returncode, 0, default.stdout)
        self.assertEqual(default.stdout, explicit.stdout)
        self.assertTrue(default.stdout.startswith("Dunhuang commercial prompt check\n"))
        self.assertNotIn("heuristic", default.stdout)

    def test_commercial_exact_text_and_missing_verbatim(self) -> None:
        base = (ROOT / "tests" / "valid-text-free.txt").read_text(encoding="utf-8").replace(
            "no text, letters, numbers", "no subtitle or extra copy"
        )
        result = self.run_text(base + '\nText (verbatim): "敦煌视觉"', "--mode", "exact-text")
        self.assertEqual(result.returncode, 0, result.stdout)
        missing = self.run_text(base, "--mode", "exact-text")
        self.assertEqual(missing.returncode, 1)
        self.assertIn("exact-text mode requires quoted verbatim copy", missing.stdout)

    def test_commercial_placeholder_free_remains_compatible(self) -> None:
        base = (ROOT / "tests" / "valid-text-free.txt").read_text(encoding="utf-8").replace("no text", "no empty title area")
        result = self.run_text(base, "--mode", "placeholder-free")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Mode: placeholder-free", result.stdout)

    def test_apsara_flags_are_not_silently_used_in_commercial_mode(self) -> None:
        for flag in ("--archery-requested", "--reference-photo"):
            with self.subTest(flag=flag):
                result = self.run_text("", flag)
                self.assertEqual(result.returncode, 2)
                self.assertIn("require --scene apsara", result.stderr)


NATURAL_EN = """Dunhuang apsara portrait, exact 3:4.
One apsara in a natural graceful flying dance pose, wearing traditional flowing attire.
Ribbons attach at the shoulders and waist with continuous paths and clear overlap/occlusion.
Mineral-pigment mural palette: cinnabar, malachite, lapis and ochre.
No bows, arrows or archery. No text, labels or logos.
"""
NATURAL_ZH = """敦煌飞天人物，3:4画幅，自然飞舞姿态，传统服饰。
飘带连接肩部和腰部，路径连续，明确前后遮挡关系。
敦煌壁画色彩：朱砂、石绿、石青、赭石。
不要弓箭或射箭动作。无文字、无标签和标识。
"""
ARCHERY_EN = """Dunhuang apsara, 3:4, traditional attire, aiming a bow.
Exactly one continuous bow body joins grip, limbs and tips.
Exactly one bowstring is connected to both bow tips.
The single string forms a drawn V with two legs meeting at the nock.
The arrow is nocked on the string and aligned with the arrow rest/support.
The bow hand grips the bow.
The draw hand pulls the string at the nock to a stable anchor point.
Use a coherent pull and aiming direction.
Ribbons attach at the shoulders; clear ribbon overlap/occlusion.
Mineral-pigment mural colors: cinnabar, malachite and lapis.
No detached bowstring, duplicate arrows, extra hands or text. No text.
"""
ARCHERY_ZH = """敦煌飞天人物拉弓瞄准，3:4画幅，传统服饰。
一张连续完整的弓体连接握把和上下弓梢。
一根弓弦连接弓体上下两端；弓弦拉成V形，两段属于同一根弓弦。
箭尾搭在弓弦上，箭矢对齐箭托。
持弓手握住弓；拉弦手拉动弓弦和箭尾到脸颊锚点。
拉弦方向和瞄准方向一致。
飘带连接肩部，路径连续，有明确遮挡关系。
矿物壁画色彩：朱砂、石绿和石青。禁止重复弓弦。无文字。
"""
PHOTO_EN = NATURAL_EN.replace("exact 3:4", "preserve original 4:5 aspect ratio").replace(
    "in a natural graceful flying dance pose", "from the uploaded reference photo"
) + "Preserve identity, facial features, hairstyle, original pose and composition.\n"


class ApsaraPromptCheckerTests(unittest.TestCase):
    run_text = PromptCheckerTests.run_text
    def apsara(self, text: str, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run_text(text, "--scene", "apsara", *args)

    def assert_pass(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("heuristic prompt quality only", result.stdout)
        self.assertIn("generated images require separate visual acceptance", result.stdout)

    def test_natural_bilingual_prompts_pass_without_archery_authorization(self) -> None:
        for text in (NATURAL_EN, NATURAL_ZH):
            with self.subTest(text=text):
                result = self.apsara(text)
                self.assert_pass(result)
                self.assertIn("Ratio: 3:4", result.stdout)
                self.assertIn("Archery requested: False", result.stdout)

    def test_subject_attire_ribbon_and_palette_are_independently_required(self) -> None:
        replacements = (
            ("apsara", "person", "apsara subject"),
            ("natural graceful flying dance pose", "standing pose", "natural flying pose"),
            ("traditional flowing attire", "modern clothing", "traditional attire"),
            ("attach at the shoulders and waist", "float", "ribbon attachment"),
            ("clear overlap/occlusion", "attractive colors", "ribbon overlap/occlusion"),
            ("Mineral-pigment mural palette: cinnabar, malachite, lapis and ochre.", "Blue and red.", "mural/mineral palette"),
        )
        for old, new, expected in replacements:
            with self.subTest(expected=expected):
                result = self.apsara(NATURAL_EN.replace(old, new))
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(expected, result.stdout)

    def test_missing_and_partial_archery_exclusions_fail(self) -> None:
        for ban in ("", "No bows or arrows.", "No duplicate bows, arrows or archery."):
            with self.subTest(ban=ban):
                result = self.apsara(NATURAL_EN.replace("No bows, arrows or archery.", ban))
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("default apsara mode requires an explicit ban", result.stdout)

    def test_common_negative_lists_pass(self) -> None:
        for ban in (
            "Without bows, arrows or archery.",
            "Avoid bows, arrows and archery.",
            "Do not add bows, arrows or archery.",
            "Forbidden: bows, arrows and archery.",
            "Bows, arrows and archery are forbidden.",
            "禁止弓箭、拉弓和射箭。",
            "弓箭和射箭动作禁止出现。",
        ):
            with self.subTest(ban=ban):
                self.assert_pass(self.apsara(NATURAL_EN.replace("No bows, arrows or archery.", ban)))

    def test_negation_does_not_leak_into_new_affirmative_sentences(self) -> None:
        for positive in (
            "An apsara holds a bow.",
            "The person carries an arrow.",
            "飞天手持弓箭。",
            "飞天正在射箭。",
        ):
            with self.subTest(positive=positive):
                result = self.apsara(NATURAL_EN + positive)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("affirmative bow/arrow/archery instruction", result.stdout)

    def test_contrast_and_new_action_end_negative_scope(self) -> None:
        for constraint in (
            "No bows, arrows or archery, but the apsara holds a bow.",
            "No bows, arrows or archery, she carries an arrow.",
            "不要弓箭或射箭动作，但是飞天手持弓。",
        ):
            with self.subTest(constraint=constraint):
                result = self.apsara(NATURAL_EN.replace("No bows, arrows or archery.", constraint))
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("affirmative bow/arrow/archery instruction", result.stdout)

    def test_archery_flag_does_not_infer_authorization_from_keywords(self) -> None:
        result = self.apsara(ARCHERY_EN)
        self.assertEqual(result.returncode, 1)
        self.assertIn("--archery-requested", result.stdout)
        empty_scene = self.apsara(NATURAL_EN, "--archery-requested")
        self.assertEqual(empty_scene.returncode, 1)
        self.assertIn("requires an affirmative archery scene", empty_scene.stdout)

    def test_archery_bilingual_connected_string_and_legitimate_v_pass(self) -> None:
        for text in (ARCHERY_EN, ARCHERY_ZH):
            with self.subTest(text=text):
                self.assert_pass(self.apsara(text, "--archery-requested"))

    def test_each_archery_contact_is_checked(self) -> None:
        for line, expected in (
            ("Exactly one continuous bow body joins grip, limbs and tips.", "one continuous bow body"),
            ("Exactly one bowstring is connected to both bow tips.", "bowstring connected to both bow tips"),
            ("The arrow is nocked on the string and aligned with the arrow rest/support.", "arrow nocked"),
            ("The bow hand grips the bow.", "bow hand gripping"),
            ("The draw hand pulls the string at the nock to a stable anchor point.", "draw hand"),
            ("Use a coherent pull and aiming direction.", "coherent pull"),
        ):
            with self.subTest(expected=expected):
                result = self.apsara(ARCHERY_EN.replace(line, ""), "--archery-requested")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("archery requires " + expected, result.stdout)

    def test_one_string_is_required_and_arrow_must_have_support(self) -> None:
        no_single = ARCHERY_EN.replace("Exactly one bowstring", "A bowstring").replace("The single string", "The string")
        result = self.apsara(no_single, "--archery-requested")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("archery requires one bowstring", result.stdout)
        unsupported = ARCHERY_EN.replace(" and aligned with the arrow rest/support", "; no arrow touching the bow")
        result = self.apsara(unsupported, "--archery-requested")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("archery requires arrow aligned with a rest/support", result.stdout)

    def test_positive_geometry_contradictions_fail_even_with_coverage(self) -> None:
        for extra in (
            "Use two bowstrings.", "Use a detached bowstring.",
            "Use a floating arrow.", "重复弓弦。", "弓体分离。", "箭矢悬空。",
        ):
            with self.subTest(extra=extra):
                result = self.apsara(ARCHERY_EN + extra, "--archery-requested")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("archery prompt contains contradictory", result.stdout)

    def test_negated_contacts_do_not_satisfy_archery_requirements(self) -> None:
        for old, new, expected in (
            ("The bow hand grips the bow", "The bow hand must not grip the bow", "bow hand gripping"),
            ("The arrow is nocked", "The arrow is not nocked", "arrow nocked"),
            ("箭尾搭在弓弦上", "箭尾没有搭在弓弦上", "arrow nocked"),
        ):
            with self.subTest(new=new):
                source = ARCHERY_ZH if "箭尾" in old else ARCHERY_EN
                result = self.apsara(source.replace(old, new), "--archery-requested")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("archery requires " + expected, result.stdout)
        self.assert_pass(self.apsara(ARCHERY_ZH + "弓弦不得与弓体分离。", "--archery-requested"))

    def test_photo_preserves_identity_pose_and_original_ratio_without_forced_flight(self) -> None:
        result = self.apsara(PHOTO_EN, "--reference-photo", "--ratio", "4:5")
        self.assert_pass(result)
        self.assertNotIn("natural flying pose", result.stdout)
        original = PHOTO_EN.replace("original 4:5 aspect ratio", "original aspect ratio")
        self.assert_pass(self.apsara(original, "--reference-photo", "--ratio", "original"))

    def test_photo_preservation_is_required_per_attribute(self) -> None:
        for target in ("identity", "facial features", "hairstyle", "original pose", "composition"):
            with self.subTest(target=target):
                result = self.apsara(PHOTO_EN.replace(target, "attribute"), "--reference-photo", "--ratio", "4:5")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("reference photo requires", result.stdout)

    def test_photo_explicit_scoped_override_is_allowed(self) -> None:
        changed = PHOTO_EN.replace("original pose", "expression") + "Explicit user-requested override: change only the pose to a standing gesture."
        self.assert_pass(self.apsara(changed, "--reference-photo", "--ratio", "4:5"))
        changed = changed.replace("Explicit user-requested override: ", "")
        result = self.apsara(changed, "--reference-photo", "--ratio", "4:5")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("override of pose", result.stdout)

    def test_photo_unscoped_change_cannot_borrow_preservation_from_a_list(self) -> None:
        photo = PHOTO_EN.replace("hairstyle, original pose", "original pose") + "Preserve identity, change hairstyle."
        result = self.apsara(photo, "--reference-photo", "--ratio", "4:5")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("override of hairstyle", result.stdout)

    def test_photo_chinese_preservation_and_no_added_archery(self) -> None:
        photo = NATURAL_ZH.replace("自然飞舞姿态", "照片中原有姿态") + "保留人物身份、面部特征、发型、动作和构图。"
        self.assert_pass(self.apsara(photo, "--reference-photo"))
        self.assert_pass(self.apsara(PHOTO_EN.replace("No bows, arrows or archery", "No bows, arrows or archery added"), "--reference-photo", "--ratio", "4:5"))

    def test_photo_existing_archery_is_preserved_without_authorizing_a_new_scene(self) -> None:
        en = PHOTO_EN.replace("No bows, arrows or archery", "No bows, arrows or archery added")
        zh = NATURAL_ZH + "保留人物身份、面部特征、发型、原有动作和构图。"
        zh = zh.replace("不要弓箭或射箭动作", "禁止新增弓箭或射箭动作")
        for text, invariant, flags in (
            (en, "Preserve the reference's existing bow, arrow and original archery pose.", ("--ratio", "4:5")),
            (zh, "保留原图中的弓箭和原有拉弓瞄准姿态。", ()),
        ):
            with self.subTest(invariant=invariant):
                result = self.apsara(text + invariant, "--reference-photo", *flags)
                self.assert_pass(result)
                self.assertIn("text cannot verify source contents", result.stdout)
                self.assertNotIn("archery requires arrow nocked", result.stdout)
                self.assertIn("Archery requested: False", result.stdout)

    def test_photo_preservation_does_not_authorize_drawing_and_aiming(self) -> None:
        en = PHOTO_EN.replace("No bows, arrows or archery", "No bows, arrows or archery added")
        zh = NATURAL_ZH.replace("不要弓箭或射箭动作", "禁止新增弓箭或射箭动作")
        zh += "保留人物身份、面部特征、发型、原有动作和构图。"
        for text, added, flags in (
            (en, "Preserve the original bow; draw it and aim.", ("--ratio", "4:5")),
            (en, "Preserve the original bow and aim toward the left.", ("--ratio", "4:5")),
            (zh, "保留原图中的弓箭；拉弓并瞄准。", ()),
            (zh, "保留原图中的弓箭并瞄准左方。", ()),
        ):
            with self.subTest(added=added):
                result = self.apsara(text + added, "--reference-photo", *flags)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("affirmative bow/arrow/archery instruction", result.stdout)

    def test_photo_original_archery_exception_requires_scoped_source_and_no_add_policy(self) -> None:
        for text in (
            PHOTO_EN + "Preserve the original bow.",
            PHOTO_EN.replace("No bows, arrows or archery", "No bows, arrows or archery added") + "Preserve a bow.",
            PHOTO_EN.replace("No bows, arrows or archery", "No bows, arrows or archery added") + "Add a bow from the reference.",
        ):
            with self.subTest(text=text):
                result = self.apsara(text, "--reference-photo", "--ratio", "4:5")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("affirmative bow/arrow/archery instruction", result.stdout)

    def test_photo_source_description_and_unchanged_contacts_use_preservation_context(self) -> None:
        photo = (ROOT / "tests" / "reference-existing-bow.txt").read_text(encoding="utf-8")
        result = self.apsara(photo, "--reference-photo", "--ratio", "original")
        self.assert_pass(result)
        self.assertIn("text cannot verify source contents", result.stdout)
        self.assertNotIn("archery requires", result.stdout)
        no_context = photo.replace("existing bow and every original prop", "the original clothing")
        result = self.apsara(no_context, "--reference-photo", "--ratio", "original")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("affirmative bow/arrow/archery instruction", result.stdout)

    def test_original_prop_context_cannot_launder_new_draw_aim_or_extra_bow(self) -> None:
        photo = (ROOT / "tests" / "reference-existing-bow.txt").read_text(encoding="utf-8")
        for added in (
            "Draw it and aim.",
            "Keep the bow's exact position, orientation and visible hand contacts and aim toward the left.",
            "No additional props and draw it and aim.",
            "Add a new bow from the reference.",
            "无新增道具并拉弓瞄准。",
        ):
            with self.subTest(added=added):
                result = self.apsara(photo + added, "--reference-photo", "--ratio", "original")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("affirmative bow/arrow/archery instruction", result.stdout)

    def test_apsara_ratio_and_text_modes(self) -> None:
        wrong_ratio = self.apsara(NATURAL_EN.replace("3:4", "13:40"))
        self.assertEqual(wrong_ratio.returncode, 1)
        self.assertIn("aspect ratio 3:4 is missing", wrong_ratio.stdout)
        missing_text = self.apsara(NATURAL_EN.replace("No text, labels or logos.", ""))
        self.assertEqual(missing_text.returncode, 1)
        self.assertIn("text-free mode requires", missing_text.stdout)
        exact = NATURAL_EN.replace("No text, labels or logos.", 'Text (verbatim): "飞天". No extra copy, labels or logos.')
        self.assert_pass(self.apsara(exact, "--mode", "exact-text"))
        self.assert_pass(self.apsara(NATURAL_EN + "No empty text boxes.", "--mode", "placeholder-free"))
        no_placeholder = self.apsara(NATURAL_EN, "--mode", "placeholder-free")
        self.assertEqual(no_placeholder.returncode, 1)
        self.assertIn("placeholder-free apsara mode requires", no_placeholder.stdout)


if __name__ == "__main__":
    unittest.main()
