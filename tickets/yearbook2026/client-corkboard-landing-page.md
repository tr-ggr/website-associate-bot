# Redesign Freedom Wall to feel like a legit corkboard

## Problem

The current Freedom Wall on the landing page is a basic, unpolished section with a flat color background and hard-coded sticky notes. It lacks authentic depth, rich visual textures, realistic pin elements, shadowed layers, and natural interactive responses that make it feel like a real physical corkboard. To wow the user, we need to create a highly premium, tactile, and responsive corkboard experience that feels hand-made, personal, and nostalgic.

## Potentially Related Files

- [src/app/page.tsx](src/app/page.tsx) — Main landing page where the corkboard section is defined (lines 74-118).
- [src/lib/data/notes.json](src/lib/data/notes.json) — JSON data defining the sticky notes' content, placement, and colors.
- [src/app/globals.css](src/app/globals.css) — Custom styles and variables for custom fonts or advanced CSS textures.

## What to Fix

1. Replace the simple flat color background of the Freedom Wall section in `src/app/page.tsx` with a rich, multi-layered cork texture, combined with CSS radial gradients to simulate natural overhead lighting.
2. Add a thick, stylized wooden border/frame around the entire corkboard container using linear gradients, wood colors (e.g., rich warm oak), and inset box-shadows to give it 3D physical framing.
3. Redesign the sticky notes to look like genuine pieces of colored paper (pastel yellow, light blue, soft pink, pale green) with soft paper textures and subtle bottom-curl shadow effects using CSS `:before` or `:after` pseudo-elements.
4. Replace standard system fonts on the notes with a beautiful, hand-written cursive font from Google Fonts (e.g., *Caveat*, *Shadows Into Light*, or *Architects Daughter*) loaded globally.
5. Enhance the pin elements to look like 3D plastic push pins (using custom borders, radial gradients for highlight, and a distinct angled shadow cast on the note below it).
6. Implement a smooth hover animation for each sticky note where it gently straightens (rotation changes to `0deg`), scales up slightly, and increases its drop-shadow depth, suggesting that the note is being examined closely.
7. Ensure sticky note placement coordinates in `src/lib/data/notes.json` scale gracefully on mobile screens or collapse into a responsive layout so they do not overlap illegibly on small displays.

## Acceptance Criteria

- The Freedom Wall section resembles a realistic corkboard complete with a wooden frame and lighting gradient overlay.
- Sticky notes look like paper cards with distinct curling/shadow effects, realistic plastic push pins, and hand-written style fonts.
- Hovering over any sticky note plays a smooth transition animation (straightens the note, lifts it up, and deepens its shadow).
- The corkboard is fully responsive, adjusting card coordinates or stacked columns gracefully on mobile screens without breaking accessibility or legibility.
