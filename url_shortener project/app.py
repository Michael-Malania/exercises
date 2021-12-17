from base64 import b64encode
from hashlib import blake2b
import random
import re
import sqlite3 as sql
from datetime import date
import json

from src.constants import MAX_DAY_LIMIT, DIGEST_SIZE, SHORT_URL_SPECIFIER

from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

def url_valid(url):
    """Validates a url by parsing it with a regular expression. 
        and checks if url letters are less than 250 characters

    Parameters:
    url - string representing a url to be validated.

    Return values:
    Boolean, indicating the validity of the url.
    """
    return re.match(regex, url) is not None and len(url) <= 250

def shorten(url):
    """Shortens a url by generating a 9 byte hash, and then
    converting it to a 12 character long base 64 url friendly string.

    Parameters:
    url - the url to be shortened.

    Return values:
    String, the unique shortened url, acting as a key for the entered long url.
    """
    url_hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)

    while url_hash in shortened:
        url += str(random.randint(0, 9))
        url_hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)

    b64 = b64encode(url_hash.digest(), altchars=b'-_')
    return b64.decode('utf-8')


def bad_request(message):
    """Takes a supplied message and attaches it to a HttpResponse with code 400.

    Parameters:
    message - string containing the error message.

    Return values:
    An object with a message string and a status_code set to 400.
    """
    response = jsonify({'message': message})
    response.status_code = 400
    return response


@app.route('/shorten_url', methods=['POST', 'GET'])
def shorten_url():
    """POST endpoint that looks for a supplied string called "url",
    contained inside a json object. Then validates this url and
    either returns an error response as appropriate, or generates a
    shortened url, stores the shortened url, and then returns it - if valid.

    Parameters:
    None. However, the global request object should contain the aforementioned json.

    Return values:
    A response signifying success or error.
    Successes contain the shortened url, errors contain an appropriate message.
    """

    if request.method == "GET":
        url = request.args.get('url')
        premium = request.args.get('premium')
        custom_url = request.args.get('custom_url')

    elif request.method == "POST":
        url = request.json.get('url')
        premium = request.json.get('premium')
        custom_url = request.json.get('custom_url')

    # finding the server's base url address
    base_url_index = request.base_url
    base_url = base_url_index[:base_url_index.rfind('/')+1]

    if url[:4] != 'http':
        url = 'http://' + url

    if not url_valid(url):
        return bad_request('Provided url is not valid.')

    if premium:
        if not custom_url:
            return jsonify({"Error":"custom URL is not provided"}), 400
        shortened_url = custom_url
    elif custom_url:
        return jsonify({"Error":"To use custom url, premium mebership is required!"}), 400

    else:
        # For redirection purposes, we want to append http at some point.
        shortened_url = shorten(url)
    shortened[shortened_url] = url

    conn = sql.connect('urls.db')
    cursor = conn.cursor()
    today = date.today()
    current_date = today.strftime("%Y/%m/%d").split('/')

    cursor.execute('SELECT * FROM urls')
    url_table_data = [[str(item) for item in results] for results in cursor.fetchall()][-1]
    short_url = shortened_url
    short_url_from_db = SHORT_URL_SPECIFIER+url_table_data[2]
    original_url = url_table_data[1]
    if short_url == short_url_from_db:
        return (
            jsonify(
                {
                'success': True,
                'original_url': original_url,
                'short_url': base_url+short_url_from_db
                }
            ),
            200,
        )

    else:
        cursor.execute("INSERT INTO urls(original_url,short_url, url_creation_time) VALUES (?,?,?);", 
        (str(url),str(shortened_url), str(current_date)))

    cursor.execute('SELECT * FROM urls WHERE short_url=?;', (str(shortened_url),))
    conn.commit()

    return_this = [[str(item) for item in results] for results in cursor.fetchall()][0]

    shortened_url = "url/"+return_this[2]

    return jsonify(
                {'success': True,
                'original_url': url,
                'short_url': base_url+shortened_url
                }), 201



@app.route('/'+SHORT_URL_SPECIFIER+'<alias>', methods=['GET'])
def get_shortened(alias):
    """GET endpoint that takes an alias (shortened url) and redirects if successfull.
    Otherwise returns a bad request.

    Arguments:
    alias, the string representing a shortened url.

    Return values:
    A Flask redirect, with code 302.
    """
    if alias not in shortened:
        return bad_request('Unknown alias.')

    url = shortened[alias]
    con = sql.connect('urls.db')
    cur = con.cursor()

    try:
        cur.execute("UPDATE urls SET visitors=visitors+1 WHERE short_url = ?", (str(alias),))
        con.commit()
    except Exception as e:
        print(e)
        return jsonify({"error": "Please check the short_url."}), 400

    cur.close()
    con.close()
    return redirect(url, code=302)


@app.route('/stats/', methods=['GET', 'POST'])
def stats():
    '''
    Provides statistical data
    ----
    parameters: short_url
    string to be used to perform actions with the database
    ----
    return values
    json data, consists statistical information
    '''

    if request.method == "GET":
        short_url = request.args.get('url')

    elif request.method == "POST":
        short_url = request.json.get('stats')
    

    # Support for the case if user enters a full URL
    if '/' in short_url:
        short_url = short_url[short_url.rfind('/')+1:]

    con = sql.connect('urls.db')
    cur = con.cursor()
    cur.execute("SELECT visitors FROM urls WHERE short_url = ?", (str(short_url),))

    try:
        visitors = int(cur.fetchone()[0])
    except TypeError:
        return jsonify({"Error":"Provided URL could not be found in database"}), 404

    diffrence = remaning_days_validation(short_url, cur)
    
    return jsonify({"visitors":visitors,"days_left":diffrence})

def remaning_days_validation(short_url, cur):
    '''
    provides information about remaning days before URL deletion
    ----
    parameters: short_url, cur
    first parameter is used to fetch corresponding data from database,
    second one, is a cursor (cur) which is needed to comunicate with the database
    ----
    returned data:
    returns difference in days between current and user creation date
    '''

    # Fetching url creation time data from the database
    cur.execute("SELECT url_creation_time FROM urls WHERE short_url = ?", (str(short_url),))
    
    date_lst_in_str_format = cur.fetchone()[0].replace("'",'"')   

    date_of_url_creation = list(map(int,json.loads(date_lst_in_str_format))) # used json.loads and not ast.literal_eval() for code security purposes

    # getting the current date
    today = date.today()
    current_date_in_str = today.strftime("%Y/%m/%d").split('/')
    current_date = list(map(int,current_date_in_str))

    # Checking the difference between url creation and current date
    date1 = date(date_of_url_creation[0], date_of_url_creation[1], date_of_url_creation[2])
    date2 = date(current_date[0], current_date[1], current_date[2])
    diffrence_in = date2 - date1
    diffrence = MAX_DAY_LIMIT - diffrence_in.days
    if diffrence == 0:
        cur.execute("DELETE from urls WHERE short_url= ?", (str(short_url),))
    return diffrence

# Django url validator RegeEx https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
# Slightly modified to not use ftp
regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


shortened = {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)