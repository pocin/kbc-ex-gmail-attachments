import pytest
from main import GmailClient

@pytest.mark.skip
def test_pagination_can_dl_more_than_20_messages(auth_data):
    """Test if pagination is necessary"""
    client = GmailClient(**auth_data)

    messages = client.messages("")
    # I think there is 20 messages per page
    assert len(messages['messages']) > 30


