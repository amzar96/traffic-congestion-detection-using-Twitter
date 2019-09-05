import sqlite3

sqlite_file = './tweetdata.db'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()


textt, city, time, date, road, state, neighbourhood, hamlet, prediction = (
    'test1',
    'test2',
    'test3',
    'test4',
    'test5',
    'test6',
    'test7',
    'test8',
    'test9',
)


try:
    sql = """INSERT INTO tweet(textt,city,time,date,road,state,neighbourhood,hamlet,prediction) VALUES (?,?,?,?,?,?,?,?,?)"""

    cur = conn.cursor()
    cur.execute(
        sql,
        (
            'test1',
            'test2',
            'test3',
            'test4',
            'test5',
            'test6',
            'test7',
            'test8',
            'test9',
        ),
    )
    print("success")
except sqlite3.ProgrammingError as e:
    print(e)


conn.commit()
cur.close()
