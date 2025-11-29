
from datetime import datetime, timedelta

backups = [
    {"date": datetime.now() - timedelta(days=2), "success": True},   # Good
    {"date": datetime.now() - timedelta(days=10), "success": True},  # OLD (>7 days)
    {"date": datetime.now() - timedelta(days=4), "success": False},  # FAILED
]


class BackupRecovery:
    """
    Simulates Backup & Recovery audit controls.
    """

    def __init__(self, backups):
        self.backups = backups  # list of backup dictionaries

    def check_backup_recency(self):
        """
        Fails backups older than 7 days.
        """
        threshold = datetime.now() - timedelta(days=7)
        old_backups = [b for b in self.backups if b["date"] < threshold]
        return len(old_backups) == 0, old_backups

    def check_backup_success(self):
        """
        Fails if any backup was unsuccessful.
        """
        failed = [b for b in self.backups if not b["success"]]
        return len(failed) == 0, failed
