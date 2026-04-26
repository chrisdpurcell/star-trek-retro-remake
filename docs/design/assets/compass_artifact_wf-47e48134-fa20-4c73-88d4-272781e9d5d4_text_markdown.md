# TOS-style starship asset prompts for ChatGPT Images 2.0

A complete, paste-ready prompt kit for generating placeholder isometric sprites and supporting art for an unofficial 23rd-century-style fan strategy game, built around the **`gpt-image-2`** model released by OpenAI on April 21, 2026. Every prompt below uses **descriptive visual-language only** — no copyrighted vessel names, registries, or class designators — keeping the asset set clearly derivative-not-copy for IP defensibility.

One critical finding up front: **OpenAI's official docs state `gpt-image-2` does *not* currently support transparent backgrounds** (a regression from `gpt-image-1.5`). The recommended workflow below generates each sprite on a flat keyable background and removes it in post (or falls back to `gpt-image-1.5` when native alpha is required). Treat any "transparent background" line in the prompts as a best-effort hint plus a planning instruction for the model to leave clean cuttable edges.

---

## A. ChatGPT Images 2.0 best practices in brief

**`gpt-image-2`** rewards labeled, structured natural-language prompts over comma-tag lists. The OpenAI cookbook's canonical 5-slot template — **Scene → Subject → Important details → Use case → Constraints** — outperforms paragraphs and reads cleanly at 80–250 words. The model gives the most weight to the first ~50 words, follows long instructions far better than its predecessors, supports up to **16 reference images** for style/identity conditioning, and can produce **up to 8 coherent images per prompt** in Thinking mode (Plus/Pro/Business). It has no public seed parameter and no native negative-prompt field — exclusions go in a final `Constraints:` block as plain English, repeated on every iteration.

For game-asset work specifically: always say **"isometric, 2:1 dimetric, parallel projection, no perspective"** to defeat the perspective-view default; lock lighting direction (recommended: warm key from upper-left) in every prompt; replace empty aesthetic words ("cinematic, 8K, masterpiece") with concrete visual facts ("matte painted lacquer, single hard key light, hand-stenciled markings"). **Generate at 1024×1024 or 2048×2048 and downscale to 256×256 with Lanczos** — the model cannot natively render small targets cleanly. Native 16:9 (e.g., **2048×1152**) is supported for splash art. Native transparency is currently unsupported on `gpt-image-2`; generate on a flat **#00FF00 magenta-free green** or **#FF00FF magenta** background and key it out with `rembg` or remove.bg, or fall back to `gpt-image-1.5` with `background="transparent"` for the few assets where alpha is non-negotiable.

---

## B. Style anchor (paste at the top of every prompt)

This block locks the visual language across the entire asset set. **Copy it verbatim into every prompt below** — never paraphrase, never trim. Style drift is silent and cumulative; the only defense is a literal repeated paragraph plus reference-image conditioning on the first approved hero asset.

```
STYLE ANCHOR — paste verbatim at the top of every prompt:

Rendering style: 1966–1969 television-era science-fiction filming-miniature
aesthetic. Hand-painted hard-shell studio model in matte lacquer, optically
composited against black on 35mm film. No CGI, no specular bloom, no lens
flare, no aztec paneling, no greebling, no panel-line weathering, no carbon
scoring. Smooth painted surfaces with stenciled markings only. Mid-century-
modern industrial design language: clean, confident, ceramic, aviation-
derived rather than nautical or rocket-like. No visible exhaust, no smoke,
no jet flames.

Perspective: isometric 3/4 view from above, 2:1 dimetric projection,
parallel orthographic — no perspective foreshortening, no vanishing point,
all parallel lines remain parallel. Camera tilted approximately 30 degrees
above horizontal, looking down-and-forward at the subject.

Lighting: a single hard key light from the upper-left of the frame at
roughly 45 degrees, soft cool ambient fill, deep crushed shadows on the
shaded side of the hull. Lighting direction is identical across the entire
asset set — the sun does not move between sprites.

Color treatment: 1960s color-television palette. Saturated primaries,
crushed blacks reading as charcoal-blue rather than pure black, slightly
warm overall cast. Limited palette per asset (≤8 dominant tones).

Framing: single subject centered in frame, full silhouette visible with
~10% padding on all sides, no cropping of nacelles or wingtips. Subject
isolated on a flat solid magenta background (#FF00FF) for clean keying;
no shadow, no ground plane, no horizon, no environment, no scenery, no
stars, no nebulae, no UI, no HUD, no text, no labels, no captions, no
signature, no watermark, no border, no frame, no vignette, no other
objects, no companion ships.

Output: 2048×2048 PNG unless otherwise specified, quality=high. The image
will be downscaled to 256×256 for in-game use, so silhouette must read
clearly at small sizes.
```

When you generate the **first** approved asset (recommended: the Federation-style cruiser NE facing — see C1 below), save it as `_hero_reference.png` and **pass it as a reference image on every subsequent prompt** with an added line: *"Match the palette, brushwork, lighting angle, surface finish, and overall era of reference image #1 exactly."* This is the single biggest consistency win available in the April 2026 model.

---

## C. The v0.1 asset prompt set

Filenames follow the project convention `{category}_{name}_{variant}.png` in lowercase snake_case. Each prompt assumes the style anchor (section B) is pasted at the top.

---

### C1. Federation-style cruiser — NE facing  →  `ship_federation_cruiser_facing_ne.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

Subject: A mid-23rd-century human-coalition exploratory cruiser, rendered
as a 1960s studio filming miniature.

Hull configuration:
- Primary hull: a flat, near-perfectly circular disc held above the rest
  of the ship. Diameter-to-thickness ratio approximately 9:1 — a thin
  discus, not a puck. Slight stepped dome rising in two tiers near the
  center of the upper surface, capped by a small cylindrical command
  turret at the apex. Underside is mostly flat with a single shallow
  hemispherical concave sensor pit at the ventral center.
- Connecting neck: a short narrow rectangular pylon angled rearward,
  joining the underside of the disc to the front-top of a horizontal
  cigar-shaped secondary hull. Four small windows visible down each face.
- Secondary hull: a horizontal cylindrical tube with length-to-diameter
  ratio of about 4:1, rounded snout, tapered tail with a flat circular
  cap. On the front face, a circular concave deflector dish in coppery
  amber tones ringed by a chrome bezel.
- Two long thin cylindrical warp engine pods mounted on swept-back swept-
  up flat pylons rising from the upper-rear of the secondary hull. The
  pods sit higher than the disc rim and are spaced well outboard. Each
  pod is roughly 4× the secondary hull's diameter in length, perfectly
  cylindrical. Front cap of each pod: a hemispherical translucent cherry-
  red dome (#C42A1A) with a glowing amber-orange core (#F2A038) suggesting
  a slow rotating impeller behind the bubble. Rear cap: a smooth dark
  sphere glowing soft electric blue (#3A6BC2) with three small radial
  spikes. A row of four narrow rectangular grilles along the upper spine
  of each pod, faintly back-lit warm yellow.

Surface finish: smooth matte hull in pale gray-green (#A4A89E) with
slightly lighter accent panels (#C7CAC4) and darker rim trim (#76776F).
A single thin matte-black pennant stripe runs around the disc edge.
Stenciled invented alphanumeric registry "NX-2247" in upright sans-serif
black capitals on the dorsal saucer, repeated on the ventral surface.
Sparse small rectangular window dots in concentric arcs on the disc, lit
soft warm yellow. Two small painted hangar-door rectangles aft on the
secondary hull. No aztec paneling, no panel-line weathering, no detailed
greebles — surface decoration is strictly stencils, pinstripes, and
window dots.

Orientation: bow pointing toward the upper-right corner of the frame
(the "1 o'clock" / north-east direction in screen space). The ship is
tilted slightly so the upper surface of the disc faces the viewer's
upper-left, exposing the dorsal markings. The full silhouette including
both engine pods is visible with ~10% padding.

Use case: 256×256 unit sprite for a 2:1 dimetric isometric turn-based
strategy game. Must read clearly at small sizes; silhouette is more
important than fine detail.

Constraints: do not name, label, or letter the ship beyond the invented
"NX-2247" registry. No real-world copyrighted ship designs, no specific
recognizable franchise vessels, no franchise logos. No text other than
"NX-2247". No shadow, no ground plane, no environment, no stars, no UI,
no border, no companion ships. Single subject only. Hull paint is matte
not glossy; no chrome highlights, no plastic sheen, no AI-airbrush look.
```

**Generate this first.** Approve it, save it as `_hero_reference.png`, and use it as reference image #1 on every other prompt below. Variant rejection criteria: front engine domes not red; rear caps not blue; engine pods angled forward instead of swept-back-and-up; primary hull thicker than ~1/9 its diameter; disc replaced by sphere; aztec paneling present; visible exhaust or thrusters; chrome/glossy hull; bow pointing the wrong direction.

---

### C2. Federation-style cruiser — SE facing  →  `ship_federation_cruiser_facing_se.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

[Reference image #1: ship_federation_cruiser_facing_ne.png — match its
palette, brushwork, lighting angle, surface finish, hull proportions,
engine-pod placement, and stenciled registry "NX-2247" exactly. This is
the same ship rotated, not a new design.]

Subject: The same mid-23rd-century human-coalition exploratory cruiser
shown in reference image #1, rotated so the bow points toward the lower-
right corner of the frame (the "5 o'clock" / south-east direction in
screen space). The viewer now sees more of the ship's port flank and
upper-rear quarter.

[Repeat the full hull configuration block from C1 verbatim — primary hull
disc, neck, secondary cylindrical hull, two cylindrical engine pods on
swept-back swept-up pylons, red front domes, blue rear caps, etc.]

Lighting must remain a hard key light from the upper-left of the frame
at 45 degrees — the sun has not moved. The shaded side of the hull is
now the upper-left-facing surface; the dorsal markings on the disc remain
visible because the camera angle is still 30° above the ship.

Constraints: identical to C1. Same registry "NX-2247", same palette, same
materials, same lighting direction. Bow pointing toward lower-right.
```

**Reject** any output where the lighting has rotated with the ship (sun follows the bow), where the registry number changes, or where surface details differ from the hero reference.

---

### C3. Federation-style cruiser — SW facing  →  `ship_federation_cruiser_facing_sw.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

[Reference image #1: ship_federation_cruiser_facing_ne.png — match
palette, brushwork, lighting angle, surface finish, hull proportions,
engine-pod placement, and stenciled registry "NX-2247" exactly.]

Subject: The same cruiser as reference image #1, rotated so the bow now
points toward the lower-left corner of the frame (the "7 o'clock" /
south-west direction in screen space). The viewer now sees the ship's
starboard flank and rear quarter; the dorsal markings remain visible
because the camera angle is still 30° above the ship.

[Repeat the full hull configuration block from C1 verbatim.]

Lighting remains a hard key light from the upper-left of the frame at
45 degrees. The shaded side of the hull is now the lower-right-facing
surface.

Constraints: identical to C1. Same registry "NX-2247", same palette,
same materials, same lighting direction. Bow pointing toward lower-left.
```

---

### C4. Federation-style cruiser — NW facing  →  `ship_federation_cruiser_facing_nw.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

[Reference image #1: ship_federation_cruiser_facing_ne.png — match
palette, brushwork, lighting angle, surface finish, hull proportions,
engine-pod placement, and stenciled registry "NX-2247" exactly.]

Subject: The same cruiser as reference image #1, rotated so the bow now
points toward the upper-left corner of the frame (the "11 o'clock" /
north-west direction in screen space). The viewer sees the ship's
starboard upper quarter; the dorsal markings on the disc remain visible.

[Repeat the full hull configuration block from C1 verbatim.]

Lighting remains a hard key light from the upper-left of the frame at
45 degrees — the bow now points toward the light source, so the front
of the disc and the front engine domes catch the strongest highlight.

Constraints: identical to C1. Same registry "NX-2247", same palette,
same materials, same lighting direction. Bow pointing toward upper-left.
```

---

### C5. Klingon-style warship — NE facing  →  `ship_klingon_warship_facing_ne.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

[Reference image #1: ship_federation_cruiser_facing_ne.png — match the
overall era, miniature aesthetic, lighting angle, paint finish, and
1960s color-television look. This is a different ship in the same
universe and the same studio aesthetic.]

Subject: A mid-23rd-century antagonist warship of a militaristic
interstellar empire, rendered as a 1960s studio filming miniature in
the same era and finish as reference image #1. Manta-ray-and-stinger
silhouette designed to read "predator" in a single flash cut.

Hull configuration (front to back):
- Forward command bulb: a smooth bulbous near-spherical pod with a
  slightly flattened underside, sitting at the very tip of the ship.
  A few small rectangular windows on its forward face. Looks like an
  insect head or a smooth helmet.
- Long thin neck-boom: a slender, slightly tapered rectangular tube
  extending rearward from the bulb, roughly 1.5× the bulb's diameter
  in length. Conspicuously narrow and exposed — gives the ship its
  trademark "head on a stick" predatory profile.
- Main body: the neck terminates in a flat, low, kite-shaped main hull
  with FORWARD-SWEPT WINGS — leading edges angle outward and forward,
  trailing edges angle outward and back. Opposite to the Federation
  cruiser's swept-back-and-up engine pylons. The main hull has a raised
  central spine with a small dome and three diagonal grilles along the
  dorsal surface. The aft trailing edge has segmented vent panels.
- Engines: cylindrical engine pods integrated INTO the wingtips (not on
  pylons), smaller in diameter than the Federation cruiser's pods. Each
  has a steady warm reddish-amber glowing forward intake (#C8501F);
  no rotating impeller, no blue rear cap.

Color scheme: matte two-tone paint divided along the horizontal
centerline. Dorsal (top): desaturated purplish-gray (#6F6772, muted
aubergine). Ventral (bottom): muted dirty olive-gray / military green-
gray (#7A8472). Dorsal main hull carries a small hand-painted angular
trefoil "trident-claw" emblem in matte slate-black. No other markings,
no registry numerals.

Surface finish: smooth matte lacquer, painted-on panel lines only, no
aztec paneling, no weathering, no greebles. CRITICAL: this is the 1960s-
era design language only — no dense paneling, no dark militaristic dark-
green, no heavy detail. The 1979 redesign aesthetic must NOT appear.

Orientation: bow (the forward command bulb) pointing toward the upper-
right corner of the frame ("1 o'clock" / north-east in screen space).
The viewer sees the dorsal main hull and port wing in three-quarter view.
Full silhouette including both wingtips and the forward command bulb
visible with ~10% padding.

Use case: 256×256 unit sprite for a 2:1 dimetric isometric turn-based
strategy game.

Constraints: no specific copyrighted franchise designs, no franchise
logos, no canonical class names. No real-world military insignia. No
text. No companion ships, no shadow, no environment. The dorsal must
be purplish-gray and the ventral olive-gray — do NOT render this as
a uniformly dark-green ship.
```

**Reject** outputs that look like the late-1970s redesign (dense aztec paneling, uniformly dark-green hull, busy greebles), or where the wings sweep backward instead of forward, or where the command bulb sits flush to the body without a visible neck.

---

### C6. Klingon-style warship — SE facing  →  `ship_klingon_warship_facing_se.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

[Reference image #1: ship_federation_cruiser_facing_ne.png — match
overall era and finish.]
[Reference image #2: ship_klingon_warship_facing_ne.png — match palette,
two-tone paint scheme, hull proportions, command bulb, neck-boom length,
forward-swept wing geometry, and surface finish exactly. This is the
same ship rotated, not a new design.]

Subject: The same antagonist warship shown in reference image #2, rotated
so the bow (the forward command bulb) points toward the lower-right
corner of the frame ("5 o'clock" / south-east direction). The viewer
sees the dorsal main hull from a different angle; the ventral two-tone
divide remains correctly oriented (top of hull purplish-gray, bottom
olive-gray).

[Repeat the full hull configuration block from C5 verbatim.]

Lighting remains a hard key light from upper-left at 45 degrees. The
shaded side of the hull is now the upper-left-facing flank.

Constraints: identical to C5. Bow pointing toward lower-right.
```

---

### C7. Klingon-style warship — SW facing  →  `ship_klingon_warship_facing_sw.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]
[Reference image #1: ship_federation_cruiser_facing_ne.png]
[Reference image #2: ship_klingon_warship_facing_ne.png — match exactly.]

Subject: The same antagonist warship as reference image #2, rotated so
the bow points toward the lower-left corner of the frame ("7 o'clock" /
south-west direction). The viewer sees the dorsal hull and starboard
forward-swept wing.

[Repeat the full hull configuration block from C5 verbatim.]

Lighting remains upper-left key. Constraints identical to C5. Bow
pointing toward lower-left.
```

---

### C8. Klingon-style warship — NW facing  →  `ship_klingon_warship_facing_nw.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]
[Reference image #1: ship_federation_cruiser_facing_ne.png]
[Reference image #2: ship_klingon_warship_facing_ne.png — match exactly.]

Subject: The same antagonist warship as reference image #2, rotated so
the bow points toward the upper-left corner of the frame ("11 o'clock" /
north-west direction). The bow now faces the key light, so the forward
command bulb and the leading edges of the forward-swept wings catch
the strongest highlight.

[Repeat the full hull configuration block from C5 verbatim.]

Constraints identical to C5. Bow pointing toward upper-left.
```

---

### C9. Romulan-style warbird — NE facing  →  `ship_romulan_warbird_facing_ne.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]
[Reference image #1: ship_federation_cruiser_facing_ne.png — match the
overall era, miniature aesthetic, and 1960s color-television look.]

Subject: A mid-23rd-century cruiser of an isolationist imperial power,
rendered as a 1960s studio filming miniature. Avian-themed silhouette
with bold heraldic markings.

Hull configuration:
- Primary hull: a flat, broad lozenge / lens-shaped saucer, somewhat
  similar in scale to a Federation disc but FLATTER and WIDER (more
  oval than circular when viewed from above). No raised dome on top,
  no command turret at the apex.
- Two short, thick cylindrical engine pods mounted parallel to the
  body on stubby pylons, sitting close alongside the hull at port and
  starboard — NOT swept up and back like the Federation cruiser. The
  pods are shorter and thicker than the Federation type, roughly 2× the
  hull thickness in diameter. Front caps: hemispherical translucent
  blue domes (#3D7CC4) — note this is the inverse of the Federation
  cherry-red. Rear caps: smooth dark silver-gray.
- A single raised vertical dorsal tail fin sits on the upper-rear
  centerline, like a 1950s-car tail fin or a shark's dorsal. A few
  vent slats painted on it.

Surface finish: smooth matte hull in light neutral gray (#B0B2AE), almost
indistinguishable from the Federation hull when viewed from above. A few
darker gray accent panels and a small invented alphanumeric identifier
in matte-black stencil on the dorsal surface. Sparse tiny rectangular
window dots, very few of them.

The signature feature — the painted bird emblem:
A large, stylized heraldic bird-of-prey graphic painted on the VENTRAL
hull, wings half-spread, beak-and-head pointing forward toward the bow,
talons or tail-feathers spreading toward the rear. The bird extends
across the saucer underside almost wingtip-to-wingtip. Style is bold
flat heraldic poster art — like an enamel badge or 1940s bomber nose-
art — with strong dark outlines, NOT a realistic eagle illustration.
Dominant color: burnt orange / vermilion (#C8501F). Counter-shaded with
off-white (#E8E2D2). Detail linework in deep crimson (#7C1F1F).

Orientation: bow pointing toward the upper-right corner of the frame
("1 o'clock" / north-east in screen space). Critically, because of the
oblique 30°-above isometric camera angle, the painted bird on the
underside should be PARTIALLY VISIBLE through the foreshortened ventral
surface near the leading edge of the saucer — the bird's head and one
wing should be glimpsed, conveying the ship's iconography even from a
high-3/4 view. The dorsal stays mostly plain gray; the bird is the visual
hook.

Use case: 256×256 unit sprite for a 2:1 dimetric isometric turn-based
strategy game.

Constraints: no specific copyrighted franchise designs, no canonical
class names, no franchise logos. No text other than the small invented
dorsal identifier. The bird emblem must be heraldic / poster-style flat
art, NOT a photorealistic eagle. Engine pods must be parallel to the
body, NOT swept up and back. Front engine caps are blue, not red. No
companion ships, no shadow, no environment.
```

**Reject** outputs that look like the Federation cruiser with extra paint (engines swept up and back, red front caps, raised central dome), photorealistic eagles instead of heraldic flat art, or no visible bird at all.

---

### C10. Romulan-style warbird — SE facing  →  `ship_romulan_warbird_facing_se.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]
[Reference image #1: ship_federation_cruiser_facing_ne.png]
[Reference image #2: ship_romulan_warbird_facing_ne.png — match palette,
hull proportions, engine-pod placement parallel to body, blue front
domes, dorsal tail fin, and the painted heraldic bird emblem on the
ventral surface exactly.]

Subject: The same avian-marked imperial cruiser as reference image #2,
rotated so the bow points toward the lower-right corner of the frame
("5 o'clock" / south-east direction). The viewer's lower angle now
glimpses more of the ventral painted bird emblem on the leading flank.

[Repeat the full hull configuration block from C9 verbatim.]

Lighting remains upper-left key. Constraints identical to C9. Bow
pointing toward lower-right.
```

---

### C11. Romulan-style warbird — SW facing  →  `ship_romulan_warbird_facing_sw.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]
[Reference image #1: ship_federation_cruiser_facing_ne.png]
[Reference image #2: ship_romulan_warbird_facing_ne.png — match exactly.]

Subject: The same warbird as reference image #2, rotated so the bow
points toward the lower-left corner of the frame ("7 o'clock" / south-
west direction). The viewer sees the starboard flank with the painted
bird's other wing partially visible across the ventral edge.

[Repeat the full hull configuration block from C9 verbatim.]

Lighting remains upper-left key. Constraints identical to C9. Bow
pointing toward lower-left.
```

---

### C12. Romulan-style warbird — NW facing  →  `ship_romulan_warbird_facing_nw.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]
[Reference image #1: ship_federation_cruiser_facing_ne.png]
[Reference image #2: ship_romulan_warbird_facing_ne.png — match exactly.]

Subject: The same warbird as reference image #2, rotated so the bow
points toward the upper-left corner of the frame ("11 o'clock" / north-
west direction). The bow now faces the key light, so the leading edge
of the saucer and the blue front engine caps catch the strongest
highlight.

[Repeat the full hull configuration block from C9 verbatim.]

Constraints identical to C9. Bow pointing toward upper-left.
```

---

### C13. Asteroid  →  `anomaly_asteroid.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

Subject: A single irregular space asteroid, rendered as a hand-sculpted
1960s television studio miniature — papier-mâché and painted plaster,
shot against black with a single hard key light from the upper-left.

Form: lumpy, irregular, vaguely potato-shaped or kidney-shaped silhouette
with shallow surface bumps and a few small craters. Clearly hand-built,
not photorealistic. Surface texture is matte and dusty, NOT detailed
geological strata, NOT volumetrically rendered. No visible CGI lighting,
no global illumination, no procedural noise — this looks like a model
photographed on 35mm film.

Color: warm tan-gray base (#7E7468) shading to brownish (#5E4E40) on
the shaded right-hand side. A faint colored gel rim-light tint (subtle
orange) on the lit edge.

Orientation: tumbling slowly, presented at a generic 3/4 angle so the
silhouette reads clearly on a 2:1 dimetric tilemap.

Use case: 256×256 environmental hazard sprite for an isometric turn-
based strategy game.

Constraints: single asteroid only — NOT a field, not a cluster. No other
rocks in frame. No stars, no nebula, no ship, no environment. Smooth-
ish matte surface, hand-sculpted look, no photoreal volumetric detail,
no AI airbrush look. No text, no labels.
```

---

### C14. Debris field  →  `anomaly_debris_field.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]
[Reference image #1: ship_federation_cruiser_facing_ne.png — match the
hull palette and miniature finish so the wreckage clearly reads as
fragments of ships from this universe.]

Subject: A scatter of 5–7 tumbling pieces of starship wreckage, rendered
as 1960s television studio model fragments shot against black. The
fragments are bent metal-foil shards, broken hull plates, snapped pylon
stubs, and a single twisted cylindrical engine-pod fragment with a dead
unlit forward dome.

Form: each piece is small relative to the frame, scattered in a loose
constellation across the image with a shallow parallax (some closer,
some farther). Edges are jagged and blackened with charred matte paint;
two or three pieces have a faint internal red glow (#C42A1A) suggesting
hot core damage. Slow tumble implied by orientation, not motion blur.

Color: pale gray-green hull paint fragments (#A4A89E) with charred
edges (#1A1A1A) and the occasional warm-red internal glow.

Orientation: presented at a 3/4 oblique view consistent with the iso-
metric camera; fragments are scattered roughly within the central 80%
of the frame.

Use case: 256×256 environmental hazard / map-feature sprite.

Constraints: NO intact ship, no recognizable hull section larger than a
quarter of one ship, no copyrighted markings, no franchise logos. No
text. No stars, no nebula, no environment. The fragments are clearly
debris, not a ship.
```

---

### C15. Nebula  →  `anomaly_nebula.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

Subject: A 1960s television-effects nebula, rendered as a back-lit
colored-gel cloud-tank effect. NOT a photoreal Hubble-style nebula,
NOT a JWST deep-field. Think tinted vapor, swirling smoke, and thin
colored cellophane animated under glass.

Form: a roughly circular planar swirl of luminous colored haze filling
the central 80% of the frame, with soft feathered edges fading to black.
The swirl reads as flat curtains of color rather than volumetric cloud
— layered planes of tint, not 3D dust.

Palette: dominant magenta-purple core (#8E3FC4) shading outward through
electric pink to a sickly yellow-green outer fringe (#C4D03A). Faint
hand-rotoscoped white energy zigzags scattered across the cloud, drawn
as solid 2D lines rather than realistic plasma.

Background: pure black, no stars, no other objects. The nebula glow does
not illuminate any nearby objects (there are none).

Use case: 256×256 environmental / map-feature sprite for an isometric
turn-based strategy game. Will sit on a tile as a hazard or terrain
feature, so the silhouette must read on a black background.

Constraints: no photorealistic nebula detail, no Hubble palette, no
NASA imagery, no volumetric cloud rendering. No stars in frame. No
text. No ship, no debris.
```

---

### C16. Black hole / spatial anomaly  →  `anomaly_black_hole.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]

Subject: A 1960s television-effects spatial anomaly, rendered as a
back-lit rotating animation cel — NOT a relativistic black hole with
accretion disk and photon ring (that visual vocabulary is post-1979
and must NOT appear).

Form: a swirling 2D pinwheel of bright concentric color rings spiraling
inward to a dark oval core. Reads clearly as a hand-drawn animation
effect, not a physics simulation. Rotational motion implied by the
inward spiral pattern. A faint distorted starfield streak bends
slightly toward the central core.

Palette: outermost ring bright yellow (#F2D838) → orange (#E89028) →
cherry red (#C42A1A) → black core. Colors are saturated and slightly
poster-flat, not gradient-smoothed. A hand-rotoscoped optical halo
edge gives the whole effect a faint rainbow fringe.

Background: black, with a sparse scatter of small white pinhole stars
(varied sizes, no nebulae, no galaxies) bending faintly inward toward
the anomaly.

Use case: 256×256 environmental hazard sprite for an isometric turn-
based strategy game.

Constraints: NO accretion disk, NO photon ring, NO gravitational
lensing distortion, NO realistic event horizon, NO Interstellar-style
imagery. This is explicitly a 1960s effects-driven cel, not a
scientifically accurate black hole. No text, no labels.
```

---

### C17. Starbase  →  `station_starbase.png`

```
[PASTE STYLE ANCHOR FROM SECTION B]
[Reference image #1: ship_federation_cruiser_facing_ne.png — match the
hull palette, paint finish, and miniature aesthetic so the starbase
clearly belongs to the same universe and faction.]

Subject: A mid-23rd-century human-coalition orbital trading and refit
station, rendered as a 1960s television studio filming miniature.
"Spider / mushroom" silhouette descended from period NASA/Douglas
Aircraft concept models.

Hull configuration:
- Central core: a vertical mushroom-cap dome sitting atop a fat
  cylindrical core spire.
- Outboard pods: three small dome-tipped cylindrical module pods held
  away from the central core by thin radial booms, each pod capped with
  a rounded clamshell-like end. The pods are evenly spaced around the
  core at 120° intervals.
- Lower base: a wide flat disc-shaped docking platform at the bottom
  of the core spire, with a circular hangar slot opening on its lower
  surface.
- Spires / antennae: a few thin cylindrical antenna masts rising from
  the very top of the dome.

Color: same off-white / pale gray-green as the Federation cruiser
(#A4A89E) with darker gray pinstripe trim and matte-black stenciled
alphanumeric markings ("NB-7" or similar invented identifier). Sparse
warm-amber lit window dots (#E8C77A) across the core and pods. A slow-
rotating warm-red docking beacon (#C23A2A) at one extremity, an amber
beacon (#F0A93C) at another.

Surface finish: smooth matte plastic-and-balsa miniature look, no
greebles, no aztec paneling.

Orientation: presented at a 3/4 oblique view from above-front so all
three outboard pods are visible plus the docking-platform disc. Single
subject centered with ~10% padding.

Use case: 256×256 large-station sprite for an isometric turn-based
strategy game.

Constraints: no specific copyrighted franchise stations, no spacedock
designs from later eras (no enclosed cathedral-scale dome stations —
this is the small TOS-era family). No franchise logos. No ships docked.
No environment, no stars, no shadow.
```

---

### C18. App icon  →  `icon_app.png`

```
[PASTE STYLE ANCHOR FROM SECTION B — but override the "framing" line:
this asset is the game's identity icon, not a unit sprite.]
[Reference image #1: ship_federation_cruiser_facing_ne.png — match the
era and palette.]

Subject: A 1024×1024 game application icon for an unofficial fan
strategy game set in a 1960s-television-style 23rd-century universe.
Bold flat silhouette of a Federation-style cruiser at a 3/4 angle —
flat circular saucer disc, cylindrical secondary hull, two cylindrical
warp pods on swept-back-and-up pylons — filling roughly 70% of the
frame, centered with even padding.

Composition: the ship silhouette in front of a simple two-color
background — a deep starfield-blue circle (#1A2540) on a slightly
lighter navy square (#243057), with a subtle 2 px highlight on the
top edge suggesting a glossy app-icon bezel. A few sparse small white
pinhole stars scattered around the ship.

Color palette (limited, ≤4 dominant tones): deep navy #1A2540, lighter
navy #243057, hull off-white #C7CAC4, accent cherry-red #C42A1A on the
front engine domes. High contrast. The silhouette must read clearly as
a black-on-light shape if all detail is removed, and must remain
recognizable when scaled to 32×32 and 16×16.

Use case: master app icon, will be downscaled to 256, 128, 64, 48, 32,
24, 16 px. Silhouette legibility at 32×32 is the primary success
criterion.

Constraints: no text, no letters, no numbers, no game title, no
watermark, no signature, no border (the OS will round corners). No
specific copyrighted franchise designs, no franchise logos. The ship
silhouette must be unmistakably a flat-disc-plus-twin-cylinders profile
but stylized enough to be clearly derivative-not-copy. Generate at
1024×1024 PNG.
```

**Test before approving:** downscale to 32×32 and 16×16. If the silhouette becomes a brown/gray blob, simplify and regenerate — fewer details, bigger ship, stronger color contrast.

---

### C19. Splash background  →  `bg_splash_main.png`

```
[PASTE STYLE ANCHOR FROM SECTION B — but override the "framing" and
"output" lines: this asset is a 16:9 splash background, not a centered
sprite. Do NOT generate on a magenta keying background; this is a
finished scene with a black starfield background.]
[Reference image #1: ship_federation_cruiser_facing_ne.png — match the
ship era and miniature aesthetic.]

Subject: A 2048×1152 (16:9 widescreen) main-menu splash background for
an unofficial fan strategy game set in a 1960s-television-style 23rd-
century universe.

Scene: a wide cinematic vista of deep space. In the upper-right
quadrant, a Federation-style cruiser (flat disc primary hull, cylindrical
secondary hull, two long cylindrical warp pods on swept-back-and-up
pylons, red glowing front domes, blue glowing rear caps, pale gray-
green hull) flies in 3/4 view toward the camera. In the middle distance
toward center-right, a softer-focus mushroom-silhouetted orbital station
with three outboard pod modules. In the far distance behind everything,
a single matte-painted planet — solid roundel with a clear day/night
terminator, mostly emerald-green with one tan continental band, painted
in 1960s gouache style. A small soft yellow sun glints off the upper-
left of the planet's terminator.

Background: a 1960s sparse starfield — small white and pale-yellow
pinhole stars of varied size (3–4 size grades) on deep crushed-black
space (#0A0E1F). No nebula detail, no galaxy backdrops, no JWST-style
deep-field, no anachronistic dust lanes. A faint, very subtle magenta-
green nebula veil in the upper-left as a single colored gel layer, kept
deliberately low-contrast.

Composition: leave the central LOWER THIRD of the frame visually quiet
— a subtle dark gradient with NO significant detail and NO ships — to
serve as overlay space for the game's title and menu buttons. The
upper two-thirds carries the ship, station, planet, and starfield.

Lighting: warm key light from upper-left at 45 degrees illuminates the
ship and station; stars and planet provide cool ambient. Single hard
key consistent with the rest of the asset set.

Use case: main-menu splash background. Will be downscaled / cropped to
1920×1080 for in-game display.

Constraints: no text, no game title, no logos, no UI elements, no menu
buttons, no characters in foreground, no watermark. No specific copy-
righted franchise designs. The ship must use the same Federation-style
hull configuration as reference image #1 (or as close as possible) but
need not carry a registry stencil at this scale. Painterly matte finish,
no CGI sheen.
```

**Note:** specify size **2048×1152** in the API call (it is a documented native 16:9 size for `gpt-image-2`); downscale to 1920×1080 in post with Lanczos.

---

## D. Workflow tips for the user

### How to evaluate first-pass outputs

For every generation, eyeball a checklist in this order: **silhouette, palette, era, perspective, framing, exclusions**. If any of the first three fail, regenerate with sharper prompt language — don't paint over fundamental misses. If only framing or minor exclusions fail, do a single-change edit on the existing image rather than rerolling the whole thing (`gpt-image-2` handles iterative single-change edits very well; cumulative multi-change edits cause silent drift). For unit sprites specifically, downscale every approved 2048×2048 master to 64×64 immediately and look at it — if the ship is unrecognizable at minimap size, your silhouette is too cluttered and the prompt needs simplification, not retouching. Reject any output that introduces a vanishing point, baked drop shadow on a transparent background, unrequested text or lettering on the hull, late-1970s aztec paneling, or franchise-specific markings (no actual NCC numbers, no actual class names visible).

### How to maintain visual consistency across the set

Generate the **Federation cruiser NE facing first** (C1), iterate it until it's the best example of your style anchor in practice, save it as `_hero_reference.png`, and then **pass it as reference image #1 on every subsequent prompt** including all the non-Federation ships, the starbase, the icon, and the splash. The hero reference is what locks the era and palette across the set; the literal repeated style anchor paragraph is what locks the framing rules. Then for each of the three ship lines (Federation, Klingon-style, Romulan-style), generate the NE facing first, approve it, and use *that* as a second reference image for the other three facings of the same ship. This two-tier reference structure (universe hero → ship hero → facings) is the difference between a coherent placeholder set and a Frankenstein gallery.

### April 2026 release quirks to watch for

The big one: **`gpt-image-2` does not currently support transparent backgrounds** — passing `background="transparent"` to the API on this model is rejected. Two practical responses: (1) for unit sprites and stations, generate on the magenta keying background specified in the style anchor and remove it in post with `rembg` (`pip install rembg; rembg i input.png output.png`) or remove.bg; (2) for any asset where alpha is genuinely critical and post-keying produces fringes you can't tolerate, **fall back to `gpt-image-1.5`** for that specific asset — it remains on the API specifically for transparency workflows and accepts `background="transparent"`. Other quirks: there is **no public seed parameter**, so reproducibility comes from prompt-as-code plus reference conditioning, never from RNG control; `input_fidelity` is **rejected** as a parameter (always treated as high on `gpt-image-2`); the model is **rate-limited tightly on the free tier** (~2 images/day), so do iterative work on a Plus subscription minimum; **DALL-E 2 and 3 retire May 12, 2026**, and any older prompt advice referencing them should be discarded; Thinking mode (Plus/Pro/Business) lets you generate up to 8 coherent images in one call, which is the fastest way to produce all four facings of a single ship if you trust the model's batch consistency. Finally, the model loves to add unrequested incidental text — always keep a long explicit `no text, no letters, no labels, no signage, no glyphs, no watermark, no logos` block in your constraints, and if a generation comes back with hull lettering you didn't ask for, the fix is to reroll, not to inpaint.

### How to archive prompts

Treat every prompt as versioned source. For each asset, create a markdown file at `assets/prompts/{asset_name}.md` with a single canonical structure: header with the asset path and the `gpt-image-2` model version, a link to `assets/prompts/STYLE_GUIDE.md` (where the style anchor from section B above lives as the single source of truth), the verbatim final prompt that produced the approved file, the API parameters used (`size`, `quality`, `output_format`, references), the post-processing pipeline (Lanczos downscale 2048→256, optional 1px alpha erode, optional unsharp mask r=0.5), and an iteration log table tracking versions with dates, what changed, and the archived intermediate file. Commit the `.md` alongside the `.png` in Git — diffs become meaningful, regenerations become reproducible, and any teammate (or future-you) can answer "why does this asset look like this?" by reading one file. The 19 prompt files implied by this kit (`ship_federation_cruiser.md`, `ship_klingon_warship.md`, `ship_romulan_warbird.md`, `anomaly_asteroid.md`, `anomaly_debris_field.md`, `anomaly_nebula.md`, `anomaly_black_hole.md`, `station_starbase.md`, `icon_app.md`, `bg_splash_main.md`) plus the `STYLE_GUIDE.md` constitute the entire visual contract for v0.1 — generate, archive, and version them together.

---

## Quick-start checklist

1. Save section B's style anchor as `assets/prompts/STYLE_GUIDE.md`.
2. Generate **C1 (Federation cruiser NE)** at 2048×2048, `quality="high"`, on `gpt-image-2`. Iterate until it's the best representative of your style anchor.
3. Save the approved master as `_hero_reference.png`. Downscale to 256×256 with Lanczos for `ship_federation_cruiser_facing_ne.png`.
4. Generate C2–C4 (the three other Federation facings) using C1 as reference image #1.
5. Generate C5 (Klingon-style NE) using C1 as reference. Approve, then generate C6–C8.
6. Generate C9 (Romulan-style NE) using C1 as reference. Approve, then generate C10–C12.
7. Generate the four single-asset prompts (C13–C16: asteroid, debris field, nebula, black hole) and C17 (starbase) — all referencing C1 for era consistency.
8. Generate C18 (app icon) at 1024×1024 and C19 (splash background) at 2048×1152.
9. Key out the magenta background on every unit sprite with `rembg`. Apply 1px alpha erode and unsharp mask r=0.5.
10. Commit all 19 PNGs and 11 prompt `.md` files to Git in one tagged release: `assets-v0.1`.
