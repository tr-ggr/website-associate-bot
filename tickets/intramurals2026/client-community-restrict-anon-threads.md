# Anonymous users should not be able to create a thread

## Problem

Currently, both authenticated and anonymous users can create threads in the community section. To maintain quality and accountability, thread creation should be restricted to authenticated users only.

## Potentially Related Files

- [components/public/community/new-thread-form.tsx](../app/components/public/community/new-thread-form.tsx) — Thread creation UI
- [actions/thread.ts](../app/actions/thread.ts) — `createThread` server action
- [lib/auth/index.ts](../app/lib/auth/index.ts) — Auth utility functions

## What to Fix

1. Update `new-thread-form.tsx` to check for user authentication before showing the form.
2. Add a login prompt or hide the "Start a new thread" button for anonymous users.
3. Modify the `createThread` action in `thread.ts` to require a valid session/profile; throw an error if the user is not logged in.
4. Update the UI to clearly indicate that login is required to post.

## Acceptance Criteria

- Anonymous users cannot see or access the thread creation form.
- The `createThread` server action rejects requests without an authenticated user.
- A clear call-to-action to login is shown where the thread form would be.
