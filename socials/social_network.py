# -*- coding: utf-8 -*-
import os
from enum import Enum
import tempfile
import requests
import shutil
import imghdr
from socials.env import load_env, REQUESTS_TIMEOUT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Any, Union, Dict, Generator


class SocialNetworkType(str, Enum):
    none = "none"
    facebook = "facebook"
    twitter = "twitter"
    instagram = "instagram"
    mastodon = "mastodon"
    linkedin = "linkedin"


class SocialNetwork(object):
    """
        Abstract Social Network class.

        Inherit this class and implement any of the
        ``get``, ``post``, ``update``, ``delete``, ``search``
        methods you want to use

    """

    def __init__(
        self, sn_key=SocialNetworkType.none, debug=False,
    ):
        # type: (SocialNetworkType, bool) -> None
        load_env()
        self.debug = debug  # type: bool
        self.sn_key = sn_key  # type: SocialNetworkType

    def request(
        self,
        method,  # type: str
        url,  # type: str
        data=None,  # type: Optional[str]
        params=None,  # type: Optional[dict]
        headers=None,  # type: Optional[dict]
        timeout=REQUESTS_TIMEOUT,  # type: Optional[int]
    ):
        # type: (...) ->  Optional[Union[Dict[str,Union[bytes,str]], Dict[str, str]]]
        """
        General purpose request.

        method: one of: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``
        """
        if headers is None:
            headers = {}
        if "Content-Type" not in headers:
            headers.update({"Content-Type": "application/json"})

        if params is None:
            params = {}
        kw = dict(data=data, params=params, headers=headers, timeout=timeout)

        try:
            response = requests.request(method.upper(), url, **kw)
            return response.json() if response.status_code < 400 else None
        except (requests.HTTPError, Exception) as e:
            if self.debug:
                print(f"{method} request error:", e)
            return None

    def _get_local_media(self, media):
        # type: (Optional[Union[str, os.PathLike]]) -> Optional[str]
        if not media:
            return None
        if os.path.exists(media) and os.path.isfile(media):
            return os.path.realpath(media)
        media = str(media)
        local_path = self.download_media(media)
        if not os.path.exists(local_path):  # noqa
            if self.debug:
                print("Could nof find the local path of the image")
            return None

        return local_path

    def download_media(
        self,
        media_url,  # type: str
        name=None,  # type: Optional[str]
        destination_dir=None,  # type: Optional[Union[str, os.PathLike]]
    ):
        # type: (...) -> Optional[str]
        filename = media_url.split("/")[-1] if not name else name
        filename = filename.split(".")[-1]
        if not destination_dir or not os.path.exists(destination_dir):
            destination_dir = tempfile.gettempdir()
        destination_path = os.path.join(destination_dir, filename)
        response = requests.get(media_url, stream=True, timeout=REQUESTS_TIMEOUT)
        if response.status_code == 200:
            response.raw.decode_content = True
            with open(destination_path, "wb") as f:
                shutil.copyfileobj(response.raw, f)
            if os.path.exists(destination_path):
                _extension = imghdr.what(destination_path)
                new_destination = destination_path.replace(
                    filename, f"{filename}.{_extension}"
                )
                if _extension:
                    shutil.move(destination_path, new_destination)
                    destination_path = new_destination
            if self.debug:
                print(f"Image successfully saved: {destination_path}")
            return destination_path
        if self.debug:
            print(response.text)
        return None

    def search(self, q, **kwargs):
        # type: (str, Any) ->  Optional[Union[Dict[str,Union[bytes,str]], Dict[str, str]]]
        """
        Search for sth in a social network.

        For every SN implementation i.e.:
            class ANewSN(SocialNetwork):
                ....

        this function has to be overridden / implemented

        :param q: the search query
        :param kwargs: additional kwargs
        :return: the search response
        """
        raise NotImplementedError

    def get(self, **kwargs):
        # type: (Any) ->  Optional[Union[Dict[str,Union[bytes,str]], Dict[str, str], Generator]]
        """
        For every SN implementation i.e.:
            class ANewSN(SocialNetwork):
                ....

        this function has to be overridden / implemented

        :param kwargs: keywords to include on the query
        :return: the GET response
        """
        raise NotImplementedError

    def post(
        self,
        text=None,  # type: Optional[str]
        url=None,  # type: Optional[str]
        media=None,  # type: Optional[Union[str, os.PathLike]]
        **kwargs,  # type: Any
    ):
        # type: ( ...) ->  Optional[Union[Dict[str,Union[bytes,str]], Dict[str, str]]]
        """
        Post content to a social network.

        For every SN implementation i.e.:
            class ANewSN(SocialNetwork):
                ....

        this function has to be overridden / implemented
        """
        raise NotImplementedError

    def update(self, **kwargs):
        # type: (Any) -> Optional[Union[Dict[str,Union[bytes,str]], Dict[str, str]]]
        """
        Update content to a social network.

        For every SN implementation i.e.:
            class ANewSN(SocialNetwork):
                ....

        this function has to be overridden / implemented
        """
        raise NotImplementedError

    def delete(self, **kwargs):
        # type: (Any) -> Optional[Union[Dict[str,Union[bytes,str]], Dict[str, str]]]
        """
       Delete content from a social network.

       For every SN implementation i.e.:
           class ANewSN(SocialNetwork):
               ....

       this function has to be overridden / implemented
       """
        raise NotImplementedError
