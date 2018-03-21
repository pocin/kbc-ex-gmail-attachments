# About

A basic gmail attachments extractor meant to be used alongside with processors.

# Config

```javascript
{
    "queries": [
        {
          "q": "suuubject has:attachment newer_than:21d",
          "needs_processors": true
        }
    ]
}
```
will download all attachments (in all formats) for emails identified by the `q` querystring.
The loaction `tables/files` depends on the `needs_processors` parameter. 
- If the attachment is a valid csv, set `"needs_processors": "false` and it will be saved to `/data/out/tables`
- If the attachment is not a valid csv (xlsx, zip, ...), set it to `true`. The attachments will be downloaded to `/data/out/files` and processors should be used in that case (see example below)

## Examples
### zipped csvs skipping header and footer (incrementaly)
Component:
Downloads all emails matching given query (try it in your gmail inbox) into `/data/out/files` (since `"needs_processors": true`)
```
{
    "queries": [
        {
          "q": "subject:(AGENCY_NAME) campaign report has:attachment newer_than:3d",
          "needs_processors": true
        }
    ]
}
```

the newer_than:7d parameter ensures that if the extractor failed for some reason in the past, the next iteration will backfill the data.

In this case, the attachment is a `zip` containing a csv. All the csvs have same structure, hence we can consider them as a sliced table.
```
{
  "after": [
    {"definition": {"component": "keboola.processor-decompress"}},
    {
      "definition": {"component": "keboola.processor-flatten-folders"},
      "parameters": {"starting_depth": 0}},
    {
      "definition": {"component": "keboola.processor-move-files"},
      "parameters": {
        "direction": "tables",
        "folder": "tablename_in_storage.csv"
      }
    },
    {
      "definition": {"component": "keboola.processor-skip-lines"},
      "parameters": {
        "lines": 12,
        "direction_from": "top"
      }
    },
    {
      "definition": {"component": "keboola.processor-skip-lines"},
      "parameters": {
        "lines": 1,
        "direction_from": "bottom"
      }
    },
    {
      "definition": {"component": "keboola.processor-create-manifest"},
      "parameters": {
        "columns": ["campaign", "date", "impressions", "clicks",
                    "total_conversions", "media_cost"],
        "primary_key": ["campaign", "date"],
        "incremental": true
      }
    }
  ]
}
```

# Development
TODO: make public & add OAuth2 support

To run tests on local:
1. create the `.env` file (based on `.env-template`)
The credentials to put into `.env` are to arbitrary authorized gmail account which contains an email with the subject `kbc-ex-gmail-attachments` and has an attachment `test.csv` with arbitrary content.
(to get the refresh_token, check the snippet below)
2. and run `docker-compose dev python3 -m pytest`

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


