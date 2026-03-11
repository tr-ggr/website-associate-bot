# Live Stream Channel

## Problem

There is currently no way to watch live streams of intramural games directly within the platform. A dedicated section or channel for live streams is needed to increase engagement.

## Potentially Related Files

- [prisma/schema.prisma](../app/prisma/schema.prisma) — Potential addition of `streamUrl` to Match or Sport model
- [app/(public)/schedule/page.tsx](../app/app/(public)/schedule/page.tsx) — Where streams might be linked
- [components/public/schedule/match-card.tsx](../app/components/public/schedule/match-card.tsx) — Potential UI for stream link

## What to Fix

1. Add a `streamUrl` field to the `Match` model in `schema.prisma`.
2. Update the admin dashboard to allow moderators to set or update the stream URL for live matches.
3. Create a "Live" badge and link in the schedule and home page for matches that are currently streaming.
4. Implement a simple embedded player or redirect button for the stream.

## Acceptance Criteria

- Admins can add stream URLs to matches.
- Users can see a clear "Watch Live" link for active streams.
- Clicking the link takes the user to the stream or opens an embedded player.
