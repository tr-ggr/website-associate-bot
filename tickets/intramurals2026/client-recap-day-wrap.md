# Intrams Day Wrap (Murag Spotify)

## Problem

Users want a summary of the day's highlights, winners, and trending topics, presented in a visually engaging "Spotify Wrap" style format. This provides a sense of closure and excitement for each day of the event.

## Potentially Related Files

- [app/(public)/page.tsx](../app/app/(public)/page.tsx) — Potential location for the wrap component
- [actions/analytics.ts](../app/actions/analytics.ts) — Data gathering for the day's events
- [lib/data/compute-standings.ts](../app/lib/data/compute-standings.ts) — Standing changes for the day

## What to Fix

1. Create a `Recap` or `DayWrap` component with a slide-based or interactive visual style.
2. Fetch data specifically for "today's" completed matches, top scorers (if available), and most liked threads.
3. Implement animations and a mobile-friendly layout for the "Wrap" slides.
4. Add a button or banner to the home page to trigger the Day Wrap overlay.

## Acceptance Criteria

- A visually stunning "Day Wrap" is accessible at the end of each event day.
- It summarizes key results: "Team X won Y matches", "Most discussed topic: Z", etc.
- Responsive design that feels premium and engaging.
