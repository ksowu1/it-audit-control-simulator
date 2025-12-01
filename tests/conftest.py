import pytest
import json
from datetime import datetime, timedelta


@pytest.fixture
def sample_users():
    return {
        "john": {"role": "admin", "status": "active", "active": True, "privileged": True, "department": "development"},
        "mary": {"role": "user", "status": "active", "active": True, "privileged": False, "department": "finance"},
        "lisa": {"role": None, "status": "active", "active": True, "privileged": False, "department": "marketing"},
        "paul": {"role": "user", "status": "terminated", "active": True, "privileged": False, "department": "sales"}
    }


@pytest.fixture
def sample_changes():
    return [
        {
            "id": 101,
            "approved": True,
            "approval_date": datetime(2024, 7, 1),
            "deployment_date": datetime(2024, 7, 2)
        },
        {
            "id": 102,
            "approved": False,
            "approval_date": datetime(2024, 7, 5),
            "deployment_date": datetime(2024, 7, 6)
        }
    ]


@pytest.fixture
def sample_backups():
    return [
        {"date": datetime.now() - timedelta(days=2), "success": True},
        {"date": datetime.now() - timedelta(days=10), "success": True},
        {"date": datetime.now() - timedelta(days=1), "success": False},
    ]


@pytest.fixture
def sample_sod_rules():
    return [
        {"role1": "admin", "role2": "finance", "conflict": "developer & deployer"},
        {"role1": "user", "role2": "development", "conflict": "requester & approver"},
    ]
