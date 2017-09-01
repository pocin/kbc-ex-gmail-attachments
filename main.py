import requests
from keboola.docker import Config
from urllib.parse import urljoin

# {
#     "installed": {
#         "client_id": "738574772797-n8jrb960o0jkb2ci8ud0p59f6esf7i55.apps.googleusercontent.com",
#         "project_id": "keboola-connection-167714",
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://accounts.google.com/o/oauth2/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_secret": "cJJ4JM5eKVbvDv6aoF9Ij7It",
#         "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
#     }
# }
REQUIRED_PARAMS = ['client_id', '#client_secret', '#refresh_token']

def parse_config(folder='/data'):
    cfg = Config(folder)
    params = cfg.get_parameters()
    for param in REQUIRED_PARAMS:
        assert param in params, "{} not in {}!".format(param, params)
    return params



class GmailClient:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self._access_token = None
        self.root_url = 'https://www.googleapis.com/gmail/v1/'

    @property
    def access_token(self):
        url = 'https://www.googleapis.com/oauth2/v4/token'
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
            print(e)
            raise
        else:
            self._access_token = resp.json()['access_token']

    def _get(self, url, params=None):
        headers = {'Authorization': "Bearer {}".format(self.access_token)}
        resp = requests.get(url, params, headers=headers)
        try:
            resp.raise_for_status()
        except Exception as e:
            print(e)
            raise
        else:
            return resp


    def messages(self, q):
        """query languge https://support.google.com/mail/answer/7190?hl=en"""
        messages = self._get(urljoin(self.root_url, 'me/messages'),
                             {"q":q,
                              "includeSpamTrash": True})
        import pdb; pdb.set_trace()

if __name__ == "__main__":
    params = parse_config()
    print(params)
