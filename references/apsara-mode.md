# Dunhuang apsara人物 mode

Use this reference when the user requests 敦煌飞天 / flying apsaras, a Dunhuang character portrait, or an uploaded-photo transformation into that style. These are stylized creative images, not archaeological restoration or claims about a specific historical mural. Commercial-only exclusions and product-stage layouts do not apply to this mode.

## Route and preserve intent

- For a new image, default to one character in a natural, graceful flying or dance pose, traditional flowing attire, coherent ribbons, and Dunhuang mineral-pigment mural colors. Default aspect ratio: **3:4**. Honor an explicit ratio, subject count, pose, or clothing choice.
- **Do not add bows, arrows, or archery by default.** Enter a new archery scene only when the current user explicitly requests it. “Dunhuang,” “dynamic,” a previous archery image, or a reference image alone does not authorize inventing an archery action.
- For a photo transformation, inspect the supplied image first. Preserve identity, facial features, hairstyle, unrequested pose/action, composition, camera angle, crop, and original aspect ratio. Styling changes may alter clothing, palette, and materials within the requested scope; do not replace the subject with a generic face or force a flying pose or 3:4 crop.
- Record explicit overrides separately from preserved attributes. A request to change clothing does not authorize changing the face; a requested new pose does not authorize a new hairstyle or camera angle.
- Do not automatically remove existing props or change an existing archery pose in a reference. Preserving supplied content is an edit invariant, not permission to introduce new archery. Apply a current explicit instruction to remove the bow or change the pose within that scope. If simultaneous preservation and alteration instructions genuinely conflict, clarify the affected attribute before changing it.

## Character and ribbon relationships

Traditional attire may use layered skirts, fitted upper garments, flowing sleeves, and a long scarf appropriate to the requested design. Keep garment seams, sleeve openings, waist ties, and drape readable; do not describe the costume as a verified reconstruction without evidence.

Give each scarf or ribbon an identifiable attachment or resting point at the shoulders, arms, or waist. Its path must remain continuous through visible sections, with clear foreground/background overlap and plausible concealed sections. A free scarf end can float; do not attach it to arbitrary skin or make it grow out of the body. Keep ribbons, sleeves, hair strands, limbs, and accessories distinguishable. Avoid opaque loops across the face, merged fingers, ribbons posing as extra arms, and impossible passes through the torso. Floating attire is a stylized flying effect; limb anatomy and visible contact relationships still need to read clearly.

Use cinnabar, malachite green, lapis blue, ochre, and sand mineral white with restrained gold, subtle plaster grain, and softened mural edges. Give the face readable light and enough contrast for likeness. A quiet mural or cloud background should support the figure; a commercial pedestal, phone, or illuminated panel is not required.

## Archery only on explicit request

Identify the shot phase: carrying, preparing, drawing, aiming, or release. Apply the following drawn-shot relationships only when the user requests a drawn or aiming pose; do not impose a full-draw string or nocked arrow on a carrying pose or an arrow already in flight.

For a drawn traditional bow:

- One continuous bow body joins the grip to both limbs and tips; the grip is part of the bow, not a disconnected handle.
- Exactly **one bowstring** connects the two bow tips. At full draw, the pulled string forms a V with two legs meeting at the drawing point; those legs are parts of one string, not duplicate strings or decorative cords.
- The arrow nock contacts the bowstring at the drawing point. The shaft runs toward the bow across the support/rest or bow-hand grip area, with its arrowhead pointing toward the intended target. The shaft does not float beside the string or pass through the hand, arm, or bow body.
- Distinct roles: the bow hand grips the bow; the draw hand contacts the string at the nock area. Show plausible fingers, wrist positions, and a readable anchor near the face when appropriate to the requested draw. Keep the pulling direction, bow plane, arrow shaft, and aim direction coherent.
- Inspect any ribbons near the bow separately so they cannot be mistaken for additional strings. Avoid floating bows, detached strings, duplicate arrows, and a third hand. Do not claim a specific historical grip or release technique unless the user supplies it and it is supported.

## Adaptable prompt templates

Fill bracketed fields before running the checker. Each template uses text-free output; use the existing exact-text or placeholder-free policy when the user requests typography.

### New 3:4 natural flying apsara

```text
Use case: Dunhuang apsara人物 creative illustration.
Asset type: text-free character portrait, exact 3:4.
Primary request: Create one Dunhuang flying apsara in a natural graceful flying dance pose, with no text.

Subject: one 【CHARACTER DESCRIPTION】 with a readable face and coherent hands. Use traditional flowing attire with layered fabric and clearly defined sleeve openings. Relaxed open hands and a gentle curved body line convey flight; do not invent an action with equipment.
Composition: a 3:4 portrait with the figure as the primary subject; leave breathing room for hair, hands, garment hems, and ribbon ends. Separate the figure from a quiet mural-cloud background. Use a foreground ribbon arc for depth without covering the face.
Ribbons: one long flowing scarf resting around the shoulders and arms; keep identifiable attachment/resting points, a continuous path, and clear overlap/occlusion behind the torso. Separate ribbons from sleeves, hair, and limbs.
Style/materials: Dunhuang-inspired mineral-pigment mural painting with subtle weathered plaster grain and softened painted edges.
Lighting: soft directional light, a readable face, gentle shadows separating hands and fabric layers.
Palette: cinnabar red, malachite green, lapis blue, ochre, sand mineral white, and restrained gold accents.
Constraints: no bows, arrows, or archery; no extra limbs, merged fingers, disconnected ribbons, or cloth passing through the body. No text, letters, numbers, labels, logos, watermarks, or accidental glyphs.
```

### Uploaded-photo style transformation

Replace `【ORIGINAL_RATIO】` with the inspected source ratio. Replace the default archery sentence when the source already contains props that must be preserved; name those props as invariants and prohibit adding new ones. Do not add unrelated natural-flight instructions.

```text
Edit target: the supplied reference photo.
Use case: Dunhuang apsara人物 style transformation.
Asset type: text-free styled portrait, preserve original 【ORIGINAL_RATIO】 aspect ratio.
Primary change: translate the requested clothing, palette, and surface treatment into a Dunhuang apsara mural style, with no text.

Preserve unchanged: the person's identity, facial features and proportions, recognizable facial expression, hairstyle and hairline, original pose and action, composition, camera angle, crop, original aspect ratio, and 【OTHER SUPPLIED INVARIANTS】.
Explicit scoped overrides: 【NONE, OR THE USER'S SPECIFIC REQUESTED CHANGES】. Every unlisted attribute remains unchanged.
Attire: apply traditional flowing attire only within the requested clothing change; follow the existing shoulders, waist, sleeves, and body pose.
Ribbons: place flowing scarf fabric with identifiable attachment/resting points; use continuous paths and clear overlap/occlusion behind the torso. Keep ribbons distinct from sleeves, hair, hands, and limbs; preserve face visibility and the original pose.
Style/materials: mineral-pigment mural painting, fine plaster grain, softened painted edges; keep the face recognizable.
Lighting and palette: preserve the source light direction while introducing cinnabar, malachite green, lapis blue, ochre, sand mineral white, and restrained gold.
Constraints: no bows, arrows, or archery added; no extra limbs or merged fingers, no ribbons passing through the body. No text, letters, numbers, labels, logos, watermarks, or accidental glyphs.
```

### Explicitly requested drawn traditional archery

Use only for an explicit request such as “生成一位拉弓瞄准的敦煌飞天人物.” Choose the target direction and hand assignment before generating.

```text
Use case: Dunhuang apsara人物 illustration; the user explicitly requests archery.
Asset type: text-free character portrait, exact 3:4.
Primary request: Create one Dunhuang flying apsara drawing and aiming a traditional bow toward 【TARGET DIRECTION】, with no text.

Subject and attire: one character in traditional flowing attire, with coherent anatomy and two distinct hands. The bow hand grips the bow grip; the draw hand contacts the string at the arrow nock and has a plausible anchor near the face. Keep the hands and face visible.
Bow: exactly one continuous bow body connects the grip to both limbs and tips. Exactly one bowstring is connected to both bow tips; the single string is drawn into a V with two legs meeting at the nock, not duplicate strings.
Arrow: exactly one arrow is nocked on the string at the drawing point and aligned with the arrow rest/support or bow-hand grip area. The arrowhead points toward the target. The draw hand pulls the string at the nock to a stable anchor point. Keep a coherent pull and aiming direction, with the bow plane and shaft aligned; no floating arrow or penetration through fingers or the bow.
Composition: exact 3:4; keep both bow tips, the string, the arrow, and both hands within the frame with clear visual separation from the background.
Ribbons: a flowing scarf has identifiable attachment/resting points, continuous paths, and clear overlap/occlusion behind the torso; keep ribbons separated from the bowstring and hands.
Style/materials: Dunhuang-inspired mineral-pigment mural painting, subtle weathered plaster grain, and softened painted edges.
Lighting: soft directional light with readable shadows around the grip, draw hand, nock, and face.
Palette: cinnabar, malachite green, lapis blue, ochre, sand mineral white, restrained gold.
Constraints: no detached bowstring, second string, disconnected bow body, duplicate arrow, extra hands, merged fingers, or cloth passing through the body. No text, letters, numbers, labels, logos, watermarks, or accidental glyphs.
```

## Generation preflight

1. Select `apsara` only for the requested character mode; preserve the existing commercial route for commercial deliverables.
2. Record whether the task is new generation or a reference edit; choose the ratio and text state from the request and source.
3. Check subject, pose, traditional attire, mural palette, continuous ribbon paths, attachment points, and clear overlaps. For photo edits, list preserved identity, face, hairstyle, pose, and composition, plus each explicit override.
4. Confirm whether archery was explicitly requested. Without that request, exclude newly added bows, arrows, and archery actions. With it, describe the actual shot phase and its required contacts before generating.
5. Run the prompt checker where useful, then inspect its warnings and any contradictions manually. A text check cannot determine the user's authorization from a keyword alone.

```bash
python scripts/check_prompt.py prompt.txt --scene apsara --mode text-free
python scripts/check_prompt.py prompt.txt --scene apsara --mode text-free --reference-photo --ratio 4:5
python scripts/check_prompt.py prompt.txt --scene apsara --mode text-free --archery-requested
```

`--scene apsara` defaults to 3:4; `--ratio` sets another requested or original-source ratio. `--reference-photo` enables preservation checks. `--archery-requested` records an explicit user request; it does not grant authorization by itself. The automated archery checks cover the drawn/aiming template above; carrying, preparation, and release phases need manual prompt preflight and phase-appropriate image inspection. For a style-only edit retaining existing archery, name the original pose/props as preserved and prohibit additions; the text checker cannot verify what is in the source photo, so inspect those invariants visually. `--mode` retains the existing `text-free`, `exact-text`, and `placeholder-free` meanings. The commercial route continues to default to 5:2.

## Real-image acceptance and regression cases

**Prompt quality checks and image acceptance are separate.** The checker is a heuristic text preflight. A pass means expected instructions were found; it does not prove likeness, anatomy, ribbon geometry, bowstring contact, or a usable image. Never report a passing prompt as a passing generated image.

Inspect an actual generated image at full resolution and thumbnail size. Check the requested ratio, face and hand readability, limb count, clothing/ribbon separation, and absence of unrequested archery. For edits, compare face, hairstyle, pose, framing, and each invariant against the source. For requested archery, zoom in on both tips, the grip, both string legs, the nock, shaft support, arrowhead, and both hands; check the phase-specific relationships above. If a visible defect blocks acceptance, make a targeted correction while preserving accepted attributes and inspect again.

| Regression case | Prompt expectation | Visible-image acceptance |
| --- | --- | --- |
| “正常敦煌飞天，3:4” | Natural flight, traditional attire, coherent ribbons, mural palette, no archery. | No bow/arrow/action introduced; coherent figure and ribbons. |
| “敦煌飞天，更有动感” after earlier archery work | Dynamic flight or dance; previous history does not select archery. | Dynamic movement without newly invented weapons. |
| Reference photo, “只改为敦煌风格” | Preserve identity, face, hairstyle, pose, composition, and original ratio. | Compare against the source; likeness and framing survive styling. |
| Reference photo, “改服装，保持脸、发型和动作” | Override clothing only; list other invariants. | Requested clothing changes with the original face, hair, and pose. |
| Reference already contains a bow, “只改画风” | Preserve supplied pose/props; do not invent an additional action. | Existing composition survives; no extra bow, arrow, or string. |
| “拉弓瞄准的飞天，3:4” | Explicit archery with connected bow body, one drawn string, nocked supported arrow, distinct hand roles. | All visible contacts and aim relationships hold together. |
| Commercial text-free 5:2 or exact-title cover | Existing commercial rules and text state still apply. | Existing commercial acceptance checklist still applies. |

Automated regression tests exercise prompt routing and checks; keep the visible-image column **pending until an actual image has been generated and inspected**. Record the prompt, tool/model if available, result image, observed defects, and acceptance decision for each real-image run. Repository changes only affect workflows that load this updated skill; they do not install it elsewhere or automatically change the image generation behavior of the current chat.
