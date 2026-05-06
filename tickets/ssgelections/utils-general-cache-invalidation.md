# Implement Proper Cache Invalidation with Cache Tags

**[CRITICAL]**

## Problem

The cache invalidation system has two issues:

**1. Missing route:** `refreshAll()` in [app/actions/admin.ts](../app/actions/admin.ts) calls `revalidatePath` for many admin routes but is missing `/admin/candidates`. This means creating, updating, or deleting a candidate does not refresh the admin candidates list — admins see stale data.

**2. No cache tag strategy:** The project relies entirely on `revalidatePath` with `force-dynamic` pages. Next.js documentation recommends using `revalidateTag` for shared data, because `revalidatePath` only refreshes the specified route — other pages consuming the same data remain stale. For example, updating a candidate's stands on the admin page should invalidate stands data on both `/candidates` and `/stands`, but with `revalidatePath` each route must be listed individually, and data functions don't use cache tags at all.

## Potentially Related Files

- [app/actions/admin.ts](../app/actions/admin.ts) — Lines 87–100: `refreshAll()` function and all server actions that call it
- [lib/data/public.ts](../lib/data/public.ts) — Public data fetchers for home, candidates, timeline, results
- [lib/data/admin.ts](../lib/data/admin.ts) — Admin data fetchers for reference data and stands
- [lib/facebook.ts](../lib/facebook.ts) — Line 48: Existing `fetch` with `next: { revalidate: 300 }` (reference pattern)
- [app/(admin)/admin/candidates/page.tsx](../app/(admin)/admin/candidates/page.tsx) — Admin candidates page affected by missing revalidation

## What to Fix

1. Add `revalidatePath("/admin/candidates")` to the `refreshAll()` function immediately
2. Introduce `unstable_cache` in data fetchers (`lib/data/public.ts`, `lib/data/admin.ts`) with explicit cache tags:
   - `candidates` — for candidate data
   - `parties` — for party data
   - `stands` — for stand questions, stance options, and candidate stands
   - `results` — for election results and turnout
   - `timeline` — for timeline events
   - `departments` — for department data
   - `settings` — for site settings
3. Refactor `refreshAll()` to call `revalidateTag` for the specific entity affected by each mutation, plus `revalidatePath` for the primary page route
4. Remove redundant/all-encompassing `revalidatePath` calls from `refreshAll()` in favor of targeted invalidation per action
5. Ensure pages still using `force-dynamic` remain functional

## Acceptance Criteria

- Editing a candidate on `/admin/candidates` immediately reflects on `/admin/candidates` without manual refresh
- Updating stands, parties, or results invalidates data across all consuming pages (public + admin)
- `revalidateTag` is used for shared data entities; `revalidatePath` is used as a complement for page-specific layout revalidation
- No stale data remains visible on any public or admin page after a mutation
- Server actions remain functional and error-free
