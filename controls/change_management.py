
class ChangeManagement:
    """
    Simulates a basic Change Management control test.
    """

    def __init__(self, changes):
        self.changes = changes  # list of change dictionaries

    def check_for_unapproved_changes(self):
        """
        Fails if any change has approved == False
        """
        unapproved = [c for c in self.changes if not c["approved"]]
        return len(unapproved) == 0, unapproved

    def check_deployment_after_approval(self):
        """
        Fails if deployment date comes BEFORE approval date.
        """
        bad_changes = [
            c for c in self.changes
            if c["deployment_date"] < c["approval_date"]
        ]
        return len(bad_changes) == 0, bad_changes
