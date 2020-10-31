# -*- coding: utf-8 -*-
import logging
import os
from typing import TYPE_CHECKING
from instabot import Bot  # noqa
from socials.social_network import SocialNetwork, SocialNetworkType
from socials.env import INSTAGRAM_LOGIN, INSTAGRAM_PASSWORD

if TYPE_CHECKING:
    from typing import Optional


class Instagram(SocialNetwork):
    instance = None  # type: Optional[Bot]

    def __init__(self, debug=False):
        super().__init__(
            sn_key=SocialNetworkType.instagram, debug=debug,
        )
        instagram_login = os.environ.get(INSTAGRAM_LOGIN, None)
        instagram_password = os.environ.get(INSTAGRAM_PASSWORD, None)
        if instagram_login and instagram_password:
            try:
                self.instance = Bot(
                    verbosity=self.debug,
                    loglevel_file=logging.DEBUG if self.debug else logging.ERROR,
                    loglevel_stream=logging.DEBUG if self.debug else logging.ERROR,
                )
                if not self.instance.login(
                    username=instagram_login, password=instagram_password
                ):
                    self.instance = None
            except Exception as err:
                print(err)
                raise err
        if not self.instance:
            raise RuntimeError("Could not initialize Instagram")

    def get(self, **kwargs):
        if not self.instance:
            return None
        # TODO: check from kwargs what to get, example:
        # self.instance.get_messages()
        raise NotImplementedError

    def post(self, text=None, url=None, media=None, **kwargs):
        if media is None:
            raise ValueError("A media file (photo) is required")
        remove_after_upload = False
        response = None
        if self.instance:
            if os.path.exists(media) and os.path.isfile(media):
                photo_path = media
            else:
                photo_path = self.download_media(media)
                remove_after_upload = True
            if photo_path and os.path.exists(photo_path):
                success = self.instance.upload_photo(
                    photo_path, caption=text, options={"rename": remove_after_upload}
                )
                if success:
                    response = {"message": "Image successfully uploaded"}
        return response

    def search(self, q, **kwargs):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self, **kwargs):
        raise NotImplementedError


if __name__ == "__main__":
    _instagram = Instagram(debug=True)
    _instagram.post(media="/home/username/Pictures/image_file.jpg")
