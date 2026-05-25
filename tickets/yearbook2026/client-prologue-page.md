# Create a dedicated Prologue page for the graduation journal

## Problem

The website currently lacks a dedicated Prologue page. Although the footer has a navigation link for "The Prologue", it currently redirects users to the homepage (`/`). A premium graduation website needs an introductory prologue page that sets a literary, emotional, and elegant tone, serving as a welcoming preface for the Class of 2026. This page should feel like an opening chapter of a beautifully bound physical book.

## Potentially Related Files

- [src/components/layout/Footer.tsx](src/components/layout/Footer.tsx) — Contains the dummy "The Prologue" link that currently points to `/` (line 38).
- [src/components/layout/Navbar.tsx](src/components/layout/Navbar.tsx) — Main navigation header (may need a Prologue link or update).
- [src/app/prologue/page.tsx](src/app/prologue/page.tsx) — New file to be created for the Prologue page.

## What to Fix

1. Create a new Next.js route directory `src/app/prologue/` and initialize a new page file `page.tsx`.
2. Design a premium, book-inspired layout for the Prologue page featuring a high-contrast serif font (e.g. *Playfair Display*, *Cormorant Garamond*, or *Lora*) loaded via Google Fonts.
3. Center the content inside an elegant, single-column reading column with wide margins to resemble a luxury novel or journal page.
4. Implement a gorgeous, oversized first-letter drop cap (`initial-letter` or custom CSS float styling) to start the prologue text with visual flair.
5. Structured contents should include:
   - An atmospheric epigraph or short quote at the top (italicized, smaller serif).
   - A warm, formal opening letter addressed to the graduates, peers, and mentors of the Class of 2026.
   - An elegant signature line at the bottom (e.g., "The Editorial Board, Class of 2026").
   - A smooth, flowing call-to-action button or link (e.g., "Open the Yearbook" or "Read the Profiles") to seamlessly guide readers to `/yearbook`.
6. Add subtle page entrance animations (e.g., fade-in and a gentle slide-up) for the header and body text so that it transitions into view with premium polish.
7. Update the navigation link in `src/components/layout/Footer.tsx` (and `src/components/layout/Navbar.tsx` if necessary) to point "The Prologue" to `/prologue`.

## Acceptance Criteria

- Navigating to `/prologue` loads a gorgeous, dedicated preface page.
- The typography uses an elegant, book-like serif font with balanced margins and a stylized drop cap for the first paragraph.
- The footer link for "The Prologue" successfully navigates to `/prologue` instead of `/`.
- The page includes a clear call-to-action button guiding visitors to the yearbook section.
- Content elements and typography are completely responsive and scale beautifully on mobile devices.
