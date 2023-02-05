
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, request, jsonify, make_response
from datacleansing import upload_file, text
import sqlite3
import pandas as pd

# instantiate flask object
app = Flask(__name__)
# set app configs
app.config['JSON_SORT_KEYS'] = False 

# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swag.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Tworst!"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# Database
db = sqlite3.connect('database.db', check_same_thread=False) 
db.row_factory = sqlite3.Row
mycursor = db.cursor()

# error handling
@app.errorhandler(400)
def handle_400_error(_error):
    "Return a http 400 error to client"
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    "Return a http 401 error to client"
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    "Return a http 404 error to client"
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    "Return a http 500 error to client"
    return make_response(jsonify({'error': 'Server error'}), 500)





# Tweet
#post tweet
@app.route("/tweet", methods=["POST"])
def tweet():
    input = str(request.form["text"])
    output = text(input)
    database = "insert into tweet (tweet_dummy,tweet_bersih) values (?,?)"
    variable = (input, output)
    mycursor.execute(database, variable)
    db.commit()
    print(input)
    print(output)
    return "Success Input Data"

    
#get tweet
@app.route("/tweet", methods = ["GET"])
def get_tweet():    
    data_query = "select * from tweet"
    #execute data_query
    select_tweet_from_data_query = mycursor.execute(data_query)
    tweet = [dict(tweet_id=row[0], tweet_dummy=row[1], tweet_bersih=row[2])for row in select_tweet_from_data_query.fetchall()]
    return jsonify(tweet)



#melakukan dalate
@app.route("/tweet/<string:tweet_id>", methods=["DELETE"])
def tweet_id(tweet_id):
    data_query= "delete from tweet where tweet_id = ?"
    variable = tweet_id
    mycursor.execute(data_query, [variable])
    db.commit()
    return "Success Delete Data"




# Upload File
@app.route("/tweet/csv", methods=["POST"])
def tweet_csv():
    #melakukan request file yang akan di upload
    file = request.files['file'] 
    try: data = pd.read_csv(file, encoding='iso-8859-1')
    except:data = pd.read_csv(file, encoding='utf-8') 
    #melakukan proses upload scv
    upload_file(data)
    return data


#Run Server
if __name__ == '__main__':
    app.run(debug=True)
