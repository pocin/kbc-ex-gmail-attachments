import pytest
import os

@pytest.fixture
def auth_data():
    return {
        "refresh_token": os.environ["KBC_EX_REFRESH_TOKEN"],
        "client_id": os.environ["KBC_EX_CLIENT_ID"],
        "client_secret": os.environ["KBC_EX_CLIENT_SECRET"]
    }
