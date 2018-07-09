import pytest
import logging
from main import main, AttachmentsExtractor
import os

def test_main_downloading_with_processors(tmpdir, auth_data):
    params = {
        "queries": [
            {
                "q": "kbc-ex-gmail-attachments has:attachment",
                "needs_processors": True
            }
        ]
    }
    main(params, datadir=tmpdir.strpath, **auth_data)
    # expecxt the file in out/files
    downloaded_files = os.listdir(os.path.join(tmpdir.strpath, 'out/files'))
    assert len(downloaded_files) == 1
    assert downloaded_files[0] == 'test.csv'

def test_main_downloading_without_processors(tmpdir, auth_data):
    params = {
        "queries": [
            {
                "q": "kbc-ex-gmail-attachments has:attachment",
                "needs_processors": False
            }
        ]
    }
    main(params, datadir=tmpdir.strpath, **auth_data)
    # expecxt the file in out/files since needs_processors = False
    downloaded_files = os.listdir(os.path.join(tmpdir.strpath, 'out/tables'))
    assert len(downloaded_files) == 1
    assert downloaded_files[0] == 'test.csv'



def test_ValueError_if_query_doesnt_match_any_message(auth_data, tmpdir, caplog):
    """Test if pagination is necessary"""
    ex = AttachmentsExtractor(**auth_data)

    q = "this_is_an_unexisting_query_should_fail_with_ValueError"
    outdir = tmpdir.mkdir("out")
    with pytest.raises(ValueError) as excinfo:
        ex.search_and_download_attachments(
            q,
            outdir.strpath)

    assert excinfo.match(r"^No messages matching")
