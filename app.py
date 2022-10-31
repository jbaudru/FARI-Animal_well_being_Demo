from flask import Flask, redirect, url_for, request, render_template
import json

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('rules.html')

@app.route('/play')
def play():
    data = None
    with open("staticFiles/data/ads.json") as json_file:
        data = json.load(json_file)

    return render_template('play.html', ads=data["ads"])

@app.route('/leaderboard')
def leaderboard():
    data = None
    with open("staticFiles/data/leaderboard.json") as json_file:
        data = json.load(json_file)
    return render_template('leaderboard.html', players=data["players"])


if __name__ == "__main__":
    app.run()

# python -m flask --app=app --debug run --host=0.0.0.0

