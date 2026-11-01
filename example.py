#!/usr/bin/env python3
"""One TatSeek request, with attribution and no image downloads. Python 3.9+."""
import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

def result_link(value):
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    return value if parsed.scheme == 'https' and parsed.hostname == 'tatseek.com' else None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='fine line rose')
    parser.add_argument('--composition', action='store_true',
                        help='Require a scanned Realism portrait to have at least 50%% share')
    args = parser.parse_args()
    if args.composition:
        path = 'tattoos'
        params = dict(style='realism', subject='portrait', min_share=50, min_conf='high', limit=2)
    else:
        path, params = 'search', dict(q=args.query, limit=2)
    url = 'https://tatseek.com/api/v1/' + path + '?' + urlencode(params)
    try:
        request = Request(url, headers={'Accept': 'application/json',
                                       'User-Agent': 'TatSeek-GitHub-example/1.0'})
        with urlopen(request, timeout=20) as response:
            data = json.load(response)
        if not isinstance(data, dict) or not isinstance(data.get('tattoos'), list):
            raise ValueError('Expected an object containing a tattoos array')
    except HTTPError as error:
        print('TatSeek HTTP error:', error.code, file=sys.stderr)
        if error.code == 429:
            print('Slow down; Retry-After:', error.headers.get('Retry-After', 'not supplied'), file=sys.stderr)
        return 1
    except (URLError, TimeoutError, OSError, ValueError) as error:
        print('TatSeek request failed:', error, file=sys.stderr)
        return 1
    understood = data.get('understood') or {}
    print('Source: TatSeek — https://tatseek.com')
    print('Query:', url)
    print('Relaxed constraints:', json.dumps(understood.get('dropped', []), ensure_ascii=False))
    if not data['tattoos']:
        print('No tattoo results in this response. This is not a service error.')
    for item in data['tattoos']:
        artist, studio = item.get('artist') or {}, item.get('studio') or {}
        print('\n' + str(item.get('title') or 'Untitled tattoo'))
        print('TatSeek page:', result_link(item.get('url')) or '(not supplied)')
        print('Artist:', artist.get('name') or '(not supplied)', result_link(artist.get('url')) or '')
        print('Studio:', studio.get('name') or '(not supplied)', result_link(studio.get('url')) or '')
        composition = item.get('composition') or {}
        main_subject = item.get('main_subject') or {}
        print('Composition source:', composition.get('source') or '(unknown)')
        print('Lead subject:', main_subject.get('slug') if main_subject.get('tier') == 'lead' else '(not established)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
