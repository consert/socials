# -*- coding: utf-8 -*-
import os
import sys
import requests
from facebook import GraphAPI, FACEBOOK_GRAPH_URL  # noqa
from typing import TYPE_CHECKING

try:  # noqa
    from socials.env import FACEBOOK_ACCESS_TOKEN, REQUESTS_TIMEOUT
    from socials.social_network import SocialNetwork, SocialNetworkType
except ImportError:
    try:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
    except (NameError, Exception) as e:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname("."), "..")))
    from socials.env import FACEBOOK_ACCESS_TOKEN, REQUESTS_TIMEOUT
    from socials.social_network import SocialNetwork, SocialNetworkType

if TYPE_CHECKING:
    from typing import Optional, Dict, Any, Union, Generator

FACEBOOK_API_VERSION = "3.1"


class Facebook(SocialNetwork):
    graph = None
    my_id = None
    base_url = f"https://graph.facebook.com/v{FACEBOOK_API_VERSION}"

    def __init__(self, debug=False):
        super().__init__(
            sn_key=SocialNetworkType.facebook, debug=debug,
        )
        # load env vars after calling super().__init__(*args, **kwargs)
        self.access_token = os.environ.get(FACEBOOK_ACCESS_TOKEN, None)
        if self.access_token:
            try:
                self.graph = GraphAPI(
                    access_token=self.access_token,
                    timeout=REQUESTS_TIMEOUT,
                    version=FACEBOOK_API_VERSION,
                )
                me = self.graph.get_object("me", fields="id")
                self.my_id = me.get("id", None)
                if self.debug:
                    print(f"Initialized")
            except Exception as err:
                if self.debug:
                    print("ERROR: could not initialize Facebook! X_X", err)

    def search(self, q=None, **kwargs):
        """
        https://developers.facebook.com/docs/places/search
            example:
            search(type=place, q=McDonalds, fields=name,checkins,website)
            Deprecated on v8.0 :(
        """
        type_ = kwargs.get("type", None)
        fields = kwargs.get("fields", None)
        center = kwargs.get("center", None)
        distance = kwargs.get("distance", None)

        if not type_:
            return None
        if not q and not center:
            if self.debug:
                print("At least one of `q` or `center` keyword args is required")
            return None
        url = f"{self.base_url}/search?type={type_}"
        if self.debug:
            url += "&debug=all"
        if q:
            url += f"&q={q}"
        if center:
            url += f"&center={center}"
        if distance:
            url += f"&distance={distance}"
        if fields:
            url += f"&fields={fields}"
        url += f"&access_token={self.access_token}"
        try:
            response = requests.get(url, timeout=REQUESTS_TIMEOUT)
            return response.json()
        except (requests.HTTPError, Exception):
            return None

    def get(self, **kwargs):
        # type: (Any) ->  Optional[Union[Dict[str,Union[bytes,str]], Dict[str, str], Generator[Union[int,str],Any, None]]] # noqa
        if not self.my_id or not self.graph:
            if self.debug:
                print("Could not initialize me :(")
            return None
        id_ = kwargs.pop("id", None)
        ids = kwargs.pop("ids", None)
        if not id_ and not ids:
            if self.debug:
                print("At least one of ``id``, ``ids`` keyword args is required")
            return None
        if id_:
            connection_name = kwargs.pop("connection_name", None)
            if connection_name:
                get_all = kwargs.pop("get_all", False)
                if get_all:
                    return self.graph.get_all_connections(
                        id_, connection_name=connection_name, **kwargs
                    )
                return self.graph.get_connections(
                    id_, connection_name=connection_name, **kwargs
                )
            return self.graph.get_object(id_, **kwargs)
        return self.graph.get_objects(ids, **kwargs)

    def post(self, text=None, url=None, media=None, **kwargs):
        parent_object = kwargs.get("parent_object", "me")
        connection_name = kwargs.get("connection_name", "feed")
        response = None
        try:
            if media:
                url = f"{FACEBOOK_GRAPH_URL}/{parent_object}/photos?access_token={self.access_token}"
                if os.path.exists(media):
                    name = os.path.split(media)[-1]
                    files = {name: open(media, "rb")}
                    response = requests.post(url, files=files)
                else:
                    local_path = self.download_media(media)
                    if local_path and os.path.exists(local_path):
                        name = os.path.split(local_path)[-1]
                        files = {name: open(local_path, "rb")}
                        response = requests.post(url, files=files)
                        os.unlink(local_path)
            else:
                if url:
                    response = self.graph.put_object(
                        parent_object=parent_object,
                        connection_name=connection_name,
                        message=text,
                        link=url,
                    )
                else:
                    response = self.graph.put_object(
                        parent_object=parent_object,
                        connection_name=connection_name,
                        message=text,
                    )
                if self.debug:
                    print(response)
            return response
        except Exception as err:
            print("ERROR: could not post stuff on Facebook! X_X", err)
            return None

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self, **kwargs):
        raise NotImplementedError


if __name__ == "__main__":
    _facebook = Facebook(debug=True)
    print(
        _facebook.search(
            type="place", q="McDonalds", fields="name,checkins,website,location"
        )
    )
