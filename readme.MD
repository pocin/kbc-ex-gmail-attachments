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
          "q": "suuubject has:attachment newer_than:21d"
        }
    ]
}
```
will download all attachments (in all formats) for emails identified by the `q` querystring to /data/out/tables

If it's valid csv, then all good, but for something extra use processors.

# Development
TODO: make public & add OAuth2 support

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


