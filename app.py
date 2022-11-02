from flask import Flask, redirect, url_for, request, render_template
import json

global difficulty 

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('rules.html')


@app.route('/play', methods=['GET', 'POST'])
def play():
    global difficulty
    data = None
    with open("staticFiles/data/ads.json") as json_file:
        data = json.load(json_file)

    return render_template('play.html', ads=data["ads"], level=difficulty)


@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):
    global difficulty
    difficulty = 0
    if(jsdata=="eazy"):
        difficulty = 0
    elif(jsdata=="normal"):
        difficulty = 1
    elif(jsdata=="hard"):
        difficulty = 2
    print("Level of difficuly selected: ", difficulty)
    return jsdata

@app.route('/getusername/<jsdata>')
def get_user_data(jsdata):
    username = jsdata.split("---")[0]
    score = jsdata.split("---")[1]
    print("New score by :", username, "with", score)
    leaderboard = {}
    with open("staticFiles/data/leaderboard.json", 'r') as openfile:
        leaderboard = json.load(openfile)
    tmp_dict = {'pseudo': username, 'score': int(score)}
    leaderboard["players"].append(tmp_dict)

    json_object = json.dumps(leaderboard, indent=4)
    with open("staticFiles/data/leaderboard.json", "w") as outfile:
        outfile.write(json_object)
    return jsdata


@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    data = None
    with open("staticFiles/data/leaderboard.json") as json_file:
        data = json.load(json_file)
    return render_template('leaderboard.html', players=data["players"])


if __name__ == "__main__":
    app.run()

# python -m flask --app=app --debug run --host=0.0.0.0

