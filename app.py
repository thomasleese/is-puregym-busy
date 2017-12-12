import os

import flask
import psycopg2

from chart import BusynessChart


app = flask.Flask(__name__)
database = psycopg2.connect(os.environ['DATABASE_URL'])


def get_colour(index):
    if 0 <= index <= 20:
        return '#5cb85c'
    elif 20 < index <= 50:
        return '#f0ad4e'
    else:
        return '#d9534f'


def get_busyness_data():
    cursor = database.cursor()
    cursor.execute("""
        SELECT
            to_char(date, 'ID') AS day,
            to_char(date, 'HH24') as hour,
            trunc(extract('minute' from date) / 15) as quarter,
            AVG(busyness) AS busyness
        FROM
            records
        GROUP BY
            to_char(date, 'ID'),
            to_char(date, 'HH24'),
            trunc(extract('minute' from date) / 15)
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows


@app.route('/')
def index():
    rows = get_busyness_data()
    chart = BusynessChart(rows)

    return flask.render_template('index.html', get_colour=get_colour, chart=chart)


if __name__ == '__main__':
    app.run(debug=True)
