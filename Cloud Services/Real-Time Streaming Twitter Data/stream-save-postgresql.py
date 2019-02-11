from socketIO_client import SocketIO, BaseNamespace
import requests
from datetime import datetime, timedelta
from unidecode import unidecode
import re
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
from geopy.geocoders import Nominatim
import psycopg2
from config import config
import malaya
from fuzzywuzzy import fuzz

def clean(text):
    stop_words = set({'ada','inikah','sampai','adakah','inilah','sana','adakah','itu','sangat','adalah','itukah','sangatlah','adanya','itulah','saya','adapun','jadi','se','agak','jangan','seandainya','agar','janganlah','sebab','akan','jika','sebagai','aku','jikalau','sebagaimana','akulah','jua','sebanyak','akupun','juapun','sebelum','al','juga','sebelummu','alangkah','kalau','sebelumnya','allah','kami','sebenarnya','amat','kamikah','secara','antara','kamipun','sedang','antaramu','kamu','sedangkan','antaranya','kamukah','sedikit','apa','kamupun','sedikitpun','apa-apa','katakan','segala','apabila','ke','sehingga','apakah','kecuali','sejak','apapun','kelak','sekalian','atas','kembali','sekalipun','atasmu','kemudian','sekarang','atasnya','kepada','sekitar','atau','kepadaku','selain','ataukah','kepadakulah','selalu','ataupun','kepadamu','selama','bagaimana','kepadanya','selama-lamanya','bagaimanakah','kepadanyalah','seluruh','bagi','kerana','seluruhnya','bagimu','kerananya','sementara','baginya','kesan','semua','bahawa','ketika','semuanya','bahawasanya','kini','semula','bahkan','kita','senantiasa','bahwa','ku','sendiri','banyak','kurang','sentiasa','banyaknya','lagi','seolah','barangsiapa','lain','seolah-olah','bawah','lalu','seorangpun','beberapa','lamanya','separuh','begitu','langsung','sepatutnya','begitupun','lebih','seperti','belaka','maha','seraya','belum','mahu','sering','belumkah','mahukah','serta','berada','mahupun','seseorang','berapa','maka','sesiapa','berikan','malah','sesuatu','beriman','mana','sesudah','berkenaan','manakah','sesudahnya','berupa','manapun','sesungguhnya','beserta','masih','sesungguhnyakah','biarpun','masing','setelah','bila','masing-masing','setiap','bilakah','melainkan','siapa','bilamana','memang','siapakah','bisa','mempunyai','sini','boleh','mendapat','situ','bukan','mendapati','situlah','bukankah','mendapatkan','suatu','bukanlah','mengadakan','sudah','dahulu','mengapa','sudahkah','dalam','mengapakah','sungguh','dalamnya','mengenai','sungguhpun','dan','menjadi','supaya','dapat','menyebabkan','tadinya','dapati','menyebabkannya','tahukah','dapatkah','mereka','tak','dapatlah','merekalah','tanpa','dari','merekapun','tanya','daripada','meskipun','tanyakanlah','daripadaku','mu','tapi','daripadamu','nescaya','telah','daripadanya','niscaya','tentang','demi','nya','tentu','demikian','olah','terdapat','demikianlah','oleh','terhadap','dengan','orang','terhadapmu','dengannya','pada','termasuk','di','padahal','terpaksa','dia','padamu','tertentu','dialah','padanya','tetapi','didapat','paling','tiada','didapati','para','tiadakah','dimanakah','pasti','tiadalah','engkau','patut','tiap','engkaukah','patutkah','tiap-tiap','engkaulah','per','tidak','engkaupun','pergilah','tidakkah','hai','perkara','tidaklah','hampir','perkaranya','turut','hampir-hampir','perlu','untuk','hanya','pernah','untukmu','hanyalah','pertama','wahai','hendak','pula','walau','hendaklah','pun','walaupun','hingga','sahaja','ya','ia','saja','yaini','iaitu','saling','yaitu','ialah','sama','yakni','ianya','yang','inginkah','samakah','ini','sambil'})
    text = [w for w in text if not w in stop_words]
    text="".join(text)
    
    stemmer = malaya.deep_stemmer()
    text=malaya.sastrawi_stemmer(str(text))
    
    text = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text)
    
    return text

def detect_traffic(text):
    r = requests.post('http://68.183.236.113/api/', json = {'data': text})
    return r.json()

def coord(c):
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    rev = c[::-1]
    ab=''.join(c for c in str(rev) if c not in '[]')

    loc=geolocator.reverse(ab,timeout=300)
    
    if "road" not in loc.raw["address"]:
        r=None   
    else:
        road=loc.raw["address"]["road"]
        r=road
    
    #CITY
    if "city" not in loc.raw["address"]:
        c=None 
    else:
        cit=loc.raw["address"]["city"]
        c=cit
    
    #HAMLET  
    if "hamlet" not in loc.raw["address"]:
        ham=None  
    else:
        let=loc.raw["address"]["hamlet"]
        ham=let
    
    #neighbourhood
    if "neighbourhood" not in loc.raw["address"]:
        n=None  
    else:
        let=loc.raw["address"]["neighbourhood"]
        n=let
        
    if "state" not in loc.raw["address"]:
        s=None 
    else:
        let=loc.raw["address"]["state"]
        s=let
    
    return r,c,ham,n,s

def insert_vendor(textt,city,time,date,road,state,neighbourhood,hamlet,prediction):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO tweet(textt,city,time,date,road,state,neighbourhood,hamlet,prediction)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
    conn = None
    id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (textt,city,time,date,road,state,neighbourhood,hamlet,prediction,))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
    return id

consumer_key= ''
consumer_secret= ''
access_token=''
access_token_secret=''


class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            tweet = json.loads(data)
            tweettime_utc = datetime.strftime(
                datetime.strptime(
                    tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'
                )
                + timedelta(hours = 0),
                '%Y-%m-%d %H:%M:%S',
            )

            dte = datetime.strftime(
                datetime.strptime(
                    tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'
                )
                + timedelta(hours = 0),
                '%Y-%m-%d',
            )

            tme = datetime.strftime(
                datetime.strptime(
                    tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'
                )
                + timedelta(hours = 0),
                '%H:%M:%S',
            )

            text = clean(tweet['text'])
            id_str = tweet['id_str']
            screen_name = re.sub(
                r'[^\x00-\x7F]+', '', tweet['user']['screen_name']
            )
            coor = tweet['place']['bounding_box']['coordinates'][0][2]
            road,city,hamlet,ne,state = coord(coor)

            if fuzz.token_set_ratio(["trafik","traffic","jalan jem","jammed","jalan slow","traffic jammed","traffic light","jalan"], text) > 50:
                if 'yes' in detect_traffic(text)['pred_text'].lower():
                    insert_vendor(text,city,str(tme),str(dte),road,state,ne,hamlet,"yes")
                    print(dte, text)

                    
            return True

        except Exception as e:
            print(e)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    while True:
        try:
            print("boleh run")
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            stream = Stream(auth, l)
            stream.filter(
                locations = [101.418145, 2.756636, 101.736528, 3.277724]
            )
        except Exception as e:
            print('outer exception:', e)
            time.sleep(60)
            continue
