# Fix Photo Upload: Orphaned Storage Files and Missing Validation

**[PRIORITY]**

## Problem

The photo upload system has three issues:

**1. Orphaned storage files:** When a candidate's photo is updated (or a party's logo), the `uploadImage()` function uploads the new file to Supabase Storage but never deletes the old file. This causes unbounded storage growth as orphaned files accumulate in `candidate-assets` and `party-assets` buckets.

**2. No server-side validation:** `uploadImage()` accepts any `File` object without checking file size or MIME type. A user could upload a 100MB video or a non-image file, which would either fail opaquely at the Supabase level or waste storage.

**3. Missing `contentType`:** The Supabase upload call does not pass `contentType`, which means Supabase infers it from the file extension, potentially leading to incorrect content type headers on the stored object.

## Potentially Related Files

- [app/actions/admin.ts](../app/actions/admin.ts) — Lines 55–85: `uploadImage()` helper; Lines 102–138: `upsertPartyAction()`; Lines 150–189: `upsertCandidateAction()`
- [app/(admin)/admin/candidates/inline-table.tsx](../app/(admin)/admin/candidates/inline-table.tsx) — Lines 94–103: Inline edit form with photo upload (needs error display)
- [app/(admin)/admin/candidates/page.tsx](../app/(admin)/admin/candidates/page.tsx) — Lines 68–71: Create candidate form with photo upload
- [supabase/migrations/202604180001_init.sql](../supabase/migrations/202604180001_init.sql) — Lines 214–218: Bucket creation (needs `allowedMimeTypes` / `fileSizeLimit`)
- [lib/supabase/env.ts](../lib/supabase/env.ts) — Supabase environment configuration

## What to Fix

1. **Delete old files on update:**
   - In `upsertCandidateAction`, when `payload.id` exists and a new photo is uploaded, query the existing candidate's `photo_url`, extract the storage path, and call `supabase.storage.from("candidate-assets").remove([path])` before saving the new URL
   - In `upsertPartyAction`, apply the same logic for `logo_url` in `party-assets`

2. **Add upload validation to `uploadImage()`:**
   - Reject files larger than 5MB with a descriptive error
   - Reject files with MIME types other than `image/jpeg`, `image/png`, `image/webp`
   - Pass `contentType: file.type` to the Supabase `upload()` options

3. **Improve error propagation:**
   - Return user-friendly error messages from `uploadImage()` instead of a generic throw
   - Ensure the inline edit form in `inline-table.tsx` catches and displays these errors

4. **Harden bucket configuration:**
   - Create a new migration (or update an existing one) to set `allowedMimeTypes: ['image/*']` and `fileSizeLimit: '5MB'` on both `party-assets` and `candidate-assets` buckets

## Acceptance Criteria

- Updating a candidate's photo deletes the old file from the `candidate-assets` Supabase Storage bucket
- Updating a party's logo deletes the old file from the `party-assets` Supabase Storage bucket
- Uploading a file larger than 5MB returns a clear error: "File must be under 5MB"
- Uploading a non-image file (e.g., `.pdf`, `.exe`) returns a clear error: "Only JPEG, PNG, and WebP images are allowed"
- The inline candidate edit form displays upload errors to the admin user
- New candidates can still be created without a photo (existing behavior preserved)
- Supabase bucket configuration restricts uploads to images only, with a 5MB cap
