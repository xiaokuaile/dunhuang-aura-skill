---
name: dunhuang-aura
description: Create or edit commercial key visuals, product advertising, social graphics, and 5:2 covers in a contemporary Dunhuang mineral-pigment style. Use when the user asks for 敦煌美学, dark cave-wall textures, illuminated mural panels, flowing mineral-color ribbons, or this specific product-stage visual language. Do not use for archaeological restoration, historical reconstruction, or devotional religious imagery.
---

# Dunhuang Aura

Create polished commercial imagery that borrows Dunhuang's mineral colors, weathered surfaces, ribbons, lotus geometry, caisson order, caves, mountains, and luminous murals without turning the result into a scenic souvenir poster.

This is a commercial art-direction skill. It is not a license to copy a specific mural, reproduce a religious figure, or paste every Dunhuang motif into one frame.

## Design read

Treat the default request as:

> A contemporary Chinese commercial key visual for a design-conscious audience, combining cinematic product photography with Dunhuang mineral-pigment materiality.

Default visual dials:

- Composition variance: 8/10. Prefer layered, asymmetric depth over centered symmetry.
- Visual density: 7/10 for text-free art, 5/10 when the image must carry a headline.
- Ornament intensity: 5/10. Motifs support hierarchy; they do not fill every gap.
- Realism: 8/10 for products and devices, 6/10 for painted landscapes and ribbons.
- Contrast: high at the focal object, restrained in the background.

If the user gives a reference image, preserve its composition and invariants before applying these defaults.

## Choose the operating mode

### Generate

Use when no image needs to be preserved. Read:

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

For multi-step edits, read [Edit workflows](references/workflows.md). Do not combine unrelated edits in one pass when drift would be hard to diagnose.

## Non-negotiable visual invariants

Apply these unless the user explicitly overrides them:

1. Use one coherent mineral palette across the image.
2. Give the scene one obvious primary subject.
3. Build depth with foreground object, middle mural layer, and background cave or mountain layer.
4. Make commercial objects physically believable. Product geometry, materials, contact shadows, reflections, and perspective must hold together.
5. Use ribbons as directional flow, not random decoration.
6. Use lotus and caisson forms sparingly. One strong occurrence is better than a repeated pattern wall.
7. Keep gold restrained. It should act as reflected light, a sun disc, edge highlight, or small ornament.
8. Avoid real brand marks unless the user supplies them and requests their use.
9. Exclude religious figures by default. Do not generate Buddhas, bodhisattvas, apsaras, worship scenes, or copied mural characters unless the user explicitly requests historically grounded or devotional content.
10. Never rely on the word "高级" alone. Translate it into composition, spacing, material, lighting, palette, and object-scale decisions.

## Default palette

Use role-based color language first; include hex values only when the workflow needs precise art direction.

- Charcoal cave black: dominant architectural base.
- Sand mineral white: illuminated mural panels and product surfaces.
- Cinnabar red: primary flowing ribbon.
- Malachite green: secondary ribbon and small product accents.
- Lapis blue: cool balance in mountains and fine accents.
- Ochre gold: sun disc, reflected light, thin edges, and small highlights.

Read [Visual system](references/style-system.md) before building a brand-wide palette or multiple related images.

## Composition rules

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

## Prompt construction

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
5. Check product geometry, device geometry, reflections, and contact shadows.
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

## Quality gate

Before delivery, read and run [QA checklist](references/qa-checklist.md). A result fails when any of these are true:

- the user asked for no text but glyphs remain;
- one side of a full-frame composition is unintentionally empty;
- the product changes shape or floats without contact shadow;
- ribbons collide with the subject edge or hide essential detail;
- gold dominates the whole image;
- the image reads as a tourist poster, fantasy game splash screen, or generic luxury cosmetics ad;
- religious figures appear without an explicit request;
- the requested aspect ratio is wrong.

The bundled validator checks prompt completeness before generation:

```bash
python3 scripts/check_prompt.py prompt.txt --mode text-free --ratio 5:2
```
