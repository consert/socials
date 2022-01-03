"""-*- coding: utf-8 -*-."""
import os
import requests
from typing import TYPE_CHECKING
from socials.env import LINKEDIN_ACCESS_TOKEN, REQUESTS_TIMEOUT
from socials.social_network import SocialNetwork, SocialNetworkType
from socials.sns.LinkedInAuth import (
    get_authorization_url_and_start_server,
    check_token_expiration,
)

if TYPE_CHECKING:
    from typing import Optional, Union


class LinkedIn(SocialNetwork):
    """LinkedIn Implementation."""

    access_token = None
    my_urn = None
    headers = {
        "x-li-format": "json",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    base_url = "https://api.linkedin.com/v2"

    def __init__(self, debug=False):
        """Class Initialization."""
        super().__init__(
            sn_key=SocialNetworkType.linkedin,
            debug=debug,
        )
        self.access_token = os.environ.get(LINKEDIN_ACCESS_TOKEN, None)
        if not self.access_token:
            print(
                "Could not find an existing linkedin access token, trying to get one..."
            )
            get_authorization_url_and_start_server(debug=debug)
        self.access_token = os.environ.get(LINKEDIN_ACCESS_TOKEN, None)
        if not self.access_token and self.debug:
            print("Still no access token, cannot continue :(")
            return
        check_token_expiration()
        self.headers["Authorization"] = f"Bearer {self.access_token}"
        try:
            me = self.request("GET", f"{self.base_url}/me", headers=self.headers)
            self.my_urn = f"urn:li:person:{me.get('id')}"
            if self.debug:
                print("Initialized")

        except (requests.HTTPError, Exception) as err:
            if debug:
                print("Could not get your id :(", err)

    def get(self, **kwargs):
        """Read Posts."""
        raise NotImplementedError

    def _get_media_asset_and_upload_url(self):
        """Upload a media file to LinkedIn.

        on success we get sth like:
        {
            "value": {
                "uploadMechanism": {
                    "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest": {
                        "headers": {},
                        "uploadUrl": "https://api.linkedin.com/mediaUpload/C5..
                          ....HQ/feedshare-uploadedImage/0?ca=vector_feedshare&cn=uploads&m=AQ...
                          ....J2j3A&app=19784&sync=0&v=beta&ut=2H-IhpbfXrRow1"
                    }
                },
                "mediaArtifact": "urn:li:digitalmediaMediaArtifact:(urn:li:digitalmediaAsset:C552...
                  ...yHQ,urn:li:digitalmediaMediaArtifactClass:feedshare-uploadedImage)",
                "asset": "urn:li:digitalmediaAsset:C5522AQGTYER3k3ByHQ"
            }
        }
        """
        asset = None
        upload_url = None
        url = f"{self.base_url}/assets?action=registerUpload"
        params = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": self.my_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        }
        try:
            response = requests.post(url, json=params, headers=self.headers)
            if response and response.status_code < 400:
                if self.debug:
                    print(response.json())
                value = response.json().get("value", {})
                upload_mechanism = value.get("uploadMechanism", {})
                upload_request = upload_mechanism.get(
                    "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {}
                )
                upload_url = upload_request.get("uploadUrl", None)
                asset = value.get("asset", None)
        except (KeyError, requests.HTTPError, Exception) as err:
            if self.debug:
                print("media upload registration error:", err)
        return asset, upload_url

    def _media_flow(self, media):
        # type: (Optional[Union[str, os.PathLike]]) -> Optional[str]
        local_path = self._get_local_media(media)
        if not local_path:
            return None
        try:
            # step 1: register the upload
            asset, upload_url = self._get_media_asset_and_upload_url()
            # step 2: do the actual upload
            if upload_url and asset and local_path:
                print(local_path, asset, upload_url)
                # step 2: upload the file
                # files = {"file": open(local_path, "rb")}
                response = requests.put(
                    upload_url,
                    data=open(local_path, "rb"),
                    headers={"Authorization": f"Bearer {self.access_token}"},
                )
                if self.debug:
                    print(
                        "Image uploaded :)"
                        if response.status_code < 400
                        else "Could not upload the image :("
                    )
                return asset if response.status_code < 400 else None
        except (KeyError, requests.HTTPError, Exception) as err:
            if self.debug:
                print("media upload error:", err)

        return None

    @staticmethod
    def _new_post_category(url, media, media_asset):
        share_category = "NONE"
        if url:
            share_category = "ARTICLE"
        elif media and media_asset:
            share_category = "IMAGE"
        return share_category

    def post(self, text=None, url=None, media=None, **kwargs):
        """Create a new post.

        required scope: w_member_social
        docs:
        https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin?context=linkedin/consumer/context#share-media

        """
        if not self.access_token or not text:
            if not text and self.debug:
                print("Text is required")
            return None
        _url = f"{self.base_url}/ugcPosts"
        media_asset = self._media_flow(media)
        share_content_key = "com.linkedin.ugc.ShareContent"
        try:
            share_category = self._new_post_category(url, media, media_asset)
            params = {
                "author": f"{self.my_urn}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    share_content_key: {
                        "shareCommentary": {"text": f"{text}"},
                        "shareMediaCategory": share_category,
                    },
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            }
            if share_category != "NONE":
                if share_category == "ARTICLE" and url:
                    params["specificContent"] = {
                        share_content_key: {
                            "shareCommentary": {"text": f"{text}"},
                            "shareMediaCategory": share_category,
                            "media": {"status": "READY", "originalUrl": url},
                        },
                    }
                elif media_asset and media_asset:
                    params["specificContent"] = {
                        share_content_key: {
                            "shareCommentary": {"text": f"{text}"},
                            "shareMediaCategory": share_category,
                            "media": {"status": "READY", "media": media_asset},
                        },
                    }
            response = requests.post(
                _url,
                json=params,
                headers=self.headers,
                timeout=REQUESTS_TIMEOUT,
            )
            if self.debug:
                print(response.json())
            return (
                {"message": "Post created successfully"}
                if response.status_code < 400
                else None
            )
        except (KeyError, requests.HTTPError, Exception) as err:
            if self.debug:
                print("media upload error:", err)
        return None

    def update(self, **kwargs):
        """Patch a post."""
        raise NotImplementedError

    def delete(self, **kwargs):
        """Delete a post."""
        raise NotImplementedError

    def search(self, q, **kwargs):
        """Search for posts."""
        raise NotImplementedError


if __name__ == "__main__":
    _linkedin = LinkedIn(debug=True)
