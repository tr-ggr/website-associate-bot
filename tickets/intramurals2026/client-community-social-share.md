# Facebook Share button and Twitter button

## Problem

The current share functionality only copies the link to the clipboard. Adding direct share buttons for Facebook and Twitter (X) will make it easier for users to promote community discussions on social media.

## Potentially Related Files

- [components/public/community/share-button.tsx](../app/components/public/community/share-button.tsx) — Share button UI and logic
- [actions/facebook.ts](../app/actions/facebook.ts) — Potential helper for FB sharing
- [lib/utils.ts](../app/lib/utils.ts) — URL generation helpers

## What to Fix

1. Update `share-button.tsx` to include Facebook and Twitter icons/buttons.
2. Implement sharing intent URLs for both platforms.
3. Ensure the current thread URL is correctly encoded and passed to the sharing dialogs.
4. Improve the visual styling of the share options (e.g., in a small popover or horizontal list).

## Acceptance Criteria

- Users can click a Facebook icon to open the FB share dialog for the current thread.
- Users can click a Twitter icon to open the Twitter share dialog for the current thread.
- The shared link correctly points to the specific thread page.
