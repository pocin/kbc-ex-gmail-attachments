import requests
import json
import os
import sys
from keboola.docker import Config
from urllib.parse import urljoin
import base64
import logging

REQUIRED_PARAMS = ['queries']

def parse_config(folder='/data'):
    cfg = Config(folder)
    params = cfg.get_parameters()
    for param in REQUIRED_PARAMS:
        assert param in params, "{} not in {}!".format(param, params)

    params = cfg.get_parameters()
    auth_data = dict(
        client_id=cfg.get_oauthapi_appkey(),
        client_secret=cfg.get_oauthapi_appsecret(),
        refresh_token=json.loads(cfg.get_oauthapi_data())['refresh_token']
    )
    return params, auth_data


class GmailClient:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self._access_token = None
        self.root_url = 'https://www.googleapis.com/gmail/v1/users/me/'

    @property
    def access_token(self):
        if self._access_token is None:
            url = 'https://accounts.google.com/o/oauth2/token'
            data = {
                'refresh_token': self.refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token'
            }
            resp = requests.post(url, data=data)
            try:
                resp.raise_for_status()
            except Exception as e:
                logging.exception(resp.text)
                raise
            else:
                self._access_token = resp.json()['access_token']
        return self._access_token

    def _get(self, endpoint, params=None):
        url = urljoin(self.root_url, endpoint)
        headers = {'Authorization': "Bearer {}".format(self.access_token)}
        resp = requests.get(url, params=params, headers=headers)
        try:
            resp.raise_for_status()
        except Exception as e:
            logging.exception(resp.text)
            raise
        else:
            return resp.json()

    def message(self, msg_id):
        """One message details"""
        endpoint = 'messages/{}'.format(msg_id)
        return self._get(endpoint)

    def messages(self, q):
        """query languge https://support.google.com/mail/answer/7190?hl=en"""
        return self._get('messages', params={"q" : q})

    def _download_attachment(self, msg_id, attachment_id, outpath):
        endpoint = 'messages/{}/attachments/{}'.format(msg_id, attachment_id)
        logging.info("Downloading %s to %s", endpoint, outpath)
        resp = self._get(endpoint)
        with open(outpath, 'wb') as fout:
            fout.write(base64.urlsafe_b64decode(resp['data']))


    def download_message_attachments(self, message_id, outdir):
        """Download all attachments for given message to outdir"""
        logging.debug("Downloading attachments for %s", message_id)
        msg = self.message(message_id)
        for part in msg['payload']['parts']:
            filename = part['filename']
            if filename:
                outpath = os.path.join(outdir, filename)
                att_id = part['body']['attachmentId']
                self._download_attachment(message_id, att_id, outpath)

class AttachmentsExtractor(GmailClient):
    def search_and_download_attachments(self, query, outdir):
        messages = self.messages(query)
        for message in messages['messages']:
            self.download_message_attachments(message['id'], outdir)

def main(params, client_id, client_secret, refresh_token, datadir):
    queries = params['queries']

    ex = AttachmentsExtractor(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token)
    for query in queries:
        if query.get('needs_processors'):
            outdir = os.path.join(datadir, 'out/files')
        else:
            outdir = os.path.join(datadir, 'out/tables')
        try:
            os.makedirs(outdir)
        except FileExistsError:
            pass
        out = ex.search_and_download_attachments(query['q'], outdir)

if __name__ == "__main__":
    try:
        datadir = os.environ["KBC_DATADIR"]
        params, auth_data = parse_config(datadir)
        if params.get('debug'):
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        main(params, datadir=datadir, **auth_data)
    except (ValueError, requests.HTTPError, AssertionError) as err:
        logging.error(err)
        sys.exit(1)
    except:
        logging.exception("Internal error")
        sys.exit(2)
