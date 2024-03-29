## Socials
A social networks CRUD operations attempt <br>
WIP implementation of basic social networking operations like 'read', 'create', 'search', 'update', 'delete' content.<br>
Started with Facebook, Instagram, Twitter, Mastodon, LinkedIn

## Examples:
[./main.ipynb](./main.ipynb)

## Usage & Requirements

For every network, you will need authentication. <br>
You should first provide the required credentials in a dot env file (`cp env.template .env`).<br>
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
# else, an attempt to get them will be made on first run
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_REFRESH_TOKEN=
LINKEDIN_TOKEN_CREATED_AT=1604090956.07258
LINKED_ACCESS_TOKEN_EXPIRES_IN=5183999
LINKED_REFRESH_TOKEN_EXPIRES_IN=31535999
```

### LinkedIn
Make sure your app asks for the `r_liteprofile` and `w_member_social` permissions in order to get the user's urn and post on his/her behalf. <br>

![img](./docs/LinkedInScopes.png)

Make also sure, that your app is able to get both an access, and a refresh token, so we can update expired tokens. <br>

![img](./docs/LinkedInTokens.png)

### Mastodon
The good thing is that you only need to get an access_token only once (it does not expire): <br>

![img](./docs/Mastodon.png)

## Install
```
pip3 install git+https://github.com/consert/socials.git
```
or
git clone, cd to the root of this repo and run:

```
python3 setup.py install --user
```

or build a wheel and install it with pip:

```
# if not already: `pip3 install wheel`
python3 setup.py bdist_wheel
pip install --user ./dist/*.whl
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
MIT [LICENSE](./LICENSE.md)
