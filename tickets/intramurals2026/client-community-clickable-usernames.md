# Clickable Link of the username of a thread poster

## Problem

Users cannot easily visit the profile of someone who posted a thread or a reply. Usernames should be clickable links that navigate to the user's public profile page.

## Potentially Related Files

- [app/(public)/[username]/page.tsx](../app/app/(public)/[username]/page.tsx) — Target profile route
- [components/public/community/thread-list.tsx](../app/components/public/community/thread-list.tsx) — Where name is displayed
- [components/public/community/thread-detail.tsx](../app/components/public/community/thread-detail.tsx) — Where name is displayed

## What to Fix

1. Wrap the poster's display name or username in a `Link` component.
2. Ensure the link points to the dynamic route `/[username]`.
3. If the user is anonymous, the name should **not** be clickable.
4. Apply consistent hover effects to indicate that the name is a link.

## Acceptance Criteria

- Clicking a poster's name navigates the user to that person's profile page.
- Anonymous names are not clickable.
- Links work correctly for both threads and replies.
