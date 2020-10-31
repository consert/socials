# -*- coding: utf-8 -*-
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


def _find_dot_env():
    if DOT_ENV_PATH and os.path.exists(DOT_ENV_PATH) and os.path.isfile(DOT_ENV_PATH):
        return os.path.realpath(DOT_ENV_PATH)
    _possible_path = os.path.realpath(os.path.join(_here, "./.env"))
    if os.path.exists(_possible_path) and os.path.isfile(_possible_path):
        return _possible_path
    _possible_path = os.path.realpath(os.path.join(_here, "../.env"))
    if os.path.exists(_possible_path) and os.path.isfile(_possible_path):
        return _possible_path


dot_env_path = _find_dot_env()


def dot_env_file():
    if os.path.exists(dot_env_path) and os.path.isfile(dot_env_path):
        return os.path.realpath(dot_env_path)
    return None


def load_env():
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
