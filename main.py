import os
from flask import render_template, redirect, session, request, url_for
from app import app
from dotenv import load_dotenv
import logging
from flask_login import current_user, login_required

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app.secret_key = os.getenv('SESSION_SECRET', os.urandom(24))

# Make current_user available to templates
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

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
    logger.info("Starting Discord OAuth login process")
    discord = OAuth2Session(os.getenv('DISCORD_CLIENT_ID'), redirect_uri=os.getenv('DISCORD_REDIRECT_URI'), 
                          scope=['identify', 'email'])
    authorization_url, state = discord.authorization_url(
        'https://discord.com/api/oauth2/authorize')
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    logger.info("Received OAuth callback")
    try:
        discord = OAuth2Session(os.getenv('DISCORD_CLIENT_ID'), redirect_uri=os.getenv('DISCORD_REDIRECT_URI'),
                              state=session.get('oauth2_state'))
        token = discord.fetch_token(
            'https://discord.com/api/oauth2/token',
            client_secret=os.getenv('DISCORD_CLIENT_SECRET'),
            authorization_response=request.url)

        session['discord_token'] = token
        user = discord.get(f'https://discord.com/api/v10/users/@me').json()
        session['user'] = user
        logger.info(f"Successfully authenticated user: {user.get('username')}")
        return redirect('/')
    except Exception as e:
        logger.error(f"Error during OAuth callback: {str(e)}")
        return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logger.info("User logged out")
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
else:
    # In production (Render)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)