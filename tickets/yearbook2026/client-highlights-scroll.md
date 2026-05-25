# Redesign Highlights section into a casual scrollable timeline

## Problem

The current Highlights section displays events as a rigid, formal, three-column grid of cards. This layout feels overly business-like and corporate, conflicting with the friendly, intimate, and nostalgic vibe of a graduation journal. To achieve a better balance between formal school events and friendly, casual memories, we need to restructure this section into an immersive, continuous vertical scroll timeline that takes the user on a chronological journey through the academic year.

## Potentially Related Files

- [src/app/highlights/page.tsx](src/app/highlights/page.tsx) — Main page rendering the highlights grid (lines 12-22).
- [src/app/globals.css](src/app/globals.css) — Custom styles for scrollbars, timeline tracks, and path drawing.

## What to Fix

1. Overhaul the page layout in `src/app/highlights/page.tsx` by replacing the rigid static grid with a centered, organic vertical timeline line (using dashed patterns, warm amber color gradients, or a hand-drawn look).
2. Position highlight event cards alternately on the left and right sides of the timeline track, creating a dynamic, engaging, and well-balanced flow as the user scrolls.
3. Redesign the highlight event cards with a warm, casual, scrapbook-like aesthetic:
   - Use irregular rounded corners (`border-radius: 20px 40px 20px 30px`) or slight organic rotations to make them feel friendly.
   - Embed polaroid-style image attachments with handwriting labels (e.g. "Senior Ball 2026", "Late Night Editorial Beats") hanging off the card.
   - Attach subtle decorative elements like virtual washi tape or pin clips holding the event descriptions.
4. Implement scroll-triggered animations (e.g. using simple CSS classes, Intersection Observer, or Tailwind transition utilities) so the timeline track fills up and event cards slide/fade into place elegantly as the user scrolls down the page.
5. Infuse narrative storytelling into each highlight event card, including informal "behind-the-scenes" quotes, candidate stories, and student-taken photographs alongside official descriptions.
6. Design a responsive mobile version that collapses the alternate left-right card layout into a clean, unified single-column vertical timeline that preserves the friendly, scrapbook-style elements.

## Acceptance Criteria

- The rigid multi-column grid is replaced with a single continuous vertical timeline that scrolls all the way down.
- Cards feature a highly casual, friendly scrapbook-inspired design (polaroids, irregular borders, handwritten details) to offset formal event descriptions.
- Event cards display alternately on the left and right sides of the timeline track on desktop viewports.
- Event cards and the timeline track animate smoothly into view upon scroll-reveal.
- Mobile layout collapses elegantly into a highly legible, single-column scrollable timeline.
