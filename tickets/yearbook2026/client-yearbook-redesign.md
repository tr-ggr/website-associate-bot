# Redesign Yearbook page to look and feel like a classic graduation yearbook

## Problem

The current yearbook page feels like a formal, sterile corporate "About Us" or team overview page of a business website. It uses standard rounded grids and basic layouts that lack the warmth, nostalgia, and classic collegiate aesthetic of a physical yearbook. A genuine yearbook should display profiles (objects) as tactile portrait cards. Each card must clearly showcase five key elements: a high-quality portrait photo, the graduate's name, their editorial position/role, their academic program (e.g., BS Computer Science), and their chosen personal quote as the aesthetic centerpiece.

## Potentially Related Files

- [src/app/yearbook/page.tsx](src/app/yearbook/page.tsx) — Main yearbook page containing the grid and rendering code.
- [src/lib/data/officers.json](src/lib/data/officers.json) — JSON database containing graduate profiles, which needs to be updated with academic program fields.
- [src/app/globals.css](src/app/globals.css) — Custom styles for paper textures, elegant borders, and font definitions.

## What to Fix

1. Update the schema and data in `src/lib/data/officers.json` to include a `"program"` field for every graduate (e.g., `"BS Computer Science"`, `"BS Information Technology"`, etc.) and ensure photo asset references are available.
2. Completely overhaul the grid layout in `src/app/yearbook/page.tsx`. Replace the rounded corporate cards with classic, rectangular portrait frames resembling genuine yearbook pages.
3. Design the graduate profile cards with a premium, tactile texture:
   - Use rectangular portrait photo containers with a subtle cream/white card border instead of circular, high-contrast avatars.
   - Display the graduate's name using bold, elegant typography (serif or high-quality sans-serif).
   - Display their editorial position and academic program (e.g., `BS Computer Science`) in a distinct, well-spaced secondary line.
4. Elevate the personal quote display to be the artistic focal point of the card:
   - Use an elegant serif italic typeface (e.g. *Playfair Display* or custom font).
   - Wrap the quote in beautiful, stylized quotation marks or enclose it in a subtle, classic decorative box.
5. Add rich hover animations: when a user hovers over a graduate's profile card, it should execute a smooth collegiate "focus" animation (e.g., a warm ambient shadow glow, clean border expansion, or page-lift transition).
6. Implement a client-side search bar and program-based filter dropdown at the top of the yearbook page to allow users to quickly search for peers by name or filter by department/program (e.g., CS, IT).

## Acceptance Criteria

- Graduate profiles render five core elements: Photo, Name, Position, Graduate Program, and Quote.
- Academic programs (e.g. BS Computer Science) are fully integrated into `src/lib/data/officers.json` and rendered on each card.
- Cards feature a warm, tactile, rectangular book-like design instead of a corporate circle grid.
- Personal quotes are prominently showcased with elegant, classic styling.
- A functional search and filter system is present at the top of the page, allowing instant searching by name or filtering by program.
- The entire page responds beautifully to interactions and scales across all screen sizes.
