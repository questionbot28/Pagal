import os
from flask import Blueprint, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required
from requests_oauthlib import OAuth2Session
from models import User, db

DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

API_BASE_URL = 'https://discord.com/api'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

if 'REPLIT_DEV_DOMAIN' in os.environ:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

discord_auth = Blueprint('discord_auth', __name__)

def token_updater(token):
    session['oauth2_token'] = token

def make_discord_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=DISCORD_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=DISCORD_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': DISCORD_CLIENT_ID,
            'client_secret': DISCORD_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

@discord_auth.route('/login')
def login():
    scope = ['identify']
    discord = make_discord_session(scope=scope)
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@discord_auth.route('/callback')
def callback():
    if request.values.get('error'):
        return redirect(url_for('index'))
    
    discord = make_discord_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=DISCORD_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token

    discord = make_discord_session(token=token)
    user_data = discord.get(API_BASE_URL + '/users/@me').json()

    # Get or create user
    user = User.query.filter_by(discord_id=user_data['id']).first()
    if not user:
        user = User(
            discord_id=user_data['id'],
            username=user_data['username'],
            discriminator=user_data.get('discriminator', '0000'),
            avatar=user_data.get('avatar')
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update user data
        user.username = user_data['username']
        user.discriminator = user_data.get('discriminator', '0000')
        user.avatar = user_data.get('avatar')
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

@discord_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
