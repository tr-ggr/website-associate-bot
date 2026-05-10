import unittest

from thread_naming import build_thread_name, parse_thread_name, DISCORD_CHANNEL_NAME_LIMIT


class ThreadNameBuilderTests(unittest.TestCase):
    def test_open_name_unchanged_when_short(self):
        name = build_thread_name("OPEN", "Small Ticket")
        self.assertEqual(name, "[OPEN] Small Ticket")
        self.assertLessEqual(len(name), DISCORD_CHANNEL_NAME_LIMIT)

    def test_pending_review_long_name_is_truncated(self):
        username = "Jairus Jasper Colindres"
        ticket_name = "Fix Photo Upload: Orphaned Storage Files and Missing Validation"
        name = build_thread_name("PENDING-REVIEW", ticket_name, username=username)

        self.assertLessEqual(len(name), DISCORD_CHANNEL_NAME_LIMIT)
        self.assertTrue(name.startswith(f"[Pending-Review][{username}]"))
        self.assertTrue(name.endswith("..."))

    def test_all_statuses_fit_limit(self):
        username = "example-user"
        ticket_name = "x" * 300

        statuses = ["OPEN", "CLAIMED", "PENDING-REVIEW", "REVIEWED", "CLOSED"]
        for status in statuses:
            name = build_thread_name(status, ticket_name, username=username)
            self.assertLessEqual(len(name), DISCORD_CHANNEL_NAME_LIMIT, status)

    def test_parser_still_recognizes_truncated_claimed_name(self):
        name = build_thread_name("CLAIMED", "Long Ticket " * 20, username="dev")
        status, parsed_title = parse_thread_name(name)
        self.assertEqual(status, "CLAIMED")
        self.assertIsNotNone(parsed_title)


if __name__ == "__main__":
    unittest.main()
