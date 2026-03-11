# Implement Predictions Leaderboard

## Problem

There's no competitive element to predictions. A leaderboard showing the users with the most correct predictions would increase user engagement and platform activity.

## Potentially Related Files

- [app/(public)/predictions/leaderboard/page.tsx](../app/app/(public)/predictions/leaderboard/page.tsx) — New leaderboard page
- [actions/prediction.ts](../app/actions/prediction.ts) — Helper for prediction-based analytics
- [components/public/predictions/leaderboard-table.tsx](../app/components/public/predictions/leaderboard-table.tsx) — Leaderboard UI component

## What to Fix

1. Create a `getPredictionsLeaderboard` server action to fetch users sorted by their successful prediction count.
2. Build a new page to display the leaderboard in a table format.
3. Include rank, username, profile picture (if any), and total wins.
4. Implement tabs or filters for "All Time", "This Week", or "By Sport".

## Acceptance Criteria

- A public predictions leaderboard is accessible to all users.
- Users are ranked correctly based on their correct prediction count.
- The UI is clean, responsive, and easy to read.
