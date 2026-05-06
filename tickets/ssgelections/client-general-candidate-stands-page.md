# Implement Public Candidate Stands Comparison Page

## Problem

Voters can only see candidate stands (stances on issue questions) embedded inside individual `CandidateCard` components on the `/candidates` page. There is no way to compare all candidates' positions on a specific issue side-by-side. The public navigation also lacks a link to a dedicated stands view, making this important election information hard to discover.

Currently, the data layer (`getPublicCandidatesData()` in [lib/data/public.ts](../lib/data/public.ts)) already fetches `stand_questions`, `candidate_stands`, and `stance_options` and enriches each candidate with their stands. However, the only consumer of this enriched data is the candidates page.

## Potentially Related Files

- [lib/data/public.ts](../lib/data/public.ts) — Lines 88–135: `getPublicCandidatesData()` already fetches stands data and could be leveraged or extended for the stands page
- [components/ui/candidate-card.tsx](../components/ui/candidate-card.tsx) — Lines 79–101: Existing stands display inside candidate cards (reference for stance badge styling)
- [components/public-nav.tsx](../components/public-nav.tsx) — Lines 6–10: Navigation links array; needs a new "Stands" entry
- [app/(public)/stands/page.tsx](../app/(public)/stands/page.tsx) — New route page (to be created)
- [app/(public)/layout.tsx](../app/(public)/layout.tsx) — Public layout with `PublicNav`

## What to Fix

1. Create `app/(public)/stands/page.tsx` with `export const dynamic = "force-dynamic"`
2. Fetch data: candidates (with party, position, dept), `stand_questions`, `candidate_stands`, `stance_options`
3. Build a matrix layout:
   - **Rows:** `stand_questions` ordered by created_at
   - **Columns:** Candidates grouped by position (each position is a section)
   - **Cells:** Stance badge (color from `stance_options`) or "—" if no stance assigned
4. Show candidate name, party badge, and year/dept as column headers
5. Add horizontal scroll wrapper for mobile responsiveness
6. Add empty state handling: no questions, no candidates, or no stances assigned
7. Add "Stands" link to `components/public-nav.tsx` navigation array (position between "Candidates" and "Results")

## Acceptance Criteria

- `/stands` route is accessible and renders a side-by-side comparison matrix of all candidates and stances
- Candidates are visually grouped by their position (e.g., "President", "Vice President")
- Each question appears as a row with candidate stance badges in the corresponding columns
- Stance badges display the configured label and color from `stance_options`
- Candidates with no stance on a question show "—" instead of a badge
- "Stands" link appears in the public navigation between "Candidates" and "Results"
- The active link highlighting works for `/stands`
- The page is horizontally scrollable on narrow/mobile screens
- Empty state renders gracefully when no questions or candidates exist
