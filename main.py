from flask import Flask, render_template, redirect, session, request, url_for
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

DISCORD_CLIENT_ID = "1159874534485262410"
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI', 'https://your-repl-url/callback')
DISCORD_BOT_INVITE = "https://discord.com/oauth2/authorize?client_id=1159874534485262410&permissions=8&integration_type=0&scope=bot"
DISCORD_SERVER_INVITE = "https://discord.gg/J3paY6YQkZ"

API_ENDPOINT = 'https://discord.com/api/v10'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/education')
def education():
    return render_template('education.html')


@app.route('/login')
def login():
    discord = OAuth2Session(DISCORD_CLIENT_ID, redirect_uri=DISCORD_REDIRECT_URI, 
                          scope=['identify', 'email'])
    authorization_url, state = discord.authorization_url(
        'https://discord.com/api/oauth2/authorize')
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    discord = OAuth2Session(DISCORD_CLIENT_ID, redirect_uri=DISCORD_REDIRECT_URI,
                          state=session.get('oauth2_state'))
    token = discord.fetch_token(
        'https://discord.com/api/oauth2/token',
        client_secret=DISCORD_CLIENT_SECRET,
        authorization_response=request.url)
    
    session['discord_token'] = token
    user = discord.get(f'{API_ENDPOINT}/users/@me').json()
    session['user'] = user
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/api/user')
def get_user():
    if 'user' in session:
        return session['user']
    return {'error': 'Not logged in'}, 401

@app.route('/ticket')
def ticket():
    return render_template('ticket.html')

@app.route('/ai-chat')
def ai_chat():
    return render_template('ai-chat.html')

@app.route('/support')
def support():
    return render_template('support.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)