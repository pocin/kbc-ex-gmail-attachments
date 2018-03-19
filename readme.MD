# About
https://github.com/pocin/kbc-ex-gmail-attachments.git

A basic gmail attachments extractor meant to be used alongside with processors.

# Config

```javascript
{
    "#refresh_token": "",
    "client_id": "",
    "#client_secret": "",
    "queries": [
        { "name": "ARBITRARY NAME reports",
          "q": "suuubject has:attachment newer_than:21d",
          "needs_processors": true
        }
    ]
}
```
will download all attachments (in all formats) for emails identified by the `q` querystring.
The loaction `tables/files` depends on the `needs_processors` parameter. 
If the attachment is a valid csv, set it to `false` and it will be uploaded to `/data/out/tables` and to storage
If the attachment is not a valid csv (xlsx, zip, ...), set it to `true` and it will be uploaded to `/data/out/files` and processors should be used in that case

# Development
TODO: make public & add OAuth2 support

To run tests on local:
1. create the `.env` file (based on `.env-template`)
The credentials to put into `.env` are to arbitrary authorized gmail account which contains an email with the subject `kbc-ex-gmail-attachments` and has an attachment `test.csv` with arbitrary content.
(to get the refresh_token, check the snippet below)
2. and run `run_tests.sh` script.

## Get refresh token

```python
import requests
def retrieve_authorization_code(client_id, redirect_uri='http://localhost):
    authorization_code_req = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "prompt": "consent",
        "access_type": "offline",
        "scope": (r"https://mail.google.com/")
    }

    r = requests.get(base_url + "auth",
                     params=authorization_code_req,
                     allow_redirects=False)
    url = r.headers.get('location')
    r.raise_for_status()
    return url

def retrieve_tokens(authorization_code, client_id, client_secret, redirect_uri):
    access_token_req = {
        "code" : authorization_code,
        "client_id" : client_id,
        "client_secret" : client_secret,
        "redirect_uri" : redirect_uri,
        "grant_type": "authorization_code",
    }
    r = requests.post(base_url + "token", data=access_token_req)   
    r.raise_for_status()
    return r.json()

client_id=''
client_secret=''
redirect_uri='http://localhost'

auth_url = retrieve_authorization_code(client_id)
# visit this, grant consent
print(auth_url)
# copy the `code` parameter from the redirected uri
authorization_code = "copied from above"
tokens = retrieve_tokens(authorization_code, client_id, client_secret, redirect_uri)
print(tokens['refresh_token'])
```

# License
Use at your own risk, MIT
MIT License

Copyright (c) 2018 Robin Nemeth

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


