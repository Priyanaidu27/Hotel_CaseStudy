# loading libraires
from flask import Flask  , render_template , request ,session, redirect
import mysql.connector
import pickle
import numpy as np
# connecting sql database

connection = mysql.connector.connect(host="localhost",user="root",password="",database="hotel_details",port="3306")
cursor = connection.cursor()

# loading model
model = pickle.load(open('pipeline.pkl', 'rb'))

# application
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('home.html')

# normalization function
def norm_func(i , maxi , mini):
    x = (i- mini)/(maxi-mini)
    return (x)

@app.route('/result' , methods=['POST'])
def result():
    ratings = float(request.form.get('ratings'))
    imp_count = float(request.form.get('imp_count'))
    click_count = float(request.form.get('click_count'))
    booking_count = float(request.form.get('booking_count'))
    avg_cpc = float(request.form.get('avg_cpc'))
    avg_clicked_price = float(request.form.get('avg_clicked_price'))
    avg_length_of_stay = float(request.form.get('avg_length_of_stay'))
    avg_time_to_travel = float(request.form.get('avg_time_to_travel'))
    stars = request.form.get('stars')
    if(stars == '0'):
        star_0 = 1
        star_1 = 0
        star_2 = 0
        star_3 = 0
        star_4 = 0
        star_5 = 0
    elif(stars == '1'):
        star_0 = 0
        star_1 = 1
        star_2 = 0
        star_3 = 0
        star_4 = 0
        star_5 = 0
    elif(stars == '2'):
        star_0 = 0
        star_1 = 0
        star_2 = 1
        star_3 = 0
        star_4 = 0
        star_5 = 0
    elif(stars == '3'):
        star_0 = 0
        star_1 = 0
        star_2 = 0
        star_3 = 1
        star_4 = 0
        star_5 = 0
    elif(stars == '4'):
        star_0 = 0
        star_1 = 0
        star_2 = 0
        star_3 = 0
        star_4 = 1
        star_5 = 0
    elif(stars == '5'):
        star_0 = 0
        star_1 = 0
        star_2 = 0
        star_3 = 0
        star_4 = 0
        star_5 = 1

    # # normalizing the data
    # ratings = float(norm_func(ratings , 87.020000, 74.910000))
    # imp_count = float(norm_func(imp_count, 990.00000, 28.00000))
    # click_count = float(norm_func(click_count, 18.000000, 2.000000))
    # booking_count = float(norm_func(booking_count, 8.00000, 0.00000))
    # avg_cpc = float(norm_func(avg_cpc, 1.56000, 0.71000))
    # avg_clicked_price = float(norm_func(avg_clicked_price, 230.12000, 89.02000))
    # avg_length_of_stay = float(norm_func(avg_length_of_stay, 3.5000, 1.6000))
    # avg_time_to_travel = float(norm_func(avg_time_to_travel, 60.8600, 13.0000))

    predict = model.predict([[ratings,imp_count,click_count,booking_count,avg_cpc,avg_clicked_price,avg_length_of_stay,avg_time_to_travel,star_0,star_1,star_2,star_3,star_4,star_5]])
    print(predict)
    if(predict == [0]):
        predict = 'Hanoi'
    elif(predict == [1]):
        predict = 'Los Angelos'
    elif(predict == [2]):
        predict = 'Miami'
    elif(predict == [3]):
        predict = 'New York'
    elif(predict == [4]):
        predict = 'Rio de Janerio'
    elif(predict == [5]):
        predict = 'Stockholm'

    cursor.execute("""INSERT INTO hotel_details (User_id,hotel_rating,impression_count,click_count,booking_count,avg_cpc,avg_clicked_price,avg_length_of_stay,avg_time_to_travel,stars,cities) VALUES ('Null','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(ratings,imp_count,click_count,booking_count,avg_cpc,avg_clicked_price,avg_length_of_stay,avg_time_to_travel,stars,predict))
    connection.commit()
    return render_template('home.html' , predict ='Output is {}'.format(predict))


if __name__ == "__main__":
    app.run(debug=True)
