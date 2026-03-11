# Have Predictions won on Profile

## Problem

Users want to see how successful they've been with their match predictions. A "Predictions Won" count should be visible on their public and private profile pages.

## Potentially Related Files

- [prisma/schema.prisma](../app/prisma/schema.prisma) — `MatchPrediction` and `Match` models
- [actions/profile.ts](../app/actions/profile.ts) — `getProfile` or `getPublicProfile`
- [components/public/profile/profile-info.tsx](../app/components/public/profile/profile-info.tsx) — Profile stats UI

## What to Fix

1. Update the logic for fetching profiles to count how many `MatchPrediction` records an user has that match the `winnerId` of the corresponding `Match`.
2. Add a `predictionsWonCount` field to the profile data object.
3. Update the profile UI to show this count alongside other stats (like threads, likes).
4. Implement a simple "Accuracy" percentage (Wins / Total Predictions).

## Acceptance Criteria

- Profile pages display the number of correctly predicted matches.
- The count is accurate and updates when a match is completed.
- The stat is visible to both the owner and other users (if profile is public).
