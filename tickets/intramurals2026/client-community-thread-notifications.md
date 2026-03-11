# Notification on threads

## Problem

Users currently have no way of knowing when someone replies to their thread or likes their post unless they manually check the community section. This limits interactivity.

## Potentially Related Files

- [prisma/schema.prisma](../app/prisma/schema.prisma) — Need a `Notification` model
- [actions/thread.ts](../app/actions/thread.ts) — Hook into `createReply` and `toggleLikeThread`
- [components/public/navbar.tsx](../app/components/public/navbar.tsx) — Notification bell UI

## What to Fix

1. Design and implement a `Notification` model in Prisma.
2. Update thread and reply actions to create a notification record when a user interacts with another's post.
3. Create a notification component in the navbar to show unread counts.
4. Build a notification dropdown or page for users to view their alerts.

## Acceptance Criteria

- Users receive a notification when their thread gets a reply.
- Users receive a notification when their thread is liked.
- A notification indicator (bell icon) shows the number of unread alerts in the navbar.
