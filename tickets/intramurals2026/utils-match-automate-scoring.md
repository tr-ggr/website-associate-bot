# Automate Team Scoring after Match Win

## Problem

Currently, when a match winner is set, the team's overall standings/points are not automatically updated if they rely on a persistent standing table. Although standings are computed on the fly, some sports might need explicit score accumulation.

## Potentially Related Files

- [actions/match.ts](../app/actions/match.ts) — `setWinner` function
- [actions/analytics.ts](../app/actions/analytics.ts) — Analytics and standings logic
- [lib/data/compute-standings.ts](../app/lib/data/compute-standings.ts) — Core standings computation

## What to Fix

1. Update the `setWinner` action in `match.ts` to trigger a revalidation of standings data.
2. If persistent scoring is implemented, ensure the winning team's points/wins are incremented correctly.
3. Automate the transition of match status to "COMPLETED" and ensure the bracket advances immediately.
4. Ensure cache tags for standings are purged upon match completion.

## Acceptance Criteria

- Setting a winner automatically reflects in the standings page without manual intervention.
- The bracket advances correctly and automatically.
- STANDINGS data is accurate immediately after a match concludes.
