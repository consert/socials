## Socials
A social networks CRUD operations attempt <br>
WIP implementation of basic social networking operations like 'read', 'create', 'search', 'update', 'delete' content.<br>
Started with Facebook, Instagram, Twitter, Mastodon, LinkedIn

## Examples:
[./main.ipynb](./main.ipynb)

## Usage & Requirements

For every network, you will need authentication. <br>
You should first provide the required credentials in a dot env file.<br>
A template is available here: [./env.template](./env.template) with contents:
 ```
FACEBOOK_ACCESS_TOKEN=

TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_TOKEN=
TWITTER_TOKEN_SECRET=

INSTAGRAM_LOGIN=
INSTAGRAM_PASSWORD=

# example (comma separated keys):
MASTODON_INSTANCE_KEYS=SCHOLAR_SOCIAL,MASTODON_SOCIAL
# use these keys to define the urls and the secrets
# SCHOLAR_SOCIAL
MASTODON_SCHOLAR_SOCIAL_URL=https://scholar.social
MASTODON_SCHOLAR_SOCIAL_TOKEN=
MASTODON_SCHOLAR_SOCIAL_CLIENT_ID=
MASTODON_SCHOLAR_SOCIAL_CLIENT_SECRET=
# MASTODON_SOCIAL
MASTODON_MASTODON_SOCIAL_URL=https://mastodon.social
MASTODON_MASTODON_SOCIAL_TOKEN=
MASTODON_MASTODON_SOCIAL_CLIENT_ID=
MASTODON_MASTODON_SOCIAL_CLIENT_SECRET=

# LINKEDIN
LINKEDIN_LISTENING_PORT=8000
LINKEDIN_REDIRECT_URI=http://localhost:8000/
LINKEDIN_APP_CLIENT_ID=
LINKEDIN_APP_CLIENT_SECRET=
# if you already have add them below:
# else, an attempt to get then will be made on first run
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_REFRESH_TOKEN=
LINKEDIN_TOKEN_CREATED_AT=1604090956.07258
LINKED_ACCESS_TOKEN_EXPIRES_IN=5183999
LINKED_REFRESH_TOKEN_EXPIRES_IN=31535999
```

## Install
git clone, cd to the root of this repo and run:
```
python3 setup.py install --user
```
or build a wheel and install it with pip:
```
python3 setup.py python sdist bdist_wheel
pip install ./dist/*.whl
```
## Libraries - Credits
The implementation either makes use or is inspired by the implementation of:<br>
[Facebook]: [https://github.com/mobolic/facebook-sdk](https://github.com/mobolic/facebook-sdk) <br>
[Mastodon]:  [https://github.com/halcy/Mastodon.py](https://github.com/halcy/Mastodon.py) <br>
[Instagram]: [https://pypi.org/project/instabot/](https://pypi.org/project/instabot/) <br>
[LinkedIn]: [https://pypi.org/project/python-linkedin-v2/](https://pypi.org/project/python-linkedin-v2/) <br>
[Twitter]: [https://pypi.org/project/requests-oauthlib/](https://pypi.org/project/requests-oauthlib/) <br>
[.env]: [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/) <br>
[requirements.txt](./requirements.txt)
## Licence
MIT [LICENSE](./LICENSE)