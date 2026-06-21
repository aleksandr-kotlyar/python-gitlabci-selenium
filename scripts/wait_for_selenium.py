"""Wait until Selenium Remote WebDriver is ready."""

import argparse
import json
import sys
import time
from urllib.parse import urlsplit, urlunsplit
from urllib.request import urlopen


def status_urls(remote_url):
    """Return status endpoints for Selenium 3 and Selenium 4 servers."""
    parsed = urlsplit(remote_url)
    base_path = parsed.path.rstrip('/')
    root = urlunsplit((parsed.scheme, parsed.netloc, '', '', ''))

    urls = [f'{root}/status']
    if base_path:
        urls.insert(0, f'{root}{base_path}/status')
    return urls


def is_ready(payload):
    """Return true when Selenium status payload says the server is ready."""
    return payload.get('status') == 0 or payload.get('value', {}).get('ready')


def wait_for_selenium(remote_url, timeout, request_timeout):
    """Wait until one of the Selenium status endpoints returns ready."""
    deadline = time.time() + timeout
    urls = status_urls(remote_url)
    last_error = None

    while time.time() < deadline:
        for status_url in urls:
            try:
                with urlopen(status_url, timeout=request_timeout) as response:
                    payload = json.loads(response.read().decode('utf-8'))
                if is_ready(payload):
                    print(f'Selenium is ready at {status_url}')
                    return 0
            except Exception as error:
                last_error = error
        time.sleep(1)

    print(f'Selenium is not ready after {timeout} seconds', file=sys.stderr)
    if last_error:
        print(f'Last error: {last_error}', file=sys.stderr)
    return 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True,
                        help='Remote Selenium URL, for example '
                             'http://selenium:4444/wd/hub')
    parser.add_argument('--timeout', type=int, default=60,
                        help='How many seconds to wait for Selenium.')
    parser.add_argument('--request-timeout', type=int, default=2,
                        help='HTTP request timeout in seconds.')
    return parser.parse_args()


def main():
    args = parse_args()
    return wait_for_selenium(args.url, args.timeout, args.request_timeout)


if __name__ == '__main__':
    raise SystemExit(main())
