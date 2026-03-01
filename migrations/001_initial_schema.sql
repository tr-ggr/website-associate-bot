-- Initial schema for website-associate-bot

-- Create threads table
CREATE TABLE IF NOT EXISTS threads (
    thread_id INTEGER PRIMARY KEY,
    ticket_name TEXT NOT NULL,
    folder TEXT NOT NULL,
    channel_id INTEGER NOT NULL,
    status TEXT DEFAULT 'OPEN',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    claimed_by_id INTEGER,
    claimed_by_username TEXT,
    resolved_by_id INTEGER,
    resolved_by_username TEXT,
    pr_url TEXT,
    reviewed_by_id INTEGER,
    reviewed_by_username TEXT
);

-- Create user_roles table
CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    is_developer INTEGER DEFAULT 0,
    is_qa INTEGER DEFAULT 0,
    is_pm INTEGER DEFAULT 0,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create leaderboard table
CREATE TABLE IF NOT EXISTS leaderboard (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    dev_resolved_count INTEGER DEFAULT 0,
    qa_reviewed_count INTEGER DEFAULT 0,
    last_dev_resolved TIMESTAMP,
    last_qa_reviewed TIMESTAMP
);

-- Create loaded_tickets table
CREATE TABLE IF NOT EXISTS loaded_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_filename TEXT NOT NULL,
    folder TEXT NOT NULL,
    thread_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticket_filename, folder)
);

-- Create settings table
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
