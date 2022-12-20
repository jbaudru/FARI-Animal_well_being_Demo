from flask import Flask, jsonify, url_for, request, render_template
import json

global difficulty, score, time, vector
difficulty = 0; language= "EN"; score = 0; time = 0; vector = []; text= None

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route('/', methods=['GET', 'POST'])
def home():
    global text
    text = get_text()
    return render_template('rules.html', vector=vector, text=text)


@app.route('/play', methods=['GET', 'POST'])
def play():
    global difficulty, score, time, vector, language, text
    data = None
    if(language=="EN"):
        filename = "staticFiles/data/ads_EN.json"
    elif(language=="FR"):
        filename = "staticFiles/data/ads_FR.json"
    elif(language=="NL"):
        filename = "staticFiles/data/ads_NL.json"
    with open(filename) as json_file:
        data = json.load(json_file)
    text = get_text()
    return render_template('play.html', ads=data["ads"], level=difficulty, score=score, time=time, vector=vector, text=text)

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    global text
    data = None
    with open("staticFiles/data/leaderboard.json") as json_file:
        data = json.load(json_file)
    text = get_text()
    return render_template('leaderboard.html', players=data["players"], vector=vector, text=text)


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

@app.route('/gettext/')
def get_javascript_text():
    text = get_text()
    return text

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

@app.route('/getlanguage/<jsdata>') # Do stuff to change language
def get_javascript_lang(jsdata):
    global language
    language = "EN"
    if(jsdata=="EN"):
        language = "EN"
    elif(jsdata=="FR"):
        language = "FR"
    elif(jsdata=="NL"):
        language = "NL"
    print("Language selected: ", language)
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


def get_text():
    global language
    filename = "staticFiles/data/text_EN.json"
    if(language=="EN"):
        filename = "staticFiles/data/text_EN.json"
    elif(language=="FR"):
        filename = "staticFiles/data/text_FR.json"
    elif(language=="NL"):
        filename = "staticFiles/data/text_NL.json"
    with open(filename) as json_file:
        text = json.load(json_file)
    return text

if __name__ == "__main__":
    app.run()

# python -m flask --app=app --debug run --host=0.0.0.0

