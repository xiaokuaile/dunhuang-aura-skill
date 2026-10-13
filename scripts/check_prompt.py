#!/usr/bin/env python3
"""Heuristic prompt checks; never substitute for inspection of a generated image."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


STYLE_GROUPS = {
    "palette": (
        "charcoal",
        "cave black",
        "炭黑",
        "cinnabar",
        "朱砂",
        "malachite",
        "石绿",
        "lapis",
        "石青",
        "ochre",
        "赭石",
        "mineral",
        "矿物",
    ),
    "material": (
        "rock",
        "stone",
        "mural",
        "plaster",
        "ceramic",
        "glass",
        "岩",
        "石",
        "壁画",
        "灰泥",
        "陶瓷",
        "玻璃",
    ),
    "composition": (
        "composition",
        "foreground",
        "middle",
        "background",
        "left",
        "right",
        "构图",
        "前景",
        "中景",
        "背景",
        "左",
        "右",
    ),
    "lighting": (
        "light",
        "shadow",
        "reflection",
        "rim light",
        "光",
        "阴影",
        "反射",
        "倒影",
    ),
    "constraints": (
        "constraints",
        "avoid",
        "do not",
        "no ",
        "不要",
        "禁止",
        "避免",
    ),
}

TEXT_FREE_TERMS = (
    "no text",
    "no letters",
    "no numbers",
    "no typography",
    "无文字",
    "不要文字",
    "无字",
    "禁止文字",
)

SLOP_TERMS = {
    "AI purple": ("ai purple", "purple gradient", "紫色渐变", "紫色光晕"),
    "generic AI symbols": (
        "robot head",
        "ai brain",
        "circuit brain",
        "机器人头",
        "ai大脑",
        "电路大脑",
    ),
    "vague quality words": ("make it premium", "more premium", "高级一点", "更高级"),
}


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def check_ratio(text: str, ratio: str) -> bool:
    compact = re.sub(r"\s+", "", text)
    alternatives = {
        ratio.lower(),
        ratio.lower().replace(":", "x"),
        ratio.lower().replace(":", "："),
    }
    return any(item in compact for item in alternatives)


def has_unnegated_term(text: str, term: str) -> bool:
    """Return True when a term appears without a nearby negative instruction."""
    start = 0
    negatives = ("no ", "avoid", "do not", "without", "不要", "避免", "禁止", "无")
    while True:
        index = text.find(term, start)
        if index < 0:
            return False
        prefix = text[max(0, index - 48) : index]
        if not any(marker in prefix for marker in negatives):
            return True
        start = index + len(term)


def clauses(text: str) -> list[str]:
    """Keep a negative list together, but stop its scope at a new sentence/contrast."""
    return re.split(r"[.!?。！？;；\n]+|\b(?:but|however|yet|instead|while)\b|但是|但", text)


NEGATIVE = re.compile(
    r"\b(?:no|without|avoid|exclude|excluding|forbidden|forbid|never|do not|don't|must not|not)\b"
    r"|不要|不得|不许|禁止|避免|排除|不添加|不加入|不新增|不引入|不使用|不用|没有|无"
)
POSITIVE_ACTION = re.compile(
    r"\b(?:holds?|holding|carries|carrying|wields?|wielding|shoots?|shooting|draws?|drawing|"
    r"uses?|using|include|add|with|has)\b|手持|持有|握住|拉开|正在|添加|加入|拿着|握着"
)


def is_negated(clause: str, match: re.Match[str]) -> bool:
    """Recognize common EN/ZH exclusions, not general natural-language semantics."""
    if any(marker.group() != "无" for marker in NEGATIVE.finditer(match.group())):
        # Relationship patterns can contain negation between their endpoints,
        # e.g. "the bow hand must not grip the bow" or "弓弦不得与弓体分离".
        return True
    before = clause[: match.start()]
    negatives = list(NEGATIVE.finditer(before))
    if negatives:
        tail = before[negatives[-1].end() :]
        # A comma can continue a forbidden list or introduce an affirmative action.
        # "No bows, arrows or archery" is one list; "no bows, she holds an arrow"
        # introduces a new action and must not inherit the earlier exclusion.
        after_comma = re.split(r"[,，]", tail)[-1] if re.search(r"[,，]", tail) else ""
        new_action = re.search(
            r"\band\s+(?:draw|aim|shoot|add|create|introduce)\b|(?:并|然后|再)(?:拉弓|瞄准|射箭|添加|新增)",
            tail + match.group(),
        )
        if not POSITIVE_ACTION.search(after_comma) and not new_action:
            if not re.search(r"(?:do not|don't|not|不要|不得)\s*(?:avoid|exclude|避免|排除)", before):
                return True
    after = clause[match.end() :]
    return bool(
        re.search(r"\b(?:are|is|must be)\s+(?:forbidden|prohibited|excluded|not allowed)\b", after)
        or re.search(r"(?:禁止出现|不得出现|不允许出现|禁止生成|禁止添加|不出现)", after)
    )


def positive_clauses(text: str, pattern: str) -> list[str]:
    return [
        clause
        for clause in clauses(text)
        if any(not is_negated(clause, match) for match in re.finditer(pattern, clause))
    ]


def has_positive(text: str, pattern: str) -> bool:
    return bool(positive_clauses(text, pattern))


ARCHERY_TERMS = {
    "bows": r"\bbows?\b|弓箭|弓体|弓身|弓",
    "arrows": r"\barrows?\b|弓箭|箭矢|箭",
    "archery": r"\b(?:archery|archers?)\b|\bshoot(?:ing)?\s+(?:an?\s+)?arrow|\bshooting\s+pose\b|射箭|拉弓|弯弓",
}
ARCHERY_OBJECTS = "|".join(ARCHERY_TERMS.values()) + r"|\bbowstrings?\b|弓弦|搭箭"


def explicit_archery_ban(text: str, pattern: str) -> bool:
    for clause in clauses(text):
        for match in re.finditer(pattern, clause):
            if is_negated(clause, match):
                # "No duplicate bows" does not prohibit a regular bow.
                prefix = clause[: match.start()]
                negative = list(NEGATIVE.finditer(prefix))
                scope = prefix[negative[-1].end() :] if negative else ""
                if not re.search(r"\b(?:extra|duplicate|additional|detached|broken)\b|重复|多余|分离|断裂", scope):
                    return True
    return False


def explicit_no_add_archery_ban(text: str, pattern: str) -> bool:
    """Photo edits can prohibit new props while retaining original ones."""
    for clause in clauses(text):
        for match in re.finditer(pattern, clause):
            if not is_negated(clause, match):
                continue
            negatives = list(NEGATIVE.finditer(clause[: match.start()]))
            if not negatives:
                continue
            scope = clause[negatives[-1].start() : match.start()]
            suffix = clause[match.end() :]
            if re.search(r"\b(?:new|additional|add|added|adding|introduce)\b|新增|添加|加入|引入", scope):
                return True
            if re.search(r"\b(?:added|introduced)\b|新增|添加|加入", suffix):
                return True
    return False


ARCHERY_ACTIONS = r"\bdraw(?:ing)?\s+(?:it|the bow|a bow)\b|\b(?:aim|aiming|shoot|shooting)\b|拉弓|瞄准|射箭|拉开(?:它|弓)"


def preserves_existing_archery(
    clause: str, match: re.Match[str], *, action: bool = False, source_context: bool = False
) -> bool:
    """A scoped original-content invariant is not a request for a new action."""
    preserve = re.search(r"\b(?:preserve|keep|retain)\b|保留|保持", clause[: match.start()])
    source = re.search(r"\b(?:original|existing|reference|source)\b|原图|原有|已有|参考照片|参考图", clause)
    if has_positive(clause, r"\b(?:add|introduce|invent|create|change|replace|alter)\b|添加|新增|引入|改成|改变|更改|替换"):
        return False
    if not preserve or not source:
        if not source_context or action:
            return False
        source_description = (
            source
            and re.search(r"\b(?:edit target|source photo|reference photo)\b|编辑目标|参考照片|原图", clause)
            and re.search(r"\b(?:already|existing)\b|已经|原有|已有", clause[: match.start()])
        )
        unchanged_relation = (
            preserve
            and re.search(r"\b(?:the|this)\s+(?:bow|arrow|bowstring)\b|(?:弓|箭|弓弦)的", clause)
            and re.search(r"\b(?:exact|same|unchanged)\b|准确|原样|不变", clause)
            and re.search(r"\b(?:position|orientation|contacts?|shape)\b|位置|朝向|方向|接触|形状", clause)
        )
        return bool(source_description or unchanged_relation)
    if action:
        # "Preserve the original aiming pose" retains a pose. "Preserve the
        # original bow and aim left" introduces an action after that invariant.
        return bool(re.search(r"\b(?:pose|action|gesture)\b|动作|姿态|姿势", clause[match.end() : match.end() + 35]))
    return True


def check_apsara_ratio(text: str, ratio: str) -> bool:
    if ratio == "original":
        return bool(re.search(r"original (?:aspect )?ratio|原始(?:画幅|宽高比|比例)|保留[^。\n]{0,20}(?:画幅|宽高比)", text))
    compact = re.sub(r"\s+", "", text)
    escaped = re.escape(ratio.casefold()).replace(":", "[:x：]")
    return bool(re.search(r"(?<!\d)" + escaped + r"(?!\d)", compact))


PHOTO_TARGETS = {
    "identity": r"\bidentity\b|身份|同一人物|本人",
    "facial features": r"\bfacial (?:features|traits)\b|\bface\b|面部特征|五官|脸部特征|脸型",
    "hairstyle": r"\bhairstyle\b|\bhair style\b|发型",
    "pose": r"\b(?:original )?(?:pose|gesture|action)\b|动作|姿态|姿势",
    "composition": r"\bcomposition\b|\bframing\b|构图|取景",
}


def photo_invariant_present(text: str, target: str) -> bool:
    for clause in clauses(text):
        target_match = re.search(target, clause)
        if not target_match:
            continue
        # Preserve/keep may govern a list of reference attributes.
        preservation = re.search(r"\b(?:preserve|keep|retain|unchanged)\b|保留|保持|不改变|不改动", clause)
        change_before_target = re.search(r"\b(?:change|replace|alter)\b|改变|更改|替换", clause[: target_match.start()])
        if (
            preservation
            and not re.search(r"\b(?:do not|don't|never)\s+(?:preserve|keep|retain)\b|不要保留|不保留", clause)
            and not (change_before_target and change_before_target.start() > preservation.start())
        ):
            return True
        # Overrides must name both the target and explicit user intent.
        explicit_user = re.search(
            r"explicit(?:ly)?[^。\n]{0,40}(?:user|request)|user[^。\n]{0,30}request"
            r"|用户[^。\n]{0,20}明确|明确[^。\n]{0,20}(?:用户|要求)", clause
        )
        change = re.search(r"\b(?:change|replace|alter|override)\b|改变|更改|替换|覆盖", clause)
        if explicit_user and change:
            return True
    return False


def check_apsara(
    text: str, args: argparse.Namespace, errors: list[str], warnings: list[str], passes: list[str]
) -> None:
    """Check explicit prompt coverage. Counts, geometry and identity remain visual QA."""
    def require(ok: bool, success: str, failure: str) -> None:
        (passes if ok else errors).append(success if ok else failure)

    require(
        has_positive(text, r"\bapsaras?\b|飞天"),
        "apsara subject is explicit", "apsara subject is missing or excluded",
    )
    if not args.reference_photo and not args.archery_requested:
        require(
            has_positive(text, r"\b(?:natural|graceful|gently|floating|flowing)[^.;\n]{0,55}(?:flight|flying|float|dance)|自然[^。\n]{0,20}(?:飞舞|飞行|飘飞)|轻盈[^。\n]{0,20}(?:飞舞|飞行|飘飞)|自然飞天"),
            "natural flying pose is explicit", "natural flying pose guidance is missing",
        )
    require(
        has_positive(text, r"\btraditional[^.;\n]{0,45}(?:attire|clothing|robes|costume|dress)|(?:传统|敦煌|古典|古代)[^。\n]{0,20}(?:服饰|衣裙|衣袍|裙装|天衣)"),
        "traditional attire is explicit", "traditional attire guidance is missing",
    )
    require(
        has_positive(text, r"\b(?:mineral|mural|cinnabar|malachite|lapis|ochre)\b|矿物|壁画色|朱砂|石绿|石青|赭石"),
        "mural/mineral palette guidance is present", "mural/mineral palette guidance is missing",
    )
    ribbon_clauses = positive_clauses(text, r"\b(?:ribbons?|streamers?)\b|飘带|披帛")
    require(bool(ribbon_clauses), "ribbons are explicit", "ribbon guidance is missing")
    require(
        bool(ribbon_clauses) and has_positive(text, r"\b(?:attach\w*|anchor\w*)\b|连接|系于|系在|连接点|附着|固定|起点"),
        "ribbon attachment guidance is present", "ribbon attachment guidance is missing",
    )
    require(
        has_positive(text, r"\b(?:occlusion\w*|overlap\w*|layer order)\b|遮挡|层次关系|前后关系|交叠|交错"),
        "ribbon overlap/occlusion guidance is present", "ribbon overlap/occlusion guidance is missing",
    )

    if args.reference_photo:
        for label, target in PHOTO_TARGETS.items():
            require(
                photo_invariant_present(text, target),
                f"reference {label} is preserved or explicitly overridden",
                f"reference photo requires preservation or a scoped user-requested override of {label}",
            )

    if not args.archery_requested:
        for label, pattern in ARCHERY_TERMS.items():
            require(
                explicit_archery_ban(text, pattern)
                or (args.reference_photo and explicit_no_add_archery_ban(text, pattern)),
                f"no unrequested {label} constraint is explicit",
                f"default apsara mode requires an explicit ban on {label}",
            )
        photo_no_add = args.reference_photo and all(
            explicit_no_add_archery_ban(text, pattern) for pattern in ARCHERY_TERMS.values()
        )
        source_context = photo_no_add and any(
            not is_negated(clause, match) and preserves_existing_archery(clause, match)
            for clause in clauses(text)
            for match in re.finditer(ARCHERY_OBJECTS, clause)
        )
        preserved_archery = False
        unrequested_archery = False
        for clause in clauses(text):
            for match in re.finditer(ARCHERY_OBJECTS, clause):
                if is_negated(clause, match):
                    continue
                if photo_no_add and preserves_existing_archery(clause, match, source_context=source_context):
                    preserved_archery = True
                else:
                    unrequested_archery = True
        if preserved_archery:
            for clause in clauses(text):
                for match in re.finditer(ARCHERY_ACTIONS, clause):
                    if not is_negated(clause, match) and not preserves_existing_archery(clause, match, action=True):
                        unrequested_archery = True
            warnings.append(
                "reference-photo preserves existing archery; text cannot verify source contents; "
                "compare the original pose and props with the source image manually"
            )
        require(
            not unrequested_archery,
            "no new or unrequested archery instruction is present",
            "affirmative bow/arrow/archery instruction requires explicit user intent and --archery-requested",
        )
        return

    require(
        has_positive(text, ARCHERY_OBJECTS),
        "archery scene is explicit (user intent attested by flag)",
        "--archery-requested requires an affirmative archery scene",
    )
    checks = {
        "one continuous bow body": r"(?:\b(?:one|single)\b[^.;\n]{0,30}\b(?:continuous|unbroken)\b[^.;\n]{0,20}\bbow(?: body)?\b|\bbow\b[^.;\n]{0,20}\bone continuous body\b|(?:一[张把]|唯一|单[张把]|一条)[^。\n]{0,20}(?:连续|完整)[^。\n]{0,10}弓(?:体|身)?)",
        "one bowstring": r"\b(?:one|single)\s+(?:continuous\s+)?(?:bowstring|string)\b|(?:一根|单根|唯一)[^。\n]{0,10}弓弦",
        "bowstring connected to both bow tips": r"(?:\b(?:bowstring|string)\b[^.;\n]{0,55}\b(?:connect\w*|attach\w*)\b[^.;\n]{0,35}(?:both|two|upper and lower)[^.;\n]{0,15}\btips?\b|弓弦[^。\n]{0,25}(?:连接|系在|固定)[^。\n]{0,20}(?:两端|上下两端|两弓梢))",
        "arrow nocked on the bowstring": r"(?:\barrow\b[^.;\n]{0,40}\bnocked\b[^.;\n]{0,20}\b(?:string|bowstring)\b|\bnocked arrow\b[^.;\n]{0,30}\b(?:string|bowstring)\b|箭(?:尾|矢)?[^。\n]{0,20}(?:搭在|扣在|卡在)[^。\n]{0,10}弦|搭箭点[^。\n]{0,15}弦)",
        "arrow aligned with a rest/support": r"(?:\barrow\b[^.;\n]{0,55}(?:\balign\w*\b|\brests? on\b|\bsupported\b)[^.;\n]{0,40}(?:arrow rest|shelf|support)|箭(?:矢)?[^。\n]{0,30}(?:对齐|支撑|搭在|搁在)[^。\n]{0,15}(?:箭台|箭托|托点|支点))",
        "bow hand gripping the bow": r"(?:\bbow hand\b[^.;\n]{0,25}\b(?:grips?|holds?|gripping|holding)\b[^.;\n]{0,15}\bbow\b|(?:持弓手|握弓手|扶弓手)[^。\n]{0,15}(?:握|持)[^。\n]{0,10}弓)",
        "draw hand at the nock/string and a stable anchor": r"(?:\bdraw(?:ing)? hand\b[^.;\n]{0,25}\b(?:pull\w*|draw\w*)\b[^.;\n]{0,40}\b(?:nock|string|bowstring)\b[^.;\n]{0,40}\banchor\b|(?:拉弦手|拉弓手)[^。\n]{0,15}(?:拉|牵)[^。\n]{0,15}(?:搭箭点|箭尾|弓弦)[^。\n]{0,20}(?:锚点|脸颊|下颌|固定点))",
        "coherent pull and aiming direction": r"(?:\b(?:coherent|consistent|aligned)\b[^.;\n]{0,35}\b(?:pull|draw)\w*\b[^.;\n]{0,30}\b(?:aim|direction|line)\w*\b|(?:拉弦|拉力|牵拉)[^。\n]{0,20}(?:瞄准|箭轴|射向)[^。\n]{0,15}(?:一致|连贯|对齐)|(?:一致|连贯)[^。\n]{0,15}(?:拉弦|拉力)[^。\n]{0,20}(?:瞄准|方向))",
    }
    for label, pattern in checks.items():
        require(has_positive(text, pattern), f"archery: {label} guidance is present", f"archery requires {label} guidance")
    contradictions = {
        "multiple bowstrings": r"\b(?:two|three|multiple|duplicate|second)\s+(?:bowstrings?|strings?)\b|(?:两根|三根|多根|重复|第二根)弓弦",
        "disconnected bow structure": r"\b(?:detached|floating|disconnected)\s+(?:bowstring|bow body|bow grip)\b|(?:弓弦|弓体|弓身)[^。\n]{0,10}(?:分离|断裂|脱离)|(?:分离|断裂|脱离)[^。\n]{0,10}(?:弓弦|弓体|弓身)",
        "unnocked/floating arrow": r"\b(?:floating|unnocked)\s+arrow\b|箭(?:矢|尾)?[^。\n]{0,12}(?:悬空|未搭在弦)",
    }
    for label, pattern in contradictions.items():
        if has_positive(text, pattern):
            errors.append(f"archery prompt contains contradictory {label} instruction")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a prompt for the dunhuang-aura skill."
    )
    parser.add_argument("prompt", type=Path, help="UTF-8 prompt text file")
    parser.add_argument(
        "--mode",
        choices=("text-free", "exact-text", "placeholder-free"),
        default="text-free",
        help="Expected text mode",
    )
    parser.add_argument("--scene", choices=("commercial", "apsara"), default="commercial", help="Prompt scene (default: commercial)")
    parser.add_argument("--ratio", help="Expected aspect ratio (default: 5:2 commercial, 3:4 apsara; 'original' for a reference photo)")
    parser.add_argument("--archery-requested", action="store_true", help="Attest that the user explicitly requested an apsara archery scene")
    parser.add_argument("--reference-photo", action="store_true", help="Check preservation of an uploaded reference person's attributes")
    args = parser.parse_args()
    if args.scene != "apsara" and (args.archery_requested or args.reference_photo):
        parser.error("--archery-requested and --reference-photo require --scene apsara")
    if args.scene == "apsara" and args.ratio == "original" and not args.reference_photo:
        parser.error("--ratio original requires --scene apsara --reference-photo")
    args.ratio = args.ratio or ("3:4" if args.scene == "apsara" else "5:2")

    if not args.prompt.is_file():
        print(f"ERROR: prompt file not found: {args.prompt}")
        return 2

    raw = args.prompt.read_text(encoding="utf-8")
    text = raw.casefold()
    errors: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []

    ratio_check = check_apsara_ratio if args.scene == "apsara" else check_ratio
    if ratio_check(text, args.ratio):
        passes.append(f"aspect ratio {args.ratio} is explicit")
    else:
        errors.append(f"aspect ratio {args.ratio} is missing")

    if args.scene == "commercial":
        for label, terms in STYLE_GROUPS.items():
            if contains_any(text, terms):
                passes.append(f"{label} guidance is present")
            else:
                errors.append(f"{label} guidance is missing")
    else:
        check_apsara(text, args, errors, warnings, passes)

    if args.mode == "text-free":
        if contains_any(text, TEXT_FREE_TERMS):
            passes.append("text-free constraint is explicit")
        else:
            errors.append(
                "text-free mode requires an explicit ban on text, letters, or numbers"
            )

        risky_sources = ("phone", "screen", "label", "poster", "seal", "手机", "屏幕", "标签", "海报", "印章")
        has_label_ban = bool(
            re.search(r"no\s+[^.\n]{0,80}(?:labels?|logos?)", text)
            or re.search(r"(?:不要|禁止|无)[^。\n]{0,30}(?:标签|标识|logo)", text)
        )
        if contains_any(text, risky_sources) and not has_label_ban:
            warnings.append(
                "objects that often generate accidental glyphs are present; also ban labels and logos"
            )

    if args.mode == "exact-text":
        if "text (verbatim)" in text or "准确文字" in text or "原文" in text:
            passes.append("exact-text instruction is present")
        else:
            errors.append("exact-text mode requires quoted verbatim copy")

    if args.scene == "apsara" and args.mode == "placeholder-free":
        if re.search(r"no (?:empty )?(?:title area|text boxes|placeholders)|无(?:空白)?(?:标题区|文字框|占位框)|不要[^。\n]{0,15}(?:标题留白|文字占位)", text):
            passes.append("placeholder-free constraint is explicit")
        else:
            errors.append("placeholder-free apsara mode requires an explicit ban on empty text/title placeholders")

    for label, terms in SLOP_TERMS.items():
        if any(has_unnegated_term(text, term) for term in terms):
            warnings.append(f"possible {label}: replace it with visible design instructions")

    if args.scene == "commercial" and not contains_any(text, ("religious", "buddha", "apsara", "宗教", "佛", "飞天")):
        warnings.append("religious-figure policy is unspecified")

    print(f"Dunhuang {args.scene} prompt check")
    print(f"File: {args.prompt}")
    print(f"Mode: {args.mode}")
    print(f"Ratio: {args.ratio}")
    if args.scene == "apsara":
        print("Scope: heuristic prompt quality only; generated images require separate visual acceptance.")
        print(f"Archery requested: {args.archery_requested}; Reference photo: {args.reference_photo}")
    print()

    for item in passes:
        print(f"PASS: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors:
        print(f"\nResult: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1

    print(f"\nResult: PASS ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
