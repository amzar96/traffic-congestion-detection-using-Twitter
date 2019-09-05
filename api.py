from flask import Flask, render_template, url_for, request, jsonify, abort
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import pickle
import requests
from unidecode import unidecode
import sqlite3

app = Flask(__name__)

sqlite_file = 'tweetdata.db'

clf = joblib.load('model/pipeline.pkl')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods = ['POST'])
def predict():
    conn = sqlite3.connect(sqlite_file)

    tweetl, timel, neighbourhoodl, roadl, cityl, usernamel = [],[],[],[],[],[]

    if request.method == 'POST':
        print('masuk')
        state2 = request.form['state']
        date = request.form['date']
        print(date)
        print(state2)

        try:
            cur = conn.cursor()
            cur.execute(
                'SELECT * FROM tweet WHERE state=? AND date=?', (state2, date)
            )

            rows = cur.fetchall()
            print(len(rows))
            print(type(rows))
            print(rows)

            for i in rows:
                tweet = i[0]
                timee = i[2]
                neghood = i[6]
                roadd = i[4]
                cityy = i[1]
                username = i[9]

                tweetl.append(tweet)
                timel.append(timee)
                neighbourhoodl.append(neghood)
                roadl.append(roadd)
                cityl.append(cityy)
                usernamel.append(username)

        except sqlite3.ProgrammingError as e:
            print(e)

    return render_template(
        'masuk.html',
        date = date,
        state = state2,
        result = zip(tweetl, timel, neighbourhoodl, roadl, cityl, usernamel),
    )


@app.route('/api', methods = ['POST'])
def api():
    print([request.json['data']])

    if not request.json or not 'data' in request.json:
        abort(400)

    pred = clf.predict([request.json['data']])[0]

    if pred == 1:
        pred_text = 'Yes'
    else:
        pred_text = 'No'

    json_data = {
        'status': 200,
        'data': request.json['data'],
        'pred_text': pred_text,
    }

    return jsonify(json_data), 200


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = 1)
