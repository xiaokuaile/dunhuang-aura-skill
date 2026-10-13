---
name: dunhuang-aura
description: Create or edit Dunhuang mineral-pigment commercial visuals and 敦煌飞天人物 (flying apsara portraits), including identity-preserving photo stylization. Use for Dunhuang covers, product advertising, natural-flight apsaras, or explicitly requested apsara archery. Do not use for archaeological restoration, historical reconstruction, or devotional religious imagery.
---

# Dunhuang Aura

Create Dunhuang mineral-pigment imagery in either commercial mode or apsara portrait mode. Route the request before choosing templates or defaults.

## Choose the visual mode first

- **Commercial (existing default):** covers, product advertising, devices, and visual suites. Use the commercial rules below and the existing references. Exclude religious figures, including apsaras, by default in this mode.
- **Apsara portrait:** select when the user asks for 敦煌飞天, flying apsaras, or a person's photo transformed into that style. Read [Apsara mode](references/apsara-mode.md) for its templates, preflight checks, and image acceptance. New portraits default to 3:4, natural flying or dancing posture, traditional flowing attire, coherent ribbons, and Dunhuang mural colors. Do not add bows, arrows, or an archery pose by default. Enter the archery variant only when the current request explicitly asks for archery or explicitly asks to preserve existing archery; a mention in an avoid list or an earlier image is not such a request.
- **Reference-photo edit:** within apsara mode, inspect the supplied photo before writing the prompt. Preserve identity, facial features, hairstyle, pose, composition, camera angle, crop, original props, and original aspect ratio unless the user requests a specific change. Change only that scope; do not force an unchanged standing pose into flight or crop the photo to 3:4. A style-only edit preserves existing archery content without introducing a new scene; do not remove the bow or invent an additional action. Clarify only when specific preservation and alteration instructions conflict. Read the photo template in [Apsara mode](references/apsara-mode.md).

The apsara request authorizes the stylized figure. Do not import the commercial ban on flying apsaras, product pedestals, 5:2 side-balance, or charcoal-dominant palette into this mode. Stylized portraits do not claim reconstruction of a particular cave, dynasty, or mural; requests for historical accuracy need specific sources and a separate workflow.

The shared text policy, image-tool workflow, and output behavior below apply to both modes. Sections labelled commercial apply only to commercial mode. Neither mode implies copying a specific mural.

## Commercial design read

Treat the default request as:

> A contemporary Chinese commercial key visual for a design-conscious audience, combining cinematic product photography with Dunhuang mineral-pigment materiality.

Default visual dials:

- Composition variance: 8/10. Prefer layered, asymmetric depth over centered symmetry.
- Visual density: 7/10 for text-free art, 5/10 when the image must carry a headline.
- Ornament intensity: 5/10. Motifs support hierarchy; they do not fill every gap.
- Realism: 8/10 for products and devices, 6/10 for painted landscapes and ribbons.
- Contrast: high at the focal object, restrained in the background.

If the user gives a reference image, preserve its composition and invariants before applying these defaults.

## Choose generation or editing

### Generate

Use when no image needs to be preserved. For commercial mode, read:

- [Visual system](references/style-system.md) for palette, motifs, lighting, materials, and composition families.
- [Prompt recipes](references/prompt-recipes.md) for the relevant deliverable.

### Edit

Use when the user says remove text, fill the left side, change the object, rebalance the composition, or otherwise refers to an existing image.

Before editing:

1. Identify the target image.
2. State the single primary change.
3. List everything that must remain unchanged.
4. Apply one edit pass.
5. Inspect the result against the request and the invariants.

For commercial multi-step edits, read [Edit workflows](references/workflows.md). For apsara edits, use the photo-preservation and correction workflow in [Apsara mode](references/apsara-mode.md). Do not combine unrelated edits in one pass when drift would be hard to diagnose.

## Commercial visual invariants

Apply these unless the user explicitly overrides them:

1. Use one coherent mineral palette across the image.
2. Give the scene one obvious primary subject.
3. Build depth with foreground object, middle mural layer, and background cave or mountain layer.
4. Make commercial objects physically believable. Product geometry, materials, contact shadows, reflections, and perspective must hold together.
5. Use ribbons as directional flow, not random decoration.
6. Use lotus and caisson forms sparingly. One strong occurrence is better than a repeated pattern wall.
7. Keep gold restrained. It should act as reflected light, a sun disc, edge highlight, or small ornament.
8. Avoid real brand marks unless the user supplies them and requests their use.
9. Exclude religious figures by default in commercial mode. An explicit apsara portrait request routes to apsara mode; historical reconstruction and devotional content need a separate workflow.
10. Never rely on the word "高级" alone. Translate it into composition, spacing, material, lighting, palette, and object-scale decisions.

## Commercial default palette

Use role-based color language first; include hex values only when the workflow needs precise art direction.

- Charcoal cave black: dominant architectural base.
- Sand mineral white: illuminated mural panels and product surfaces.
- Cinnabar red: primary flowing ribbon.
- Malachite green: secondary ribbon and small product accents.
- Lapis blue: cool balance in mountains and fine accents.
- Ochre gold: sun disc, reflected light, thin edges, and small highlights.

Read [Visual system](references/style-system.md) before building a brand-wide palette or multiple related images.

## Commercial composition rules

### Text-free 5:2 cover

- Fill the entire frame with meaningful imagery.
- Do not reserve a title block unless the user asks for later typography.
- Give both left and right thirds visible subject matter.
- Keep an open path through the center so the panorama does not become a wall of objects.
- Vary scale: one large foreground object, two or three middle-depth panels, one distant architectural opening.
- Use a continuous ribbon system to connect the frame.

### 5:2 cover with text

- Reserve 38% to 48% of the frame for the title.
- Keep the title zone materially rich but visually quiet.
- Concentrate the product or visual-production scene in the opposite half.
- Use no more than two text lines unless the user supplies a longer title.
- Preserve safe margins and check legibility at X/Twitter thumbnail size.

### Product hero

- Show one product unless the brief specifies a set.
- Keep the full silhouette visible.
- Place the product on a real support surface with a contact shadow.
- Let the mural language appear behind or on the packaging, not over the product edge.
- Reserve space only when copy will actually be added.

### UI or device showcase

- Use the device as a commercial object, not a fake dashboard collage.
- Keep the screen perspective and bezel geometry believable.
- If no exact UI copy is supplied, use image-led screen content with no readable placeholder text.
- Do not place random microcopy, version labels, metrics, or decorative status dots.

### Multi-asset visual suite

- Lock the palette, ribbon width, edge treatment, shadow language, and grain.
- Vary the layout family across assets.
- Do not turn a suite into four identical cards with different crops.

More layouts and failure cases are in [Visual system](references/style-system.md).

## Text policy

Determine one of three states before generation:

- Exact text: reproduce only the supplied text, once, with explicit placement.
- Placeholder-free: generate the image without any readable text, then add typography in a layout tool.
- Text-free: prohibit all letters, numbers, labels, logos, watermarks, and interface microcopy.

For text-free requests, repeat the prohibition in both the primary request and constraints. Inspect product labels, device screens, background signage, frames, and decorative seals for accidental glyphs.

## Commercial prompt construction

Build prompts in this order:

1. Use case and asset type.
2. Primary request.
3. Scene and backdrop.
4. Subjects with exact counts and positions.
5. Composition and depth.
6. Style and realism.
7. Lighting.
8. Palette and materials.
9. Text state.
10. Invariants.
11. Avoid list.

Use visible nouns and measurable relationships. Replace "more premium" with instructions such as:

- Increase the main product to 32% of frame width.
- Reduce ornamental motifs to two families.
- Use a 45-degree warm key light from upper left.
- Keep gold below 10% of visible color area.
- Separate foreground, middle panels, and background opening.

Use [Prompt recipes](references/prompt-recipes.md) as adaptable starting points, not as fixed incantations.

## Image-tool workflow

When an image-generation or image-editing tool is available:

1. Generate at the requested aspect ratio.
2. Inspect the complete frame, especially edges and corners.
3. Check subject counts and placement.
4. Check for accidental text and logos.
5. In commercial mode, check product geometry, device geometry, reflections, and contact shadows. In apsara mode, inspect identity and preserved photo features, anatomy, attire, ribbon attachments and occlusions; for explicitly requested archery, inspect bow, string, arrow, and both hands as one connected system.
6. Make one targeted correction if a visible defect blocks the brief.
7. Preserve the accepted image non-destructively when creating variants.

When no image tool is available, output a production-ready prompt and a compact QA checklist. Do not pretend an image was generated.

## Required output behavior

For a generated image, report:

- final aspect ratio;
- whether text is included or prohibited;
- the final prompt or a concise prompt summary;
- saved path when the asset belongs to a project.

For an edited image, also report the change made and the invariants preserved.

## Quality gates

Before generation, check the prompt for the selected mode. A checker PASS means that textual guidance was found; it does not certify user intent, identity fidelity, anatomy, or rendered geometry. The caller must establish whether archery was explicitly requested before setting `--archery-requested`.

Before image delivery, inspect the actual pixels. Commercial mode uses [QA checklist](references/qa-checklist.md); apsara mode uses the image acceptance checklist in [Apsara mode](references/apsara-mode.md). Record prompt validation and image acceptance separately, with unperformed image checks marked pending. A commercial result fails when any of these are true:

- the user asked for no text but glyphs remain;
- one side of a full-frame composition is unintentionally empty;
- the product changes shape or floats without contact shadow;
- ribbons collide with the subject edge or hide essential detail;
- gold dominates the whole image;
- the image reads as a tourist poster, fantasy game splash screen, or generic luxury cosmetics ad;
- religious figures appear without an explicit request;
- the requested aspect ratio is wrong.

The bundled validator checks prompt completeness before generation. Existing calls keep commercial behavior:

```bash
python3 scripts/check_prompt.py prompt.txt --mode text-free --ratio 5:2
```

For a new apsara portrait (default 3:4):

```bash
python3 scripts/check_prompt.py portrait.txt --scene apsara --mode text-free
```

Add `--reference-photo --ratio <original-ratio>` for a photo edit. Add `--archery-requested` only after an explicit archery request, then validate the connected bow/string/arrow/hand instructions. These flags check prompt coverage, not images. See [Apsara mode](references/apsara-mode.md) for examples.

## Scope of repository changes

Repository updates become available only when the intended environment installs or updates this skill and actually loads it. A merged PR alone does not activate the skill in a chat or change an image tool. Never attribute an image defect to this repository without confirming the generating session used it.
