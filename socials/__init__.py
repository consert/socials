# -*- coding: utf-8 -*-
import os
import sys

try:  # noqa
    from .sns import Facebook, Instagram, LinkedIn, Twitter, Mastodon
    from .social_network import SocialNetwork
except ImportError:
    try:
        # if in jupyter notebook, we get a NameError ( no: __file__)
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
    except (NameError, Exception) as e:
        sys.path.append(os.path.realpath(os.path.join(os.path.dirname("."), "..")))
    from socials.sns import Facebook, Instagram, LinkedIn, Twitter, Mastodon
    from socials import SocialNetwork

__all__ = ["Facebook", "Instagram", "LinkedIn", "Twitter", "Mastodon", "SocialNetwork"]
