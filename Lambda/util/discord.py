import json
import urllib
from parameter_store import get_parameter

def post_discord_message(message):
    is_test = False
    test_string = "test_" if is_test else ""

    data = {"content": message}
    headers = {
        "User-Agent": "curl/7.64.1",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        url = get_parameter(f"{test_string}discord_webhook_url"),
        data = json.dumps(data).encode(),
        headers = headers
    )
    
    try:
        with urllib.request.urlopen(req) as _res:
            pass
    except urllib.error.HTTPError as err:
        print(err.code)
    except urllib.error.URLError as err:
        print(err.reason)