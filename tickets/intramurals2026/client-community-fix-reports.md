# Fix Reported thread not working

## Problem

Reports submitted for threads are currently not causing the threads to be hidden or flagged correctly in the UI. Admins might see the report, but the public view still shows potentially problematic content.

## Potentially Related Files

- [actions/thread.ts](../app/actions/thread.ts) — Thread fetching logic
- [actions/report.ts](../app/actions/report.ts) — `resolveReport` logic
- [components/public/community/thread-list.tsx](../app/components/public/community/thread-list.tsx) — Main list display

## What to Fix

1. Investigate why the `isRemoved` or `isDeleted` flag is not being set when a report is actioned by an admin.
2. Update `getThreads` and `getRecentThreads` to strictly filter out threads where `isRemoved` is true.
3. Ensure that if a report is marked as "RESOLVED" (confirmed violation), the `Thread` record is updated to `isRemoved = true`.
4. Fix any UI state issues where a reported thread remains in the cached results.

## Acceptance Criteria

- Threads marked as "REMOVED" by admins are immediately hidden from public view.
- Resolving a report as valid correctly updates the thread status in the database.
- Community list revalidates after a report is actioned.
