# Discord Ticket Management Bot

A Discord bot for managing support tickets organized by folder and channel. Track ticket statuses with role-based workflows and maintain separate leaderboards for Developers and QAs.

## Features

✨ **Ticket Management**
- Load tickets from markdown files organized in folders
- Create Discord threads for each ticket with status prefixes
- Parse detailed ticket information (problem, steps, acceptance criteria)
- Track ticket status: `[OPEN]`, `[CLAIMED]`, `[Pending-Review]`, `[Reviewed]`, `[CLOSED]`

👥 **Role-Based Workflow**
- **Developers:** Claim tickets and mark as Pending-Review
- **QAs:** Review and approve completed tickets
- Users can have both roles simultaneously
- Use `/set-role` to assign roles

📊 **Role-Based Leaderboards**
- Developer leaderboard: Tracks tickets marked as pending review
- QA leaderboard: Tracks tickets reviewed and approved
- Separate scoring for each role
- View with `/leaderboard dev` or `/leaderboard qa`

🗂️ **Folder Organization**
- Organize tickets into different folders (e.g., `support/`, `bugs/`, `features/`)
- Load tickets from any folder into any Discord channel
- Flexible folder structure

## Workflow

1. **Load Tickets:** `/load-tickets <folder> <channel>` creates threads from markdown files
2. **Developer Claims:** `/claim <thread>` → `[CLAIMED][username]ticket-name`
3. **Developer Submits:** `/resolved <thread>` → `[Pending-Review][username]ticket-name` (adds to dev leaderboard)
4. **QA Reviews:** `/reviewed <thread>` → `[Reviewed][username]ticket-name` (adds to QA leaderboard)
5. **Close Ticket:** `/closed <thread>` → `[CLOSED][username]ticket-name`

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file and add your Discord bot token:

```
DISCORD_TOKEN=your_bot_token_here
```

To get a bot token:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and click "Add Bot"
4. Copy the token and paste it in `.env`

### 3. Invite Bot to Server

1. In Developer Portal, go to "OAuth2" > "URL Generator"
2. Select scopes: `bot`, `applications.commands`
3. Select permissions: `Manage Channels`, `Manage Threads`, `Send Messages`, `Embed Links`
4. Copy the generated URL and open it in browser
5. Select your server and authorize

### 4. Create Ticket Folders

Create folders inside the `tickets/` directory with your ticket markdown files.

### 5. Run the Bot

```bash
python main.py
```

## Docker (uv)

Build the image:

```bash
docker build -t website-associate-bot .
```

Run the bot (loads `DISCORD_TOKEN` from your local `.env` file):

```bash
docker run --rm --env-file .env website-associate-bot
```

Optional: mount tickets if you want to edit them locally without rebuilding:

```bash
docker run --rm --env-file .env -v $(pwd)/tickets:/app/tickets website-associate-bot
```

## Commands

### `/set-role <developer|qa>`
Assign yourself a role. The Discord role will be created automatically.

**Parameters:**
- `role` - Choose `developer` or `qa`

**Example:**
```
/set-role developer
/set-role qa
```

### `/load-tickets <folder> <channel>`
Load all markdown files from a specified folder into a Discord channel.

**Parameters:**
- `folder` - Folder name within `tickets/` directory
- `channel` - Discord channel where threads will be created

**Example:**
```
/load-tickets support #support-squad
/load-tickets bugs #bug-reports
```

### `/claim`
Mark a ticket as claimed. Must be used **inside a ticket thread**. Only Developers can use this.

**Example workflow:**
1. Go to the ticket thread
2. Run `/claim` to claim it

### `/resolved`
Mark a ticket as pending review. Must be used **inside a ticket thread**. Only Developers can use this. Adds to developer leaderboard.

**Example workflow:**
1. Go to the ticket thread
2. Run `/resolved` to submit for QA review

### `/reviewed`
Approve a ticket after review. Must be used **inside a ticket thread**. Only QAs can use this. Adds to QA leaderboard.

**Requirements:**
- Ticket must be in Pending-Review status
- Only QAs can use this

**Example workflow:**
1. Go to the ticket thread (in Pending-Review status)
2. Run `/reviewed` to approve

### `/closed`
Mark a ticket as closed. Must be used **inside a ticket thread**.

**Example workflow:**
1. Go to the ticket thread
2. Run `/closed` to close the ticket

### `/leaderboard [role] [limit]`
Display the leaderboard for a specific role.

**Parameters:**
- `role` - `dev` for Developers (default) or `qa` for QAs
- `limit` - Number of top resolvers to show (default: 10, max: 50)

**Examples:**
```
/leaderboard dev
/leaderboard qa limit: 20
```

### `/ticket-folders`
List all available ticket folders in the `tickets/` directory.

### `/help`
Show comprehensive help information about all commands and workflows.

## Ticket Format

All ticket markdown files should follow this structure:

```markdown
# Ticket Title

**[PRIORITY]**

## Problem

Clear explanation of the issue, why it matters, and what needs to be fixed.

## Potentially Related Files

- File path and description
- File path and description

## What to Fix

1. First step
2. Second step
3. Third step

## Acceptance Criteria

- Testable condition 1
- Testable condition 2
- Testable condition 3
```

### Priority Markers (Optional)

- `**[PRIORITY]**` - Feature blocks other work, critical for MVP
- `**[CRITICAL]**` - Production bug, system broken

### Example Ticket

```markdown
# Add Daily Facebook Updates Banner to Home Page

## Problem

The home page hero section should include a prominent banner promoting daily updates from the official Facebook page. Currently, no Facebook integration or banner exists.

## Potentially Related Files

- [components/public/home/hero-section.tsx](../app/components/public/home/hero-section.tsx) — Main hero section
- [app/(public)/page.tsx](../app/app/(public)/page.tsx) — Home page entry point

## What to Fix

1. Create Facebook banner section in home page
2. Include a call-to-action button linking to Facebook page
3. Style banner to match existing branding
4. Add copy about daily updates
5. Position banner prominently
6. Make mobile-responsive

## Acceptance Criteria

- Facebook banner is visible on desktop and mobile
- Banner includes link to Facebook page
- Design matches existing aesthetic
- Button opens Facebook in new tab
```

## Database

The bot uses SQLite (`tickets.db`) to store:
- **Thread tracking** - Maps Discord threads to ticket information
- **User roles** - Developer and/or QA roles for each user
- **Leaderboard** - Separate scores for developers (pending reviews) and QAs (reviewed)

The database is automatically created and initialized on first run.

## Project Structure

```
website-associate-bot/
├── main.py                    # Main bot code with commands
├── config.py                  # Configuration and environment variables
├── database.py                # SQLite database operations
├── ticket_loader.py           # Markdown file parser
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (Discord token)
├── .gitignore                 # Git ignore patterns
├── tickets.db                 # SQLite database (auto-created)
└── tickets/                   # Ticket markdown files
    ├── support/
    │   ├── password-reset.md
    │   └── login-timeout.md
    ├── bugs/
    │   ├── button-overlap.md
    │   └── api-timeout.md
    └── features/
```

## Troubleshooting

**Bot doesn't respond to commands:**
- Verify bot has correct permissions in your server
- Check that `DISCORD_TOKEN` is set correctly in `.env`
- Run `/ticket-folders` to verify bot is working

**Role permissions not working:**
- Use `/set-role` to assign Developer or QA role first
- User must have at least one role to use relevant commands

**Tickets not loading:**
- Ensure folder exists in `tickets/` directory
- Check that files have `.md` extension
- Verify folder name matches what you pass to `/load-tickets`
- Check markdown format follows the guidelines

**Thread information not displaying:**
- Verify markdown file follows the correct format
- Parser will display raw ticket info if parsing fails
- Check bot has permission to post embeds in channel

## License

MIT

## Support

For issues or suggestions, contact the development team.
