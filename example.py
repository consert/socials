# -*- coding: utf-8 -*-
import os
import sys

try:  # noqa
    from socials import Facebook, Twitter, Mastodon, LinkedIn, Instagram, SocialNetwork
except ImportError:
    try:
        # if in jupyter notebook, we get a NameError ( no: __file__)
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
    except (NameError, Exception) as e:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname("."), "..")))
    from socials import Facebook, Twitter, Mastodon, LinkedIn, Instagram, SocialNetwork


# dummy values
one_image_url = "https://picsum.photos/1024/1024"
one_post_message = (
    "U.S. reports 97,000 new coronavirus cases, biggest one-day increase on record"
)
one_post_url = "https://www.reddit.com/r/Coronavirus/comments/jl7cr7/us_reports_97000_new_coronavirus_cases_biggest/"


def facebook_example(debug=True):  # noqa
    # type: (bool) -> None
    facebook = Facebook(debug=debug)  # noqa
    # # group
    groups_response = facebook.get(id="me", fields="groups")
    group_id = None
    if groups_response and type(groups_response) == dict:
        my_groups = groups_response.get("groups", {}).get("data", [])  # noqa
        if my_groups:
            group_id = my_groups[0].get("id", None)
    # feed
    my_feed_items = facebook.get(
        id=facebook.my_id, connection_name="feed", get_all=True
    )
    if my_feed_items:
        for item in my_feed_items:
            print(item)
    # search
    places = facebook.search(
        type="place", q="McDonalds", fields="name,checkins,website,location"
    )
    print(places)
    # post text, include link
    if group_id:
        facebook.post(
            parent_object=group_id,
            connection_name="feed",
            text=one_post_message,
            url=one_post_url,
        )

    # upload local image
    one_image = facebook.download_media(one_image_url, name="a_photo")
    if one_image and os.path.exists(one_image) and os.path.isfile(one_image):
        # upload image to group
        facebook.post(media=one_image, parent_object=group_id)
        os.unlink(one_image)
    # upload image from url (downloaded locally and uploaded like above)
    facebook.post(media=one_image_url, parent_object=group_id)


def twitter_example(debug=True):  # noqa
    twitter = Twitter(debug=debug)
    twitter.post(text=one_post_message)


def mastodon_example(debug=True):  # noqa
    # type: (bool) -> None
    mastodon = Mastodon(debug=debug)
    toot = mastodon.post(text=one_post_message)
    print(toot)
    toot = mastodon.post(text=one_post_message, url=one_post_url)
    print(toot)
    toot = mastodon.post(text=one_post_message, media=one_image_url)
    print(toot)


def linkedin_example(debug=True):  # noqa
    # type: (bool) -> None
    ...
    linkedin = LinkedIn(debug=debug)
    linkedin.post(text=one_post_message)
    linkedin.post(text=one_post_message, url=one_post_url)
    linkedin.post(text="A nice picture", media=one_image_url)


def instagram_example(debug=True):  # noqa
    # type: (bool) -> None
    instagram = Instagram(debug=debug)
    instagram.post(media=one_image_url)


def sn_example(debug=True):  # noqa
    sn = SocialNetwork(debug=_debug)
    local_media_path = sn.download_media(
        one_image_url, name="a_random_image", destination_dir=os.path.realpath("."),
    )
    if os.path.exists(local_media_path):
        os.unlink(local_media_path)


def main(debug=True):
    # type: (bool) -> None
    ...
    # sn_example(debug=debug)
    # linkedin_example(debug=debug)
    # mastodon_example(debug=debug)
    # instagram_example(debug=debug)
    # facebook_example(debug=debug)
    # twitter_example(debug=debug)


if __name__ == "__main__":
    _debug = True
    main(_debug)
