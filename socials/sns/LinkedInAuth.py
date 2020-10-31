# -*- coding: utf-8 -*-
import os
import sys
import re
import time
from datetime import datetime, timedelta
from http import server
from urllib import parse
import threading
import requests

try:  # noqa
    from socials.env import (
        LINKEDIN_APP_CLIENT_ID,
        LINKEDIN_REFRESH_TOKEN,
        LINKED_REFRESH_TOKEN_EXPIRES_IN,
        LINKEDIN_TOKEN_CREATED_AT,
        LINKED_ACCESS_TOKEN_EXPIRES_IN,
        LINKEDIN_REDIRECT_URI,
        LINKEDIN_LISTENING_PORT,
        LINKEDIN_ACCESS_TOKEN,
        LINKEDIN_APP_CLIENT_SECRET,
        dot_env_file,
    )
except ImportError:
    try:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
    except (NameError, Exception) as e:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname("."), "..")))
    from socials.env import (
        LINKEDIN_APP_CLIENT_ID,
        LINKEDIN_REFRESH_TOKEN,
        LINKED_REFRESH_TOKEN_EXPIRES_IN,
        LINKEDIN_TOKEN_CREATED_AT,
        LINKED_ACCESS_TOKEN_EXPIRES_IN,
        LINKEDIN_REDIRECT_URI,
        LINKEDIN_LISTENING_PORT,
        LINKEDIN_ACCESS_TOKEN,
        LINKEDIN_APP_CLIENT_SECRET,
        dot_env_file,
    )

SERVER_LIFETIME = 60
LINKEDIN_TOKEN_ENDPOINT = "https://www.linkedin.com/oauth/v2/accessToken"


def get_authorization_url_and_start_server():
    """Get an authorization url an print it prompting the user
    to follow it and authorize the app in order to make requests on his/her behalf.
    a simple http server is spawn after this waiting for the redirection.
    """
    client_id = os.environ.get(LINKEDIN_APP_CLIENT_ID, None)
    client_secret = os.environ.get(LINKEDIN_APP_CLIENT_SECRET, None)
    redirect_uri = os.environ.get(LINKEDIN_REDIRECT_URI, None)
    listening_port = os.environ.get(LINKEDIN_LISTENING_PORT, "8000")
    scopes_list = ["r_1st_connections_size", "r_liteprofile", "w_member_social"]
    scopes = "+".join(scopes_list)
    try:
        listening_port = int(listening_port)
    except ValueError as err:
        print("Invalid listening port:", listening_port)
        raise err
    if not client_id or not client_secret:
        raise ValueError("Could not get linkedin app client id/secret")
    authorization_url = (
        f"https://www.linkedin.com/uas/oauth2/"
        f"authorization?response_type=code&"
        f"client_id={client_id}&scope={scopes}"
        f"&redirect_uri={redirect_uri}"
    )
    print(
        f"Open within the next {SERVER_LIFETIME} seconds "
        f"the authorization link below to authorize posting on your behalf:\n{authorization_url}"
    )
    _linkedin_temp_server(client_id, client_secret, listening_port, redirect_uri)


def _token_expired():
    if not os.environ.get("LINKEDIN_ACCESS_TOKEN", None):
        return False
    token_created_env_var = os.environ.get("LINKEDIN_TOKEN_CREATED_AT", None)
    access_token_expires_in_env_var = os.environ.get(
        "LINKED_ACCESS_TOKEN_EXPIRES_IN", None
    )
    if token_created_env_var and access_token_expires_in_env_var:
        try:
            token_created_at = datetime.fromtimestamp(float(token_created_env_var))
            access_token_expires_in = int(access_token_expires_in_env_var)
            now = datetime.now()
            return token_created_at + timedelta(seconds=access_token_expires_in) < now
        except (ValueError, Exception) as err:
            print("Could not get when the token was created")
            raise err
    else:
        raise RuntimeError("Could not check for token expiration")


def check_token_expiration():
    if _token_expired():
        # try updating it
        _update_token()
    # check again
    if _token_expired():
        raise RuntimeError("Could not refresh the expired access token")
    # we don't even have a token variable ?
    if not os.environ.get("LINKEDIN_ACCESS_TOKEN", None):
        raise RuntimeError("Could not raed the access token")


def _update_token():
    client_id = os.environ.get(LINKEDIN_APP_CLIENT_ID, None)
    client_secret = os.environ.get(LINKEDIN_APP_CLIENT_SECRET, None)
    refresh_token = os.environ.get(LINKEDIN_REFRESH_TOKEN, None)
    if client_id and client_secret:
        query_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        try:
            response = requests.post(
                LINKEDIN_TOKEN_ENDPOINT, data=query_data, timeout=40
            )
            response = response.json()
            _save_token(response)
        except Exception as err:
            print("could not update the token: ", err)


def _save_token(response):
    _dot_env_file = dot_env_file()
    if not _dot_env_file:
        raise FileNotFoundError("could not get the path to save the token :(")
    access_token = response.get("access_token", None)
    refresh_token = response.get("refresh_token", None)
    access_token_expires_in = response.get("expires_in", None)
    refresh_token_expires_in = response.get("refresh_token_expires_in", None)
    if (
        access_token
        and refresh_token
        and access_token_expires_in
        and refresh_token_expires_in
    ):
        try:
            token_created_at = str(datetime.now().timestamp())
            access_token_expires_in = str(access_token_expires_in)
            refresh_token_expires_in = str(refresh_token_expires_in)
            linkedin_vars = {
                LINKEDIN_ACCESS_TOKEN: access_token,
                LINKEDIN_REFRESH_TOKEN: refresh_token,
                LINKEDIN_TOKEN_CREATED_AT: token_created_at,
                LINKED_ACCESS_TOKEN_EXPIRES_IN: access_token_expires_in,
                LINKED_REFRESH_TOKEN_EXPIRES_IN: refresh_token_expires_in,
            }
            with open(_dot_env_file, "r") as _f:
                variables = _f.read()
            for key, value in linkedin_vars.items():
                # replace or append the new values
                if key in variables:
                    variables = re.sub(rf"{key}(.*)", f"{key}={value}", variables)
                else:
                    variables += f"\n{key}={value}"
                # also export them, skipping having to re-read the .env file
                os.environ[key] = value
            if not variables.endswith("\n"):
                variables += "\n"
            # save the file with the updated values
            with open(_dot_env_file, "w") as _f:
                _f.write(variables)
        except (PermissionError, Exception) as err:
            print("Error saving the token:", err)
            raise e


def wait_until(condition, timeout, period=1, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        if condition(*args, **kwargs):
            return True
        time.sleep(period)
    return False


def _linkedin_temp_server(client_id, client_secret, port, redirect_uri):
    """Spawn a server temporarily to handle an authorization redirection after authorizing the linkedin app.

    Requirement: On app creation, the redirect uri must match the hostname this scripts is running at.
    You can use more than one redirect uris.
    If running locally (testing it), you can just use http://localhost:8000/
    If running on a remote server, you must use this server's name, e.g. http://example.com:8000/
    Also make sure the specified port is available (no firewall blocking it).
    """

    class MyHandler(server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa
            p = self.path.split("?")
            if len(p) > 1:
                params = parse.parse_qs(p[1], True, True)
                if "code" in params:
                    authorization_code = params["code"][0]
                    query_data = {
                        "grant_type": "authorization_code",
                        "code": authorization_code,
                        "redirect_uri": redirect_uri,
                        "client_id": client_id,
                        "client_secret": client_secret,
                    }
                    try:
                        response = requests.post(
                            LINKEDIN_TOKEN_ENDPOINT, data=query_data, timeout=60
                        )
                        response = response.json()
                        _save_token(response)
                    except Exception as err:
                        print("could not get a token: ", err)
            body = "<html>OK</html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body.encode())
            self.server.finished = True

    server_address = ("0.0.0.0", port)
    httpd = server.HTTPServer(server_address, MyHandler)
    httpd.finished = False
    thread = threading.Thread(None, httpd.handle_request)
    thread.start()

    def _has_served():
        return httpd.finished

    wait_until(_has_served, SERVER_LIFETIME)
    try:
        requests.get(f"http://localhost:{port}", timeout=10)
    except (requests.exceptions.ConnectTimeout, Exception):
        pass


if __name__ == "__main__":
    get_authorization_url_and_start_server()
