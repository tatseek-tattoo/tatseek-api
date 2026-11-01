#!/bin/sh
# One request. Requires curl and Python 3; never downloads photographs.
set -eu
query=${1:-fine line rose}
result=$(mktemp)
trap 'rm -f "$result"' EXIT HUP INT TERM
curl --fail --silent --show-error --max-time 20 --get \
  'https://tatseek.com/api/v1/search' \
  --header 'Accept: application/json' \
  --data-urlencode "q=$query" --data-urlencode 'limit=2' --output "$result"
python3 - "$result" <<'PY'
import json,sys
from urllib.parse import urlparse
with open(sys.argv[1]) as f:
    data=json.load(f)
if not isinstance(data,dict) or not isinstance(data.get('tattoos'),list):
    raise SystemExit('Unexpected response: expected a tattoos array')
print('Source: TatSeek — https://tatseek.com')
print('Relaxed constraints:',(data.get('understood') or {}).get('dropped',[]))
if not data['tattoos']:
    print('No tattoo results; this is not a service error.')
for item in data['tattoos']:
    url=item.get('url') or ''
    parsed=urlparse(url)
    print(item.get('title') or 'Untitled tattoo')
    print(url if parsed.scheme=='https' and parsed.hostname=='tatseek.com' else '(no TatSeek URL)')
    print('Artist:',(item.get('artist') or {}).get('name') or '(not supplied)')
    print('Studio:',(item.get('studio') or {}).get('name') or '(not supplied)')
PY
