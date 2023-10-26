import urllib.request
import os
import json

aws_session_token = os.environ.get('AWS_SESSION_TOKEN')

def get_parameter(name, is_encrypted=True):
    decrypt_parameter = "&withDecryption=true" if is_encrypted else ""
    req = urllib.request.Request(f"http://localhost:2773/systemsmanager/parameters/get?name={name}{decrypt_parameter}")
    req.add_header('X-Aws-Parameters-Secrets-Token', aws_session_token)
    config = urllib.request.urlopen(req).read()

    return json.loads(config)['Parameter']['Value']