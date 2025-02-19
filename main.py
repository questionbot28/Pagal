import os
import logging
from dotenv import load_dotenv
from app import app
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth2Session

db = SQLAlchemy(app)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Make current_user available to templates
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    logger.error(f"Page not found: {error}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Server error: {error}")
    db.session.rollback()
    return render_template('500.html'), 500

# Routes 
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return "An error occurred", 500

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

app.secret_key = os.getenv('SESSION_SECRET', os.urandom(24))

if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=5000, debug=True)
else:
    # Production (Render)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)