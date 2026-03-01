"""Database module for managing tickets and leaderboard."""
import sqlite3
import os
import logging
from datetime import datetime
import glob
from config import DATABASE_FILE


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database and run migrations."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create migrations table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

    # Run pending migrations
    run_migrations()


def run_migrations():
    """Run all pending SQL migrations."""
    conn = get_connection()
    cursor = conn.cursor()

    # Get applied migrations
    cursor.execute("SELECT name FROM migrations")
    applied_migrations = {row['name'] for row in cursor.fetchall()}

    # Get all migration files
    migration_files = sorted(glob.glob("migrations/*.sql"))

    for migration_file in migration_files:
        migration_name = os.path.basename(migration_file)
        if migration_name not in applied_migrations:
            logger.info(f"Applying migration: {migration_name}")
            with open(migration_file, 'r') as f:
                sql = f.read()
                try:
                    cursor.executescript(sql)
                    cursor.execute("INSERT INTO migrations (name) VALUES (?)", (migration_name,))
                    conn.commit()
                except sqlite3.Error as e:
                    logger.error(f"Error applying migration {migration_name}: {e}")
                    conn.rollback()
                    break

    conn.close()


def add_thread(thread_id: int, ticket_name: str, folder: str, channel_id: int, created_by: str | None = None):
    """Add a new thread to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO threads (thread_id, ticket_name, folder, channel_id, status, created_by)
        VALUES (?, ?, ?, ?, 'OPEN', ?)
    """, (thread_id, ticket_name, folder, channel_id, created_by))

    conn.commit()
    conn.close()


def get_thread(thread_id: int):
    """Get a thread from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM threads WHERE thread_id = ?", (thread_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def update_thread_status(thread_id: int, status: str, claimed_by_id: int | None = None, claimed_by_username: str | None = None,
                        resolved_by_id: int | None = None, resolved_by_username: str | None = None,
                        reviewed_by_id: int | None = None, reviewed_by_username: str | None = None, pr_url: str | None = None):
    """Update the status of a thread and optionally track who made the change."""
    conn = get_connection()
    cursor = conn.cursor()

    updates = []
    params = [status.upper(), thread_id]

    if claimed_by_id is not None:
        updates.append("claimed_by_id = ?, claimed_by_username = ?")
        params.insert(1, claimed_by_id)
        params.insert(2, claimed_by_username)

    if resolved_by_id is not None:
        updates.append("resolved_by_id = ?, resolved_by_username = ?")
        params.insert(1, resolved_by_id)
        params.insert(2, resolved_by_username)

    if pr_url is not None:
        updates.append("pr_url = ?")
        params.insert(1, pr_url)

    if reviewed_by_id is not None:
        updates.append("reviewed_by_id = ?, reviewed_by_username = ?")
        params.insert(1, reviewed_by_id)
        params.insert(2, reviewed_by_username)

    update_clause = ", ".join(updates) if updates else ""
    if update_clause:
        update_clause = ", " + update_clause

    cursor.execute(f"""
        UPDATE threads SET status = ?{update_clause} WHERE thread_id = ?
    """, params)

    conn.commit()
    conn.close()


# ===== User Role Management =====

def set_user_role(user_id: int, username: str, is_developer: bool = False, is_qa: bool = False, is_pm: bool = False):
    """Set or update a user's roles (can have multiple)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO user_roles (user_id, username, is_developer, is_qa, is_pm)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, int(is_developer), int(is_qa), int(is_pm)))

    # Also ensure user exists in leaderboard
    cursor.execute("""
        INSERT OR IGNORE INTO leaderboard (user_id, username, dev_resolved_count, qa_reviewed_count)
        VALUES (?, ?, 0, 0)
    """, (user_id, username))

    conn.commit()
    conn.close()


def get_user_roles(user_id: int) -> dict:
    """Get a user's roles."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT is_developer, is_qa, is_pm FROM user_roles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "is_developer": bool(row[0]),
            "is_qa": bool(row[1]),
            "is_pm": bool(row[2])
        }
    return {"is_developer": False, "is_qa": False, "is_pm": False}


def has_role(user_id: int, role: str) -> bool:
    """Check if user has a specific role (developer or qa)."""
    roles = get_user_roles(user_id)
    return roles.get(f"is_{role.lower()}", False)


# ===== Leaderboard Management =====

def increment_developer_resolved(user_id: int, username: str):
    """Increment the resolved count for a developer."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leaderboard 
        SET dev_resolved_count = dev_resolved_count + 1, 
            last_dev_resolved = ?
        WHERE user_id = ?
    """, (datetime.now().isoformat(), user_id))

    if cursor.rowcount == 0:
        cursor.execute("""
            INSERT INTO leaderboard (user_id, username, dev_resolved_count, last_dev_resolved)
            VALUES (?, ?, 1, ?)
        """, (user_id, username, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def increment_qa_reviewed(user_id: int, username: str):
    """Increment the reviewed count for a QA."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leaderboard 
        SET qa_reviewed_count = qa_reviewed_count + 1, 
            last_qa_reviewed = ?
        WHERE user_id = ?
    """, (datetime.now().isoformat(), user_id))

    if cursor.rowcount == 0:
        cursor.execute("""
            INSERT INTO leaderboard (user_id, username, qa_reviewed_count, last_qa_reviewed)
            VALUES (?, ?, 1, ?)
        """, (user_id, username, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def decrement_developer_resolved(user_id: int):
    """Decrement the resolved count for a developer (use for unresolve)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leaderboard 
        SET dev_resolved_count = MAX(0, dev_resolved_count - 1)
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


def decrement_qa_reviewed(user_id: int):
    """Decrement the reviewed count for a QA (use for unreview)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leaderboard 
        SET qa_reviewed_count = MAX(0, qa_reviewed_count - 1)
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()



def get_leaderboard_dev(limit: int = 10):
    """Get the developer leaderboard sorted by resolved count."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, dev_resolved_count, last_dev_resolved
        FROM leaderboard
        WHERE dev_resolved_count > 0
        ORDER BY dev_resolved_count DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_leaderboard_qa(limit: int = 10):
    """Get the QA leaderboard sorted by reviewed count."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, qa_reviewed_count, last_qa_reviewed
        FROM leaderboard
        WHERE qa_reviewed_count > 0
        ORDER BY qa_reviewed_count DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_user_resolved_count(user_id: int) -> int:
    """Get the resolved count for a specific developer."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT dev_resolved_count FROM leaderboard WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else 0


# ===== Loaded Tickets Management =====

def is_ticket_loaded(ticket_filename: str, folder: str) -> bool:
    """Check if a ticket has already been loaded."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM loaded_tickets WHERE ticket_filename = ? AND folder = ?",
        (ticket_filename, folder)
    )
    result = cursor.fetchone()
    conn.close()

    return result is not None


def mark_ticket_loaded(ticket_filename: str, folder: str, thread_id: int, channel_id: int):
    """Mark a ticket as loaded in the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO loaded_tickets (ticket_filename, folder, thread_id, channel_id)
        VALUES (?, ?, ?, ?)
    """, (ticket_filename, folder, thread_id, channel_id))

    conn.commit()
    conn.close()


def get_loaded_tickets(folder: str) -> list:
    """Get all loaded tickets for a specific folder."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT ticket_filename, thread_id, channel_id, loaded_at FROM loaded_tickets WHERE folder = ?",
        (folder,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

# ===== Settings Management =====

def set_setting(key: str, value: str):
    """Set a persistent configuration value."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO settings (key, value)
        VALUES (?, ?)
    """, (key, value))

    conn.commit()
    conn.close()


def get_setting(key: str) -> str | None:
    """Get a persistent configuration value."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None


# ===== Thread Statistics =====

def get_threads_by_status() -> dict:
    """Get all threads grouped by status."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, ticket_name, thread_id, channel_id
        FROM threads
        ORDER BY status, created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    status_groups = {
        "OPEN": [],
        "CLAIMED": [],
        "PENDING-REVIEW": [],
        "REVIEWED": [],
        "CLOSED": []
    }

    for row in rows:
        status = row['status'].upper()
        if status in status_groups:
            status_groups[status].append(dict(row))
        else:
            # Handle unexpected statuses if any
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(dict(row))

    return status_groups
