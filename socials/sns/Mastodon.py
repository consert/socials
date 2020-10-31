# -*- coding: utf-8 -*-
import os
import sys
from typing import List

from mastodon import Mastodon as MastodonPy, MastodonError  # noqa

try:  # noqa
    from socials.social_network import SocialNetwork, SocialNetworkType
    from socials.env import MASTODON_INSTANCE_KEYS
except ImportError:
    try:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
    except (NameError, Exception) as e:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname("."), "..")))
    from socials.social_network import SocialNetwork, SocialNetworkType
    from socials.env import MASTODON_INSTANCE_KEYS


class Mastodon(SocialNetwork):
    instances = []  # type: List[MastodonPy]

    def __init__(self, debug=False):
        super().__init__(
            sn_key=SocialNetworkType.mastodon, debug=debug,
        )
        instance_keys_string = os.environ.get(MASTODON_INSTANCE_KEYS, None)
        if not instance_keys_string:
            raise RuntimeError("No Mastodon instances?")
        instance_keys = instance_keys_string.split(",")
        for instance_key in instance_keys:
            _instance_url_key = f"MASTODON_{instance_key}_URL"
            _instance_token_key = f"MASTODON_{instance_key}_TOKEN"
            instance_url = os.environ.get(_instance_url_key, None)
            instance_token = os.environ.get(_instance_token_key, None)
            if instance_url and instance_token:
                try:
                    instance = MastodonPy(
                        access_token=instance_token,
                        api_base_url=instance_url,
                        version_check_mode="none",
                    )
                    instance.account_verify_credentials()
                    self.instances.append(instance)
                except (MastodonError, Exception):
                    pass
        if not self.instances:
            raise RuntimeError("No (valid) Mastodon instances could be loaded :(")

    def get(self, **kwargs):
        raise NotImplementedError

    def _image_upload(self, local_media_path, instance):
        image_id = None
        if local_media_path:
            try:
                image_dict = instance.media_post(local_media_path)
                image_id = image_dict.get("id", None)
            except (MastodonError, Exception) as err:
                if self.debug:
                    print("Could not post :(", err)
        return image_id

    @staticmethod
    def _post_text(text, url):
        status = text
        if url:
            status = f"{text}\n{url}" if text else url
        return status

    def post(self, text=None, url=None, media=None, **kwargs):
        if not text and not url and not media:
            print("Post nothing ?")
            return None
        try:
            if self.instances:
                responses = []
                local_media_path = self._get_local_media(media)
                for instance in self.instances:
                    image_id = self._image_upload(local_media_path, instance)
                    status = self._post_text(text=text, url=url)
                    if image_id or not status:
                        status = ""
                        response = instance.status_post(
                            status=status, media_ids=[image_id]
                        )
                    else:
                        response = instance.toot(status=status)
                    responses.append(response)
                return {"result": responses}

        except (MastodonError, Exception) as err:
            if self.debug:
                print("Could not post :(", err)
        return None

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self, **kwargs):
        raise NotImplementedError

    def search(self, q, **kwargs):
        raise NotImplementedError


if __name__ == "__main__":
    _mastodon = Mastodon(debug=True)
