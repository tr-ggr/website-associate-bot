"""Helpers for Discord thread naming and parsing."""
import re

DISCORD_CHANNEL_NAME_LIMIT = 100


def build_thread_name(status: str, ticket_name: str, username: str | None = None) -> str:
    """Build a Discord thread name that always respects the 100-character limit."""
    status_prefixes = {
        "OPEN": "[OPEN] ",
        "CLAIMED": f"[CLAIMED][{username or 'dev'}]",
        "PENDING-REVIEW": f"[Pending-Review][{username or 'dev'}]",
        "REVIEWED": f"[Reviewed][{username or 'qa'}]",
        "CLOSED": f"[CLOSED][{username or 'user'}]",
    }

    if status not in status_prefixes:
        raise ValueError(f"Unsupported status for thread name: {status}")

    prefix = status_prefixes[status]
    available_for_ticket = DISCORD_CHANNEL_NAME_LIMIT - len(prefix)

    if available_for_ticket <= 0:
        # Fall back to truncating the prefix itself in extreme username cases.
        return prefix[:DISCORD_CHANNEL_NAME_LIMIT]

    if len(ticket_name) <= available_for_ticket:
        return f"{prefix}{ticket_name}"

    if available_for_ticket <= 3:
        truncated_ticket = "." * available_for_ticket
    else:
        truncated_ticket = f"{ticket_name[:available_for_ticket - 3]}..."

    return f"{prefix}{truncated_ticket}"


def parse_thread_name(thread_name: str) -> tuple[str | None, str | None]:
    """Parse a thread name into status and ticket display name."""
    patterns = [
        ("OPEN", r"^\[OPEN\]\s*(.+)$"),
        ("CLAIMED", r"^\[CLAIMED\]\[.+?\](.+)$"),
        ("PENDING-REVIEW", r"^\[Pending-Review\]\[.+?\](.+)$"),
        ("REVIEWED", r"^\[Reviewed\]\[.+?\](.+)$"),
        ("CLOSED", r"^\[CLOSED\]\[.+?\](.+)$"),
    ]

    for status, pattern in patterns:
        match = re.match(pattern, thread_name)
        if match:
            return status, match.group(1).strip()

    return None, None
