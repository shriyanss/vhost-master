# vhost_master v0.0.4
## Conditions for matching a VHost
- [Status Code](#status-code)

### Status Code
- `status==<status_code>` (E.g. `status==200`)
- `status!=<status_code>` (E.g. `status!=404`)

### Content Length
The tool uses the `len()` function to calculate the content length of `response.text`. Following are the conditions:-
- `content_length==<content_length>` (E.g. `content_length==100`)
- `content_length!=<content_length>` (E.g. `content_length!=100`)
- `content_length==<content_length_range>` (E.g. `content_length==100-500`)
- `content_length!=<content_length_range>` (E.g. `content_length!=100-500`)

Note that this doesn't utilizes the `Content-Length` response header