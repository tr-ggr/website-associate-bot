# Fix Teams not showing up on prod

**[CRITICAL]**

## Problem

Teams are currently not appearing on the production environment standings page, even though they exist in the database and show up correctly in development. This prevents users from seeing team rankings and logos.

## Potentially Related Files

- [app/(public)/standings/page.tsx](../app/app/(public)/standings/page.tsx) — Main standings logic
- [lib/data/compute-standings.ts](../app/lib/data/compute-standings.ts) — Standings calculation logic
- [prisma/schema.prisma](../app/prisma/schema.prisma) — Team model definition

## What to Fix

1. Investigate `standings/page.tsx` for any environment-specific filters or data fetching issues.
2. Check if there are any missing relations or fields required by the UI that might be empty on prod.
3. Verify if `computeStandings` handles empty match sets correctly without hiding teams.
4. Ensure the database connection and prisma client are correctly configured for the production environment.

## Acceptance Criteria

- Teams are visible on the standings page in the production environment.
- Team logos and names are rendered correctly.
- Overall standings are calculated and displayed.
