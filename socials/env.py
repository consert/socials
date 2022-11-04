"""-*- coding: utf-8 -*-."""
import os
from dotenv import load_dotenv

SMTP_PORT = "SMTP_PORT"
SMTP_HOST = "SMTP_HOST"
SMTP_LOGIN = "SMTP_LOGIN"
SMTP_PASSWORD = "SMTP_PASSWORD"

FACEBOOK_ACCESS_TOKEN = "FACEBOOK_ACCESS_TOKEN"

TWITTER_CONSUMER_KEY = "TWITTER_CONSUMER_KEY"
TWITTER_CONSUMER_SECRET = "TWITTER_CONSUMER_SECRET"
TWITTER_TOKEN = "TWITTER_TOKEN"
TWITTER_TOKEN_SECRET = "TWITTER_TOKEN_SECRET"

INSTAGRAM_LOGIN = "INSTAGRAM_LOGIN"
INSTAGRAM_PASSWORD = "INSTAGRAM_PASSWORD"

LINKEDIN_LISTENING_PORT = "LINKEDIN_LISTENING_PORT"
LINKEDIN_REDIRECT_URI = "LINKEDIN_REDIRECT_URI"
LINKEDIN_APP_CLIENT_ID = "LINKEDIN_APP_CLIENT_ID"
LINKEDIN_APP_CLIENT_SECRET = "LINKEDIN_APP_CLIENT_SECRET"
LINKEDIN_ACCESS_TOKEN = "LINKEDIN_ACCESS_TOKEN"
LINKEDIN_REFRESH_TOKEN = "LINKEDIN_REFRESH_TOKEN"
LINKEDIN_TOKEN_CREATED_AT = "LINKEDIN_TOKEN_CREATED_AT"
LINKED_ACCESS_TOKEN_EXPIRES_IN = "LINKED_ACCESS_TOKEN_EXPIRES_IN"
LINKED_REFRESH_TOKEN_EXPIRES_IN = "LINKED_REFRESH_TOKEN_EXPIRES_IN"

MASTODON_INSTANCE_KEYS = "MASTODON_INSTANCE_KEYS"

REQUESTS_TIMEOUT = 15

DOT_ENV_PATH = os.environ.get("DOT_ENV_PATH", None)

try:
    _here = os.path.realpath(os.path.dirname(__file__))
except (NameError, Exception):
    _here = os.path.realpath(os.path.dirname("."))


def write_default_env(file_path):
    """Write default empty .env file."""
    mastodon_instance_keys = os.environ.get("MASTODON_INSTANCE_KEYS", "")
    mastodons = []
    if mastodon_instance_keys:
        mastodon_instance_keys = mastodon_instance_keys.replace(" ", "").split(",")
        for instance_key in mastodon_instance_keys:
            _instance_url_key = f"MASTODON_{instance_key}_URL"
            _instance_token_key = f"MASTODON_{instance_key}_TOKEN"
            mastodons.append(f"{_instance_url_key}={os.environ.get(_instance_url_key, '')}")
            mastodons.append(f"{_instance_token_key}={os.environ.get(_instance_token_key, '')}")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"""SMTP_HOST={os.environ.get("SMTP_HOST", "")}\n\
SMTP_PORT={os.environ.get("SMTP_PORT", "")}\n\
SMTP_LOGIN={os.environ.get("SMTP_LOGIN", "")}\n\
SMTP_PASSWORD={os.environ.get("SMTP_PASSWORD", "")}\n\
FACEBOOK_ACCESS_TOKEN={os.environ.get("FACEBOOK_ACCESS_TOKEN", "")}\n\
TWITTER_CONSUMER_KEY={os.environ.get("TWITTER_CONSUMER_KEY", "")}\n\
TWITTER_CONSUMER_SECRET={os.environ.get("TWITTER_CONSUMER_SECRET", "")}\n\
TWITTER_TOKEN={os.environ.get("TWITTER_TOKEN", "")}\n\
TWITTER_TOKEN_SECRET={os.environ.get("TWITTER_TOKEN_SECRET", "")}\n\
INSTAGRAM_LOGIN={os.environ.get("INSTAGRAM_LOGIN", "")}\n\
INSTAGRAM_PASSWORD={os.environ.get("INSTAGRAM_PASSWORD", "")}\n\
LINKEDIN_LISTENING_PORT={os.environ.get("LINKEDIN_LISTENING_PORT", "8000")}\n\
LINKEDIN_REDIRECT_URI={os.environ.get("LINKEDIN_REDIRECT_URI", "")}\n\
LINKEDIN_APP_CLIENT_ID={os.environ.get("LINKEDIN_APP_CLIENT_ID", "")}\n\
LINKEDIN_APP_CLIENT_SECRET={os.environ.get("LINKEDIN_APP_CLIENT_SECRET", "")}\n\
LINKEDIN_ACCESS_TOKEN={os.environ.get("LINKEDIN_ACCESS_TOKEN", "")}\n\
LINKEDIN_REFRESH_TOKEN={os.environ.get("LINKEDIN_REFRESH_TOKEN", "")}\n\
LINKEDIN_TOKEN_CREATED_AT={os.environ.get("LINKEDIN_TOKEN_CREATED_AT", "")}\n\
LINKED_ACCESS_TOKEN_EXPIRES_IN={os.environ.get("LINKED_ACCESS_TOKEN_EXPIRES_IN", "")}\n\
LINKED_REFRESH_TOKEN_EXPIRES_IN={os.environ.get("LINKED_REFRESH_TOKEN_EXPIRES_IN", "")}\n\
MASTODON_INSTANCE_KEYS={mastodon_instance_keys}
""")
    for mastodon in mastodons:
        file.write(f"{mastodon}\n")


def _find_dot_env():
    if DOT_ENV_PATH and os.path.exists(DOT_ENV_PATH) and os.path.isfile(DOT_ENV_PATH):
        return os.path.realpath(DOT_ENV_PATH)
    _possible_path = os.path.realpath(os.path.join(_here, "./.env"))
    if os.path.exists(_possible_path) and os.path.isfile(_possible_path):
        return _possible_path
    _possible_path = os.path.realpath(os.path.join(_here, "../.env"))
    if os.path.exists(_possible_path) and os.path.isfile(_possible_path):
        return _possible_path
    write_default_env(os.path.realpath(os.path.join(_here, "./.env")))
    return _possible_path


dot_env_path = _find_dot_env()


def dot_env_file():
    """Get the path to the .env file."""
    if os.path.exists(dot_env_path) and os.path.isfile(dot_env_path):
        return os.path.realpath(dot_env_path)
    return None


def load_env():
    """Load .env file."""
    load_dotenv(dotenv_path=dot_env_path)


__all__ = [
    "load_env",
    "dot_env_file",
    "SMTP_PORT",
    "SMTP_HOST",
    "SMTP_LOGIN",
    "SMTP_PASSWORD",
    "REQUESTS_TIMEOUT",
    "FACEBOOK_ACCESS_TOKEN",
    "TWITTER_CONSUMER_KEY",
    "TWITTER_CONSUMER_SECRET",
    "TWITTER_TOKEN",
    "TWITTER_TOKEN_SECRET",
    "INSTAGRAM_LOGIN",
    "INSTAGRAM_PASSWORD",
    "LINKEDIN_LISTENING_PORT",
    "LINKEDIN_REDIRECT_URI",
    "LINKEDIN_APP_CLIENT_ID",
    "LINKEDIN_APP_CLIENT_SECRET",
    "LINKEDIN_ACCESS_TOKEN",
    "LINKEDIN_REFRESH_TOKEN",
    "LINKEDIN_TOKEN_CREATED_AT",
    "LINKED_ACCESS_TOKEN_EXPIRES_IN",
    "LINKED_REFRESH_TOKEN_EXPIRES_IN",
    "MASTODON_INSTANCE_KEYS",
]
