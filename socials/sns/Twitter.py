# -*- coding: utf-8 -*-
import os
import sys
import requests
from requests_oauthlib import OAuth1  # noqa

try:  # noqa
    from socials.env import (
        TWITTER_TOKEN,
        TWITTER_TOKEN_SECRET,
        TWITTER_CONSUMER_SECRET,
        TWITTER_CONSUMER_KEY,
    )
    from socials.social_network import SocialNetwork, SocialNetworkType
except ImportError:
    try:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
    except (NameError, Exception) as e:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname("."), "..")))
    from socials.env import (
        TWITTER_TOKEN,
        TWITTER_TOKEN_SECRET,
        TWITTER_CONSUMER_SECRET,
        TWITTER_CONSUMER_KEY,
    )
    from socials.social_network import SocialNetwork, SocialNetworkType


class Twitter(SocialNetwork):

    url_posting = "https://api.twitter.com/1.1/statuses/update.json"
    header_oauth = None

    def __init__(self, debug=False):
        super().__init__(
            sn_key=SocialNetworkType.twitter, debug=debug,
        )
        consumer_key = os.environ.get(TWITTER_CONSUMER_KEY, None)
        consumer_secret = os.environ.get(TWITTER_CONSUMER_SECRET, None)
        consumer_token = os.environ.get(TWITTER_TOKEN, None)
        consumer_token_secret = os.environ.get(TWITTER_TOKEN_SECRET, None)
        if (
            consumer_key
            and consumer_secret
            and consumer_token
            and consumer_token_secret
        ):
            self.header_oauth = OAuth1(
                consumer_key,
                consumer_secret,
                consumer_token,
                consumer_token_secret,
                signature_type="auth_header",
            )
            if self.debug:
                print("Initialized")

    def get(self, **kwargs):
        raise NotImplementedError

    def post(self, text=None, url=None, media=None, **kwargs):
        if not self.header_oauth:
            raise RuntimeError(
                "Could not construct the authentication header parameters"
            )
        payload = {"status": text}
        r = requests.post(self.url_posting, auth=self.header_oauth, data=payload)
        if r.status_code == 201 or r.status_code == 200:
            return True
        return False

    def search(self, q, **kwargs):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self, **kwargs):
        raise NotImplementedError
