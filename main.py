from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/education')
def education():
    return render_template('education.html')

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