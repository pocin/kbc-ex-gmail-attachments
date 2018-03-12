import pytest
from main import main
import os


def test_main_downloading(tmpdir):
    params = {
        "#refresh_token": os.environ["KBC_EX_REFRESH_TOKEN"],
        "client_id": os.environ["KBC_EX_CLIENT_ID"],
        "#client_secret": os.environ["KBC_EX_CLIENT_SECRET"],
        "queries": [
            {
                "name": "KASKUS reports",
                "q": "kbc-ex-gmail-attachments has:attachment"
            }
        ]
    }
    outdir = tmpdir.mkdir('out').mkdir('tables').strpath
    main(params, outdir)

    downloaded_files = os.listdir(outdir)
    assert len(downloaded_files) == 1
    assert downloaded_files[0] == 'test.csv'
