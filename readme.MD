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

will download all attachments (in all formats) for emails identified by the `q` [querystring](https://support.google.com/mail/answer/7190?hl=en). (You can test your `q` right inside your gmail inbox web interface)

The loaction `tables/files` depends on the `needs_processors` parameter. 
- If the attachment is a valid csv, set `"needs_processors": "false` and it will be saved to `/data/out/tables`
- If the attachment is not a valid csv (xlsx, zip, ...), set it to `true`. The attachments will be downloaded to `/data/out/files` and processors should be used in that case (see example below)
- If the query `q` doesn't match any messages the extractor fails with user error (TODO: would a flag to ignore this be useful?)
- If the query `q` matches multiple messages and they contain attachments with overlapping names, the behavior depends on `needs_processors`
    - if `needs_processors` is `true` an unique value is appended to the filename (`my_file.csv` becomes `my_file_XXXXYYYYZZZZWWWW.csv`) and you need to use appropriate combination of processors to move the csvs into a folder (so they act as a sliced files) and create a manifest.
    - if `needs_processors` is `false` the extractor raises an error. In this case the extractor can't modify the attachment filename because the filename is the same as the table name in Storage. If you get this error, either modify your `q` or use processors.

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

the `newer_than:7d` parameter ensures that if the extractor failed for some reason in the past, the next iteration will backfill the data.

In this case, the attachment is a `zip` containing a csv. All the csvs have same structure, hence we can consider them as a sliced table.
```
{
  "after": [
    {"definition": {"component": "keboola.processor-decompress"}},
```
plain decompress - the gotcha is that `zip` archives are decompressed into a new folder so there is some nesting involved. Such table would be skipped on import so we use the `processor-flatten-folders`

```
    {
      "definition": {"component": "keboola.processor-flatten-folders"},
      "parameters": {"starting_depth": 0}},
```

Move the csvs from `files` to a subfolder `tablename_in_storage`. Doing this turns the csvs into [sliced tables](https://developers.keboola.com/extend/common-interface/folders/#sliced-tables)
This has many benefits
- you can choose the name of the table in storage (by naming the folder appropriately, just don't forget the `.csv` suffix)
- you can import multiple csvs in one run

```
    {
      "definition": {"component": "keboola.processor-move-files"},
      "parameters": {
        "direction": "tables",
        "folder": "tablename_in_storage.csv"
      }
    },
```

Since the tables are now slices, they can not contain a header (+ there are 11 garbage lines) so we skip 11 + 1 (header) lines from the top. In this particular case there is a footer containing some `sums` so we skip it too.

```
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
```

Finally, since we skipped the header, we must define a manifest file. This brings an opportunity to set up incremental loading as well

```
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

To run tests on local:
1. create the `.env` file (based on `.env-template`)
The credentials to put into `.env` are to arbitrary authorized gmail account/app.It must contain
- an email with the subject `kbc-ex-gmail-attachments` and has an attachment `test.csv` with arbitrary content.
- at least 30 emails in inbox (to test pagination)
2. and run `docker-compose run --rm dev python3 -m pytest` or simply `make test`

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


