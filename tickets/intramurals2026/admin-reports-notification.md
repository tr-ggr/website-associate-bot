# Report notification

## Problem

Admins currently have to manually check the reports dashboard to see if anything has been flagged. This leads to delays in moderation. Admins should receive an alert or notification when a new report is submitted.

## Potentially Related Files

- [actions/report.ts](../app/actions/report.ts) — `submitReport` server action
- [app/admin/(dashboard)/reports/page.tsx](../app/app/admin/(dashboard)/reports/page.tsx) — Admin reports view
- [components/public/navbar.tsx](../app/components/public/navbar.tsx) — Notification system for admins

## What to Fix

1. Modify `submitReport` in `report.ts` to trigger a notification for all users with the ADMIN role.
2. Integrate with the (planned) notification system to send a real-time alert (via Toast or Notification record).
3. Ensure the report record correctly identifies the reporter and the target.
4. Add a summary indicator in the admin dashboard showing the count of "PENDING" reports.

## Acceptance Criteria

- Admins receive a real-time notification or see an updated badge count when a new report is filed.
- The notification links directly to the moderation/report details page.
