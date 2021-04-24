from flask import Flask, render_template, redirect, url_for, request,session
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField
from wtforms.validators import DataRequired
import mysql.connector as sql
import pandas as pd
from restaurant_analysis.sentiment_prediction import SentimentPredictor



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
predictor = SentimentPredictor()


@app.route('/', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password123':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))

    return render_template('uberlogin.html', error=error)

@app.route('/index', methods = ['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/display_sentiment', methods = ['GET','POST'])
def display_sentiment():
    rest_id = request.form.get("rest_name")

    mydb = sql.connect(host="localhost",database = 'yelp_review',user="db_user", passwd="P@s$w0rd123!")
    #mycursor = mydb.cursor()
    query = f"select text from review where business_id = '{rest_id}' LIMIT 10"
    #mycursor.execute(query,(rest_id,))
    #rest_text = mycursor.fetchall()
    #text_df = pd.DataFrame(rest_text)
    text_df = pd.read_sql(query,mydb)

    mydb.close()
    sentiment_list = []

    pred_value = predictor.predict(text_df['text'])
    acceptance_rate = sum(pred_value)/len(pred_value)*100

    print(type(pred_value))
    print(pred_value)
    pred_value = pred_value.astype('<U8')
    for idx,val in enumerate(pred_value):
        if val == '-1':
            pred_value[idx] = 'Negative'
        elif val == '1':
            pred_value[idx] = 'Positive'
        else:
            pred_value[idx] = 'Neutral'

    pred_table=zip(text_df['text'],pred_value)

    return render_template('display_sentiment.html',pred_table=pred_table,acceptance_rate=acceptance_rate)


if __name__ == '__main__':
    app.run(debug=True)
