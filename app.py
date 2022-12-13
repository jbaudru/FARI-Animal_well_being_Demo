from flask import Flask, jsonify, url_for, request, render_template
import json

global difficulty, score, time, vector
difficulty = 0; score = 0; time = 0; vector = []

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('rules.html', vector=vector)


@app.route('/play', methods=['GET', 'POST'])
def play():
    global difficulty, score, time, vector
    print(score)
    print(time)
    print(vector)
    data = None
    with open("staticFiles/data/ads.json") as json_file:
        data = json.load(json_file)
    return render_template('play.html', ads=data["ads"], level=difficulty, score=score, time=time, vector=vector)

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    data = None
    with open("staticFiles/data/leaderboard.json") as json_file:
        data = json.load(json_file)
    return render_template('leaderboard.html', players=data["players"], vector=vector)


@app.route('/gettimer/<jsdata>')
def get_javascript_timer(jsdata):
    global time
    time = jsdata
    return jsdata

@app.route('/getscore/<jsdata>')
def get_javascript_score(jsdata):
    global score
    score = jsdata
    return jsdata

@app.route('/getvector', methods=['GET', 'POST'])
def get_javascript_vector():
    global vector
    if request.method == 'POST':
        data = request.json
        vector = data
        return jsonify(data)
    
@app.route('/getreset/<jsdata>')
def get_javascript_reset(jsdata):
    global score, time, vector
    score = 0; time = 0; vector = []
    return jsdata

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
    if(username!="" and not username.isnumeric()):
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


if __name__ == "__main__":
    app.run()

# python -m flask --app=app --debug run --host=0.0.0.0

