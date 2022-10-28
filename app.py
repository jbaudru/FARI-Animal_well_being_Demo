from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('rules.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

    
@app.route('/send-use')
def send_use():
    pass

if __name__ == "__main__":
    app.run()

# python -m flask --app=app --debug run --host=0.0.0.0

