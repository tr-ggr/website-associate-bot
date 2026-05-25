# Instructions: Generate `ticket-guidelines.md` for This Project

You are an AI assistant. Your task is to produce **one file** named `ticket-guidelines.md` at the **root of the project you are currently working in**. That file will guide humans + future AI sessions on how to author markdown tickets for this project.

The tickets you describe must remain machine-parseable by the upstream Discord bot `website-associate-bot` (its parser in `ticket_loader.py` uses literal regexes against the section headings — do not rename or rephrase them).

Do **not** create any actual tickets. Do **not** create the `tickets/` directory yet. Only produce `ticket-guidelines.md`.

---

## Step 1 — Scan the project before writing

Before writing a single line of the guideline, gather context from the project root:

1. Read whichever of these exist:
   - `README.md`
   - `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, or any agent-instruction file
   - `package.json` (Node), `requirements.txt` / `pyproject.toml` (Python), `Cargo.toml` (Rust), `go.mod` (Go), `Gemfile` (Ruby), `composer.json` (PHP), `pubspec.yaml` (Flutter)
2. List top-level directories. Note presence of any of: `src/`, `app/`, `apps/`, `packages/`, `components/`, `actions/`, `routes/`, `api/`, `prisma/`, `migrations/`, `supabase/`, `lib/`, `utils/`, `tests/`.
3. From the above, infer:
   - **Language(s)** (TypeScript, Python, Go, etc.)
   - **Framework(s)** (Next.js, FastAPI, NestJS, Django, Rails, Expo, etc.)
   - **Database / ORM** (Prisma, Drizzle, SQLAlchemy, ActiveRecord, raw SQL, Supabase, etc.)
   - **UI layer** (React + shadcn, Vue, SwiftUI, native Android, etc.) — skip if backend-only
   - **Convention for backend logic** (server actions, controllers, routers, handlers)
4. If `tickets/` does not yet exist at root, mention in the guideline that the user should create it before running `/load-tickets`.

Use this scan to populate **real, project-specific** file paths in the example ticket. Generic placeholders like `components/Foo.tsx` are not acceptable when a real `apps/web/src/components/` exists.

---

## Step 2 — Required parser-compatible format (non-negotiable)

The output `ticket-guidelines.md` must instruct authors to use this exact structure. The bot's parser (`ticket_loader.py`) keys off these literal strings:

| Section | Heading (exact) | Body format |
|---|---|---|
| Title | `# <title>` (H1, first line) | single line |
| Priority (optional) | own line: `**[PRIORITY]**` or `**[CRITICAL]**` | nothing else |
| Problem | `## Problem` | free prose, ends at next `##` |
| Related files | `## Potentially Related Files` | bullet list, each line starts with `- ` |
| Steps | `## What to Fix` | **numbered list**, each line `1.`, `2.`, … (regex requires `^\d+\.\s+`) |
| Done criteria | `## Acceptance Criteria` | bullets `- ` / `* ` **or** numbered `1.` |

State explicitly in the guideline:
- Heading text must match exactly (case, spelling, no trailing punctuation).
- `## What to Fix` **must** be a numbered list — bullets here will not parse.
- Only one H1 per file; subsequent `# ...` lines will confuse the title extractor.
- Only `**[PRIORITY]**` and `**[CRITICAL]**` are recognized priority markers.

---

## Step 3 — Filename + location convention

Tell authors:

- Tickets live under `tickets/<project-slug>/`.
- `<project-slug>` is a short kebab-case name for the project (e.g. `myapp`, `client2026`).
- Each ticket filename: `<area>-<feature>.md`
  - `<area>` is one of exactly: `client`, `admin`, `utils`
    - `client` = end-user / public-facing UI
    - `admin` = internal admin / staff UI
    - `utils` = infra, scripts, migrations, scheduled jobs, shared libs
  - `<feature>` = kebab-case, concise (`login-register`, `pdf-export`, `hazard-pin-submission`)
- Examples to put in the guideline (adapt area names to project reality if needed, but keep the three prefixes):
  - `client-navbar-remove-sports.md`
  - `admin-reports-pdf-export.md`
  - `utils-seed-script.md`

---

## Step 4 — Tailor the example ticket to the scanned stack

The guideline must include **one full example ticket** using **real file paths and frameworks discovered in Step 1**. Rules for the example:

- Pick a plausible feature for this project's domain (read README for clues — e-commerce, mapping, elections, scheduling, etc.).
- In `## Potentially Related Files`, list 3–6 real paths from this repo. Use relative links: `[name.ext](relative/path/to/name.ext)`. Include line ranges (`#L18-L20`) where helpful.
- In `## What to Fix`, mention the actual framework primitives (e.g. "server action", "FastAPI router", "Prisma migration", "Rails controller") — not generic terms.
- Keep the example tight: ≤ 6 fix steps, ≤ 5 acceptance criteria.

---

## Step 5 — Content rules to include verbatim in the guideline

Copy these rules into the output:

- **One problem per ticket.** Split unrelated issues into separate files.
- **Explain why**, not just what. The `## Problem` section should describe impact and current vs. desired state.
- **Link, don't dump.** Reference files via markdown links; never paste large code blocks.
- **Be specific.** Mention line numbers, function names, and dependency versions when relevant.
- **Acceptance criteria must be testable.** A QA reader should be able to verify each one with concrete action.
- **Priority markers are rare.** `**[PRIORITY]**` = blocks other work / MVP-critical. `**[CRITICAL]**` = prod outage. No marker = normal.
- **No questions as tickets.** Discuss first; file a ticket only when there is a concrete fix to make.

---

## Step 6 — Tell authors what NOT to do

The guideline should include a `## Don'ts` (or similar) section warning against:

- Renaming or translating the four `## ` section headings.
- Using bullets for `## What to Fix`.
- Multiple H1s in one file.
- Pasting long code snippets instead of linking.
- Combining several features into one file.
- Vague titles like "fix bugs" or "improve UI".
- Filenames missing the `client-` / `admin-` / `utils-` prefix.

---

## Step 7 — Output requirements

When you write `ticket-guidelines.md`:

1. Place it at the project root (sibling of `README.md`).
2. If a file by that name already exists, stop and ask the user whether to overwrite, merge, or rename.
3. The output file should contain, in order:
   - Short intro (1–3 lines) naming the project and pointing to `tickets/<slug>/`.
   - "When to create a ticket" list.
   - Required format table or section list (copy from Step 2).
   - Filename convention (Step 3).
   - The example ticket tailored to this project (Step 4).
   - Content rules (Step 5).
   - Don'ts (Step 6).
   - Closing note: tickets are consumed by an upstream Discord bot via `/load-tickets <folder> <channel>`; any deviation from the section headings will break parsing.
4. Use plain GitHub-flavored markdown. No HTML, no frontmatter.
5. Do **not** create example ticket files on disk. The example lives inside `ticket-guidelines.md` as a fenced code block.

---

## Reference template for the example ticket inside `ticket-guidelines.md`

Use this skeleton, replacing every angle-bracket placeholder with values discovered in Step 1:

````markdown
# <Concrete, action-oriented title>

**[PRIORITY]**   <!-- optional; remove if normal priority -->

## Problem

<2–4 sentences. What is broken or missing, who is affected, what should happen instead.>

## Potentially Related Files

- [<file>](<relative/path>) — <what's in it; optional line range>
- [<file>](<relative/path>) — <…>
- [<file>](<relative/path>) — <…>

## What to Fix

1. <Concrete step using real framework verbs>
2. <Next step>
3. <Next step>

## Acceptance Criteria

- <Testable condition>
- <Testable condition>
- <Testable condition>
````

---

## Self-check before you finish

Before declaring the task done, verify the file you wrote satisfies all of:

- [ ] Saved as `ticket-guidelines.md` at the project root.
- [ ] All four section headings appear verbatim: `## Problem`, `## Potentially Related Files`, `## What to Fix`, `## Acceptance Criteria`.
- [ ] `## What to Fix` is described as a numbered list (not bullets).
- [ ] Filename convention `<client|admin|utils>-<feature>.md` is stated.
- [ ] Example ticket uses real file paths from this repository, not placeholders.
- [ ] No actual ticket files were created.
- [ ] No existing project files outside `ticket-guidelines.md` were modified.
