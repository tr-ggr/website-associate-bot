"""Discord Bot for managing support tickets."""
import discord
from discord.ext import commands
from discord import app_commands
import logging
from config import DISCORD_TOKEN, TICKETS_DIR
from database import (
    init_db, add_thread, get_thread, update_thread_status,
    increment_developer_resolved, increment_qa_reviewed, 
    get_leaderboard_dev, get_leaderboard_qa,
    set_user_role, get_user_roles, has_role,
    is_ticket_loaded, mark_ticket_loaded
)
from ticket_loader import load_tickets_from_folder, get_available_folders
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    """When the bot is ready, sync commands and initialize database."""
    logger.info(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")


@bot.tree.command(
    name="set-role",
    description="Assign yourself a role (Developer, QA, or PM)"
)
@app_commands.describe(
    role="The role to assign: 'developer', 'qa', or 'pm'"
)
@app_commands.choices(role=[
    app_commands.Choice(name="Developer", value="developer"),
    app_commands.Choice(name="QA", value="qa"),
    app_commands.Choice(name="Project Manager", value="pm")
])
async def set_role(interaction: discord.Interaction, role: str):
    """Assign yourself a Developer, QA, or PM role."""
    await interaction.response.defer()
    
    try:
        role_lower = role.lower()
        
        # Check if user is trying to set PM role
        if role_lower == "pm":
            # Only admins can assign PM role
            if not interaction.user.guild_permissions.administrator:
                await interaction.followup.send("❌ Only server admins can set the Project Manager role.")
                return
        
        # Determine role parameters
        if role_lower == "developer":
            is_developer = True
            is_qa = False
            is_pm = False
            discord_role_name = "Developer"
            emoji = "👨‍💻"
        elif role_lower == "qa":
            is_developer = False
            is_qa = True
            is_pm = False
            discord_role_name = "QA"
            emoji = "🔍"
        elif role_lower == "pm":
            is_developer = False
            is_qa = False
            is_pm = True
            discord_role_name = "Project Manager"
            emoji = "📋"
        else:
            await interaction.followup.send("❌ Invalid role. Choose 'developer', 'qa', or 'pm'.")
            return
        
        # Get or create Discord role
        guild = interaction.guild
        discord_role = discord.utils.get(guild.roles, name=discord_role_name)
        
        if not discord_role:
            # Create the role if it doesn't exist
            color = discord.Color.blurple() if role_lower == "developer" else (discord.Color.gold() if role_lower == "qa" else discord.Color.purple())
            discord_role = await guild.create_role(
                name=discord_role_name,
                color=color,
                reason="Ticket bot role assignment"
            )
            logger.info(f"Created Discord role: {discord_role_name}")
        
        # Assign Discord role to user
        await interaction.user.add_roles(discord_role)
        
        # Set user role in database
        set_user_role(interaction.user.id, str(interaction.user), is_developer=is_developer, is_qa=is_qa, is_pm=is_pm)
        
        embed = discord.Embed(
            title="Role Assigned",
            description=f"{emoji} You have been assigned the **{discord_role_name}** role",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Discord Role", value=f"<@&{discord_role.id}>", inline=False)
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Role '{role_lower}' set for {interaction.user}: {interaction.user.id}")
        
    except Exception as e:
        logger.error(f"Error setting role: {e}")
        await interaction.followup.send(f"❌ Error setting role: {e}")



@bot.tree.command(
    name="load-tickets",
    description="Load tickets from a folder into a Discord channel (PM only)"
)
@app_commands.describe(
    folder="The folder name within tickets/ directory (e.g., support, bugs, features)",
    channel="The Discord channel where threads should be created"
)
async def load_tickets(interaction: discord.Interaction, folder: str, channel: discord.TextChannel):
    """Load tickets from a folder and create threads in the specified channel. Only PMs can use this."""
    await interaction.response.defer()
    
    try:
        # Check if user is a PM
        if not has_role(interaction.user.id, "pm"):
            await interaction.followup.send("❌ Only Project Managers can load tickets. Use `/set-role` to get the PM role.")
            return
        
        # Load tickets from folder with parsing
        tickets = load_tickets_from_folder(folder)
        
        if not tickets:
            await interaction.followup.send(f"❌ No markdown files found in `{folder}/` folder")
            return
        
        # Create threads for each ticket
        created_count = 0
        failed_count = 0
        skipped_count = 0
        
        for ticket in tickets:
            try:
                # Check if this ticket has already been loaded
                ticket_filename = ticket.get('name', '')
                if is_ticket_loaded(ticket_filename, folder):
                    logger.info(f"Ticket already loaded: {ticket_filename} (skipping)")
                    skipped_count += 1
                    continue
                
                # Use parsed title if available, otherwise use name
                display_name = ticket.get('title') or ticket['name']
                thread_name = f"[OPEN] {display_name}"
                
                # Create thread in the specified channel
                thread = await channel.create_thread(
                    name=thread_name,
                    type=discord.ChannelType.public_thread
                )
                
                # Add to database
                add_thread(
                    thread_id=thread.id,
                    ticket_name=display_name,
                    folder=folder,
                    channel_id=channel.id,
                    created_by=str(interaction.user)
                )
                
                # Mark ticket as loaded
                mark_ticket_loaded(ticket_filename, folder, thread.id, channel.id)
                
                # Build detailed embed with parsed information
                embed = discord.Embed(
                    title=display_name,
                    color=discord.Color.blue()
                )
                
                # Add priority if present
                if ticket.get('priority'):
                    embed.add_field(name="🚨 Priority", value=f"**{ticket['priority']}**", inline=False)
                
                # Add problem section
                if ticket.get('problem'):
                    problem_text = ticket['problem'][:1024]  # Discord limit
                    if len(ticket['problem']) > 1024:
                        problem_text += "..."
                    embed.add_field(name="Problem", value=problem_text, inline=False)
                
                # Add what to fix
                if ticket.get('what_to_fix'):
                    fix_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(ticket['what_to_fix'])])
                    embed.add_field(name="What to Fix", value=fix_text, inline=False)
                
                # Add acceptance criteria
                if ticket.get('acceptance_criteria'):
                    criteria_text = "\n".join([f"✓ {item}" for item in ticket['acceptance_criteria']])
                    embed.add_field(name="Acceptance Criteria", value=criteria_text, inline=False)
                
                # Add related files if present
                if ticket.get('related_files'):
                    files_text = "\n".join([f"• {file}" for file in ticket['related_files']])
                    embed.add_field(name="Related Files", value=files_text, inline=False)
                
                embed.add_field(name="Status", value="🔵 OPEN", inline=True)
                embed.add_field(name="Folder", value=f"`{folder}`", inline=True)
                embed.set_footer(text=f"Created by {interaction.user}")
                
                await thread.send(embed=embed)
                
                created_count += 1
                logger.info(f"Created thread: {thread_name} (ID: {thread.id})")
                
            except Exception as e:
                logger.error(f"Failed to create thread for {ticket.get('title', ticket['name'])}: {e}")
                failed_count += 1
        
        # Send summary
        summary = f"✅ Successfully created **{created_count}** thread(s)"
        if skipped_count > 0:
            summary += f"\n⏭️ **{skipped_count}** ticket(s) already loaded (skipped)"
        if failed_count > 0:
            summary += f"\n⚠️ Failed to create **{failed_count}** thread(s)"
        
        embed = discord.Embed(
            title="Tickets Loaded",
            description=summary,
            color=discord.Color.green() if failed_count == 0 else discord.Color.orange()
        )
        embed.add_field(name="Folder", value=f"`{folder}`", inline=False)
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        
        await interaction.followup.send(embed=embed)
        
    except FileNotFoundError:
        await interaction.followup.send(
            f"❌ Folder `{folder}` not found in `{TICKETS_DIR}/` directory",
        )
    except Exception as e:
        logger.error(f"Error loading tickets: {e}")
        await interaction.followup.send(f"❌ Error loading tickets: {e}")


@bot.tree.command(
    name="claim",
    description="Claim a ticket (use inside a thread) - Developer only"
)
async def claim_ticket(interaction: discord.Interaction):
    """Claim a ticket and update its status to CLAIMED. Only Developers can claim. Must be used inside a ticket thread."""
    await interaction.response.defer()
    
    try:
        # Check if user is in a thread
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("❌ This command must be used inside a thread. Go to the ticket thread and try again.")
            return
        
        # Check if user is a Developer or PM
        user_roles = get_user_roles(interaction.user.id)
        if not (user_roles['is_developer'] or user_roles['is_pm']):
            await interaction.followup.send("❌ Only Developers can claim tickets. Use `/set-role` to get the Developer role.")
            return
        
        thread = interaction.channel
        
        # Get thread info from database
        thread_info = get_thread(thread.id)
        
        if not thread_info:
            await interaction.followup.send("❌ This thread is not tracked in the database")
            return
        
        if thread_info['status'] == 'CLAIMED':
            await interaction.followup.send("⚠️ This ticket is already claimed")
            return
        
        # Get user's display name
        member = interaction.guild.get_member(interaction.user.id)
        username = member.display_name if member else interaction.user.name
        
        # Update thread name
        ticket_name = thread_info['ticket_name']
        new_name = f"[CLAIMED][{username}]{ticket_name}"
        
        await thread.edit(name=new_name)
        update_thread_status(thread.id, "CLAIMED", claimed_by_id=interaction.user.id, claimed_by_username=username)
        
        # Send notification
        embed = discord.Embed(
            title="Ticket Claimed",
            description=f"Claimed by: {interaction.user.mention}",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Old Status", value="[OPEN]", inline=True)
        embed.add_field(name="New Status", value=f"[CLAIMED][{username}]", inline=True)
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Ticket claimed: {thread.id} by {interaction.user}")
        
    except Exception as e:
        logger.error(f"Error claiming ticket: {e}")
        await interaction.followup.send(f"❌ Error claiming ticket: {e}")


@bot.tree.command(
    name="resolved",
    description="Mark a ticket as PENDING-REVIEW with PR link (use inside a thread) - Developer only"
)
@app_commands.describe(
    pr_url="Link to your PR/pull request (required)"
)
async def resolve_ticket(interaction: discord.Interaction, pr_url: str):
    """Mark a ticket as pending review with PR URL. Only Developers can mark as resolved. Must be used inside a ticket thread."""
    await interaction.response.defer()
    
    try:
        # Check if user is in a thread
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("❌ This command must be used inside a thread. Go to the ticket thread and try again.")
            return
        
        # Check if user is a Developer or PM
        user_roles = get_user_roles(interaction.user.id)
        if not (user_roles['is_developer'] or user_roles['is_pm']):
            await interaction.followup.send("❌ Only Developers can mark tickets as pending review. Use `/set-role` to get the Developer role.")
            return
        
        thread = interaction.channel
        
        # Get thread info from database
        thread_info = get_thread(thread.id)
        
        if not thread_info:
            await interaction.followup.send("❌ This thread is not tracked in the database")
            return
        
        if thread_info['status'] == 'PENDING-REVIEW':
            await interaction.followup.send("⚠️ This ticket is already pending review")
            return
        
        # Get user's display name
        member = interaction.guild.get_member(interaction.user.id)
        username = member.display_name if member else interaction.user.name
        
        # Update thread name
        ticket_name = thread_info['ticket_name']
        new_name = f"[Pending-Review][{username}]{ticket_name}"
        
        await thread.edit(name=new_name)
        update_thread_status(thread.id, "PENDING-REVIEW", resolved_by_id=interaction.user.id, resolved_by_username=username, pr_url=pr_url)
        
        # Update developer leaderboard
        increment_developer_resolved(interaction.user.id, str(interaction.user))
        
        # Send notification
        embed = discord.Embed(
            title="Ticket Pending Review",
            description=f"Marked by: {interaction.user.mention}",
            color=discord.Color.orange()
        )
        embed.add_field(name="Old Status", value=thread_info['status'], inline=True)
        embed.add_field(name="New Status", value=f"[Pending-Review][{username}]", inline=True)
        embed.add_field(name="PR Link", value=pr_url, inline=False)
        embed.add_field(name="Next Step", value="Waiting for QA review. Use `/reviewed` to approve.", inline=False)
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Ticket marked pending review: {thread.id} by {interaction.user}")
        
    except Exception as e:
        logger.error(f"Error marking ticket as pending review: {e}")
        await interaction.followup.send(f"❌ Error marking ticket as pending review: {e}")


@bot.tree.command(
    name="reviewed",
    description="Approve a ticket after review (use inside a thread) - QA only"
)
async def reviewed_ticket(interaction: discord.Interaction):
    """Mark a ticket as reviewed after QA approval. Only QAs can review. Must be used inside a ticket thread."""
    await interaction.response.defer()
    
    try:
        # Check if user is in a thread
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("❌ This command must be used inside a thread. Go to the ticket thread and try again.")
            return
        
        # Check if user is a QA or PM
        user_roles = get_user_roles(interaction.user.id)
        if not (user_roles['is_qa'] or user_roles['is_pm']):
            await interaction.followup.send("❌ Only QAs can review tickets. Use `/set-role` to get the QA role.")
            return
        
        thread = interaction.channel
        
        # Get thread info from database
        thread_info = get_thread(thread.id)
        
        if not thread_info:
            await interaction.followup.send("❌ This thread is not tracked in the database")
            return
        
        if thread_info['status'] != 'PENDING-REVIEW':
            await interaction.followup.send("⚠️ This ticket is not pending review. Only pending review tickets can be reviewed.")
            return
        
        if thread_info['status'] == 'REVIEWED':
            await interaction.followup.send("⚠️ This ticket is already reviewed")
            return
        
        # Get user's display name
        member = interaction.guild.get_member(interaction.user.id)
        username = member.display_name if member else interaction.user.name
        
        # Update thread name
        ticket_name = thread_info['ticket_name']
        new_name = f"[Reviewed][{username}]{ticket_name}"
        
        await thread.edit(name=new_name)
        update_thread_status(thread.id, "REVIEWED", reviewed_by_id=interaction.user.id, reviewed_by_username=username)
        
        # Update QA leaderboard
        increment_qa_reviewed(interaction.user.id, str(interaction.user))
        
        # Send notification
        embed = discord.Embed(
            title="Ticket Reviewed",
            description=f"Reviewed by: {interaction.user.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Old Status", value="[Pending-Review]", inline=True)
        embed.add_field(name="New Status", value=f"[Reviewed][{username}]", inline=True)
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Ticket reviewed: {thread.id} by {interaction.user}")
        
    except Exception as e:
        logger.error(f"Error reviewing ticket: {e}")
        await interaction.followup.send(f"❌ Error reviewing ticket: {e}")


@bot.tree.command(
    name="closed",
    description="Mark a ticket as CLOSED (use inside a thread)"
)
async def close_ticket(interaction: discord.Interaction):
    """Mark a ticket as closed. Must be used inside a ticket thread."""
    await interaction.response.defer()
    
    try:
        # Check if user is in a thread
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("❌ This command must be used inside a thread. Go to the ticket thread and try again.")
            return
        
        thread = interaction.channel
        
        # Get thread info from database
        thread_info = get_thread(thread.id)
        
        if not thread_info:
            await interaction.followup.send("❌ This thread is not tracked in the database")
            return
        
        if thread_info['status'] == 'CLOSED':
            await interaction.followup.send("⚠️ This ticket is already closed")
            return
        
        # Get user's display name
        member = interaction.guild.get_member(interaction.user.id)
        username = member.display_name if member else interaction.user.name
        
        # Update thread name
        ticket_name = thread_info['ticket_name']
        new_name = f"[CLOSED][{username}]{ticket_name}"
        
        await thread.edit(name=new_name)
        update_thread_status(thread.id, "CLOSED")
        
        # Send notification
        embed = discord.Embed(
            title="Ticket Closed",
            description=f"Closed by: {interaction.user.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Old Status", value=thread_info['status'], inline=True)
        embed.add_field(name="New Status", value=f"[CLOSED][{username}]", inline=True)
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Ticket closed: {thread.id} by {interaction.user}")
        
    except Exception as e:
        logger.error(f"Error closing ticket: {e}")
        await interaction.followup.send(f"❌ Error closing ticket: {e}")


@bot.tree.command(
    name="leaderboard",
    description="Show the leaderboard of resolved tickets"
)
@app_commands.describe(
    role="Filter leaderboard by role: 'dev' for Developers or 'qa' for QAs (default: dev)",
    limit="Number of top resolvers to show (default: 10, max: 50)"
)
async def show_leaderboard(interaction: discord.Interaction, role: str = "dev", limit: int = 10):
    """Display the leaderboard of users who have resolved the most tickets."""
    await interaction.response.defer()
    
    try:
        # Validate role parameter
        role_lower = role.lower().strip()
        if role_lower not in ["dev", "developer", "qa", "qas"]:
            await interaction.followup.send("❌ Invalid role. Use 'dev' for Developers or 'qa' for QAs.")
            return
        
        # Normalize role
        if role_lower in ["dev", "developer"]:
            role_param = "dev"
            title_role = "👨‍💻 Developer Resolution Leaderboard"
            stat_name = "Resolved"
        else:
            role_param = "qa"
            title_role = "🔍 QA Review Leaderboard"
            stat_name = "Reviewed"
        
        # Clamp limit between 1 and 50
        limit = max(1, min(limit, 50))
        
        # Get leaderboard based on role
        if role_param == "dev":
            leaderboard = get_leaderboard_dev(limit)
        else:
            leaderboard = get_leaderboard_qa(limit)
        
        if not leaderboard:
            await interaction.followup.send(f"📊 No {role_param.upper()} activity yet!")
            return
        
        # Build leaderboard description
        description = ""
        medals = ["🥇", "🥈", "🥉"]
        
        for idx, entry in enumerate(leaderboard, 1):
            medal = medals[idx - 1] if idx <= 3 else f"{idx}️⃣"
            
            if role_param == "dev":
                count = entry['dev_resolved_count']
            else:
                count = entry['qa_reviewed_count']
            
            description += f"{medal} **{entry['username']}** - {count} {stat_name}\n"
        
        embed = discord.Embed(
            title=title_role,
            description=description,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Showing top {limit} {role_param.upper()}s")
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Leaderboard shown to {interaction.user} (role: {role_param})")
        
    except Exception as e:
        logger.error(f"Error showing leaderboard: {e}")
        await interaction.followup.send(f"❌ Error showing leaderboard: {e}")


@bot.tree.command(
    name="ticket-folders",
    description="List all available ticket folders"
)
async def list_folders(interaction: discord.Interaction):
    """List all available ticket folders."""
    await interaction.response.defer()
    
    try:
        folders = get_available_folders()
        
        if not folders:
            await interaction.followup.send(f"📁 No folders found in `{TICKETS_DIR}/` directory")
            return
        
        folder_list = "\n".join([f"• `{folder}`" for folder in folders])
        
        embed = discord.Embed(
            title="Available Ticket Folders",
            description=folder_list,
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Total: {len(folders)} folder(s)")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Error listing folders: {e}")
        await interaction.followup.send(f"❌ Error listing folders: {e}")


@bot.tree.command(
    name="help",
    description="Show all available commands and how to use them"
)
async def show_help(interaction: discord.Interaction):
    """Display help information for all commands."""
    await interaction.response.defer()
    
    try:
        # Create main help embed
        embed = discord.Embed(
            title="📖 Ticket Bot Help",
            description="Complete guide to all available commands",
            color=discord.Color.blurple()
        )
        
        # Role Management
        embed.add_field(
            name="👥 Role Management",
            value="**`/set-role <developer|qa|pm>`**\n" +
                  "Assign yourself a role (Developer, QA, or PM).\n" +
                  "Also assigns the corresponding Discord role.\n" +
                  "`/set-role developer` or `/set-role qa` or `/set-role pm`",
            inline=False
        )
        
        # Ticket Loading
        embed.add_field(
            name="📂 Loading Tickets (PM only)",
            value="**`/load-tickets <folder> <channel>`**\n" +
                  "Load tickets from a folder into a Discord channel.\n" +
                  "Creates threads for each markdown file.\n" +
                  "*Only Project Managers can use this*\n" +
                  "`/load-tickets support #support-channel`",
            inline=False
        )
        
        # Developer Commands
        embed.add_field(
            name="👨‍💻 Developer Commands",
            value="**`/claim`** (in thread) - Claim a ticket to work on it\n" +
                  "**`/resolved <pr_url>`** (in thread) - Submit ticket for QA review with PR link (adds to dev leaderboard)\n" +
                  "*Only available to users with Developer role*",
            inline=False
        )
        
        # QA Commands
        embed.add_field(
            name="🔍 QA Commands",
            value="**`/reviewed`** (in thread) - Approve reviewed ticket (adds to QA leaderboard)\n" +
                  "Must be used on tickets in Pending-Review status\n" +
                  "*Only available to users with QA role*",
            inline=False
        )
        
        # General Commands
        embed.add_field(
            name="⚙️ General Commands",
            value="**`/closed`** (in thread) - Close a ticket\n" +
                  "**`/leaderboard <dev|qa> [limit]`** - View leaderboard\n" +
                  "  • `role`: `dev` (default) or `qa`\n" +
                  "  • `limit`: 1-50 (default: 10)\n" +
                  "**`/ticket-folders`** - List all available ticket folders\n" +
                  "**`/help`** - Show this help message",
            inline=False
        )
        
        await interaction.followup.send(embed=embed)
        
        # Send workflow embed
        workflow_embed = discord.Embed(
            title="🔄 Ticket Workflow",
            description="The typical ticket lifecycle",
            color=discord.Color.green()
        )
        
        workflow_embed.add_field(
            name="1️⃣ Load Tickets",
            value="`/load-tickets <folder> <channel>`\nCreates `[OPEN]` threads",
            inline=True
        )
        
        workflow_embed.add_field(
            name="2️⃣ Developer Claims",
            value="`/claim` (in thread)\nStatus: `[CLAIMED][dev]`",
            inline=True
        )
        
        workflow_embed.add_field(
            name="3️⃣ Dev Submits",
            value="`/resolved <pr_url>` (in thread)\nStatus: `[Pending-Review][dev]`",
            inline=True
        )
        
        workflow_embed.add_field(
            name="4️⃣ QA Reviews",
            value="`/reviewed` (in thread)\nStatus: `[Reviewed][qa]`",
            inline=True
        )
        
        workflow_embed.add_field(
            name="5️⃣ Close Ticket",
            value="`/closed` (in thread)\nStatus: `[CLOSED][user]`",
            inline=True
        )
        
        workflow_embed.add_field(
            name="6️⃣ Check Leaderboard",
            value="`/leaderboard dev` or `/leaderboard qa`",
            inline=True
        )
        
        await interaction.followup.send(embed=workflow_embed)
        
        # Send roles and permissions embed
        roles_embed = discord.Embed(
            title="📋 Roles & Permissions",
            description="What each role can do",
            color=discord.Color.gold()
        )
        
        roles_embed.add_field(
            name="🔧 Project Manager (Admin)",
            value="✓ `/load-tickets` - Load tickets into channels\n" +
                  "✓ `/claim` - Claim tickets (like Dev)\n" +
                  "✓ `/resolved` - Submit for review (like Dev)\n" +
                  "✓ `/reviewed` - Approve tickets (like QA)\n" +
                  "✓ `/closed` - Close tickets\n" +
                  "✓ Can do EVERYTHING\n" +
                  "✓ Gets Discord `Project Manager` role",
            inline=True
        )
        
        roles_embed.add_field(
            name="👨‍💻 Developer",
            value="✓ `/claim` - Claim tickets\n" +
                  "✓ `/resolved` - Submit for review\n" +
                  "✓ `/closed` - Close tickets\n" +
                  "✓ View dev leaderboard\n" +
                  "✓ Gets Discord `Developer` role",
            inline=True
        )
        
        roles_embed.add_field(
            name="🔍 QA",
            value="✓ `/reviewed` - Approve tickets\n" +
                  "✓ `/closed` - Close tickets\n" +
                  "✓ View QA leaderboard\n" +
                  "✓ Gets Discord `QA` role",
            inline=True
        )
        
        roles_embed.add_field(
            name="📝 Role System",
            value="⚠️ **ONE role per user only**\n" +
                  "When you set a new role, your old role is replaced\n" +
                  "PM has all permissions (like an admin)",
            inline=False
        )
        
        await interaction.followup.send(embed=roles_embed)
        
        logger.info(f"Help shown to {interaction.user}")
        
    except Exception as e:
        logger.error(f"Error showing help: {e}")
        await interaction.followup.send(f"❌ Error showing help: {e}")


def main():
    """Start the bot."""
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    main()
