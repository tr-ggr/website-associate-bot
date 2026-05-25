# Redesign landing page Hero section and photo Snippets collage

## Problem

The landing page Hero section and photo "Snippets" collage currently look like basic MVP placeholders. The collage uses plain gray boxes with text like "Snippet 1" and simple rotated containers that lack realistic textures, authentic polaroid/film-style framing, overlap depth, handwriting elements, or engaging hover states. The Hero section needs a premium, high-impact aesthetic (rich gradients, grid overlays, micro-animations) to wow the user instantly and evoke a strong sense of graduation nostalgia.

## Potentially Related Files

- [src/app/page.tsx](src/app/page.tsx) — Main landing page file containing the Hero section (lines 7-35) and the Highlights/Snippets section (lines 36-72).
- [src/app/globals.css](src/app/globals.css) — Contains CSS styles where advanced borders, textures, and custom handwritten fonts can be declared.

## What to Fix

1. Upgrade the Hero section background in `src/app/page.tsx` with a premium dark-burgundy/amber gradient, incorporating a subtle, semi-transparent layout grid or stardust overlay to establish a premium feel.
2. Replace the raw text headers with high-end, responsive typography using custom tracking and font pairings (e.g. elegant serif italic for subheadings and strong sans-serif bold for titles).
3. Redesign the three "Snippet" photo cards into authentic Polaroid-style snapshots:
   - Apply a thick white paper-like border (`border-b-[40px] md:border-b-[48px]` to leave room for text).
   - Use high-fidelity stock images (representing student life, graduation caps, or university grounds) instead of gray divs.
   - Add a handwriting-style caption at the bottom border of each polaroid using a handwritten font (e.g. *Caveat* or *Reenie Beanie*).
   - Apply realistic, multi-layered box-shadows to simulate physical cards resting on a canvas.
4. Replace the solid-colored mockup tape elements with authentic-looking semi-transparent masking tape (using CSS background gradients, custom noise textures, and slightly jagged/torn borders).
5. Arrange the Polaroid snippets to overlap naturally using layered z-indexes, varying degrees of rotation, and absolute positions that adapt gracefully across mobile, tablet, and desktop screens.
6. Add engaging hover micro-animations to the Polaroid snapshots: when hovered, the card should gently lift (scale up, rotate closer to neutral, and cast a softer, deeper shadow).

## Acceptance Criteria

- The Hero section displays high-fidelity typography, harmonious warm color palettes, and premium background gradients.
- Photo snippets are styled as authentic Polaroid cards with white paper frames, custom handwritten captions, and realistic shadow depths.
- Mockup tape elements look like actual translucent masking tape holding down the photographs.
- The Polaroid collage is responsive and displays beautifully across all standard device sizes.
- Hovering over a photo snippet triggers a smooth lift-and-straighten animation with shadow transitions.
