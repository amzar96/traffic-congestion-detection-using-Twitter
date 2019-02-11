from flask import Flask,render_template,url_for,request,jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import pickle
import psycopg2
import psycopg2.extras
from socketIO_client import SocketIO, BaseNamespace
import requests
from config import config
from unidecode import unidecode

app = Flask(__name__)

clf = joblib.load('model/pipeline.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    idd =[]
    dataa =[]
    data1 = {}
    neighbourhood=[]
    road = []
    ti=[]
    c = []


    if request.method == 'POST':
        state2 = request.form['state']
        date = request.form['date']
        print(date)

        with psycopg2.connect("host= dbname= user= password=") as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                #negeri=state
                cur.execute("SELECT * FROM tweet WHERE state = '%s' AND date='%s';"%(state2,date))
                rows = cur.fetchall()
                #print ("# Individual row values accessed via column name:")
                for i in range (cur.rowcount):
                    row = rows[i]
                    i=row['id']
                    u=row['textt']
                    n=row['neighbourhood']
                    r=row['road']
                    ci=row['city']
                    t=row['time']

                    idd.append(i)
                    dataa.append(u)
                    neighbourhood.append(n)
                    road.append(r)
                    c.append(ci)
                    ti.append(t)


    return render_template('masuk.html', date=date, nh=neighbourhood, state=state2, count=cur.rowcount,id=idd,data=dataa,road=road,city=c,time=ti)


@app.route('/api', methods=['POST'])
@app.route('/api/', methods=['POST'])
def api_v1():

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
        'pred_text': pred_text
    }

    return jsonify(json_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
