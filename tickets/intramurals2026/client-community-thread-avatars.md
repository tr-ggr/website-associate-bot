# Threads have picture of the poster

## Problem

Community threads and replies currently only show the display name or "Anonymous". Showing the profile picture (avatar) of the user will make the community feel more personal and vibrant.

## Potentially Related Files

- [prisma/schema.prisma](../app/prisma/schema.prisma) — Profile model `imageUrl`
- [actions/thread.ts](../app/actions/thread.ts) — Need to include `author` relation in fetch
- [components/public/community/thread-list.tsx](../app/components/public/community/thread-list.tsx) — Main list UI
- [components/public/community/thread-detail.tsx](../app/components/public/community/thread-detail.tsx) — Detail view and reply UI

## What to Fix

1. Update `getThreads` and `getThreadById` in `thread.ts` to include the `author` relation and select the `imageUrl`.
2. Modify thread and reply components to display the `imageUrl` in an `Avatar` component.
3. Handle the "Anonymous" case by showing a default system avatar.
4. Ensure the UI remains responsive and the images are appropriately sized.

## Acceptance Criteria

- Threads posted by authenticated users show their profile picture.
- Replies show the poster's profile picture.
- Anonymous posts show a placeholder avatar.
