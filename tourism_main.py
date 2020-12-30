from flask import Flask, render_template,request,session,flash
import pandas as pd
import numpy as np
from flask_table import Table, Col
import csv
import sqlite3 as sql
import os


#building flask table for showing recommendation results
class Results(Table):
    id = Col('Id', show=False)
    title = Col('Recommendation List')

app = Flask(__name__)

#Welcome Page
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/gohome')
def homepage():
    return render_template('main_home.html')


@app.route('/signup')
def new_user():
   return render_template('signup1.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['Name']
            phonno = request.form['MobileNumber']
            email = request.form['email']
            unm = request.form['Username']
            passwd = request.form['password']
            with sql.connect("gendb.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user(name,phono,email,username,password)VALUES(?, ?, ?, ?,?)",(nm,phonno,email,unm,passwd))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("login.html")
            con.close()

@app.route('/login')
def user_login():
   return render_template("login.html")

@app.route('/user_rating')                        #-----------  First ----Und fun geppu
def user_rating():
   return render_template("rating.html")

@app.route('/logindetails',methods = ['POST', 'GET'])
def logindetails():
    if request.method=='POST':
            usrname=request.form['username']
            passwd = request.form['password']




            welc = "Welcome "

            with sql.connect("gendb.db") as con:
                cur = con.cursor()
                cur.execute("SELECT username,password FROM user where username=? ",(usrname,))
                account = cur.fetchall()

                for row in account:
                    database_user = row[0]
                    database_password = row[1]
                    if database_user == usrname and database_password==passwd:
                        #session['logged_in'] = True
                        return render_template('main_home.html', pred_welc = welc ,prediction_username = usrname)  #mulpa----------- 2nd
                    else:
                        failed_login = 'Invalid user credentials... Please Try Again!!'
                        return render_template('login.html', prediction_login_fail=failed_login)
#Rating Page
@app.route("/rating", methods=["GET", "POST"])
def rating():
    if request.method=="POST":
        return render_template('recommendation.html')
    return render_template('rating.html')

#Results Page
@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    if request.method == 'POST':
        #reading the original dataset


        #from flask import Flask, render_template, request, session, flash
        #from flask import Flask, render_template, request, session, flash
        import pandas as pd
        import numpy as np
        from flask_table import Table, Col
        import csv
        import sqlite3 as sql
        import os
        trips_df = pd.read_csv('train_main.csv', usecols=['TourId', 'Place_Name'],
                               dtype={'TourId': 'int32', 'Place_Name': 'str'})
        rating_df = pd.read_csv('rating1.csv', usecols=['userId', 'TourId', 'rating'],
                                dtype={'userId': 'int32', 'TourId': 'int32', 'rating': 'float32'})
        trips_df.head()
        rating_df.head()
        df = pd.merge(rating_df, trips_df, on='TourId')
        df.head()

        combine_trip_rating = df.dropna(axis=0, subset=['Place_Name'])
        trip_ratingCount = (combine_trip_rating.
                            groupby(by=['Place_Name'])['rating'].
                            count().
                            reset_index().
                            rename(columns={'rating': 'totalRatingCount'})
                            [['Place_Name', 'totalRatingCount']]
                            )
        trip_ratingCount.head()
        rating_with_totalRatingCount = combine_trip_rating.merge(trip_ratingCount, left_on='Place_Name',
                                                                 right_on='Place_Name',
                                                                 how='left')
        rating_with_totalRatingCount.head()
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        print(trip_ratingCount['totalRatingCount'].describe())
        popularity_threshold = 50
        rating_popular_trip = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
        rating_popular_trip.head()
        rating_popular_trip.shape
        trip_features_df = rating_popular_trip.pivot_table(index='Place_Name', columns='TourId',
                                                           values='rating').fillna(0)
        trip_features_df.head()

        from scipy.sparse import csr_matrix

        trip_features_df_matrix = csr_matrix(trip_features_df.values)

        from sklearn.neighbors import NearestNeighbors
        x = [0, 0, 0, 0]
        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(trip_features_df_matrix)
        trip_features_df.shape
        query_index = np.random.choice(trip_features_df.shape[0])
        print(query_index)
        distances, indices = model_knn.kneighbors(trip_features_df.iloc[query_index, :].values.reshape(1, -1),
                                                  n_neighbors=4)
        trip_features_df.head()
        for i in range(0, len(distances.flatten())):
            if i == 0:
                print('Recommendations for {0}:\n'.format(trip_features_df.index[query_index]))
            else:
                print('{0}: {1}, with distance of {2}:'.format(i, trip_features_df.index[indices.flatten()[i]],
                                                               distances.flatten()[i]))
                x[i] = trip_features_df.index[indices.flatten()[i]]

        print('x', x)
        prediction33 = 'Beautiful city with so many tourist attraction, which attract thousands of travellers all around the world '
        prediction44 = 'Each tourist attraction in this place promises a unique and lively experience that will leave you in awe for many days to come'
        prediction55 = 'One of the cleanest cities in India, This Place is an important business center and is known for its amazing beaches, seaports and a diverse culture.'
        if x[1] =='Mangalore' or 'Udupi' or 'Uttara Kannada':

            prediction33 = 'One of the cleanest cities in India, This Place is an important business center and is known for its amazing beaches, seaports and a diverse culture.'
        elif x[2] == 'Mysore' or 'Bangalore' or 'Ooty':
             prediction44 = 'Each tourist attraction in this place promises a unique and lively experience that will leave you in awe for many days to come'
        elif x[3] == 'Mysore' or 'Udupi' or 'Bangalore':
            prediction55 = 'Beautiful city with so many tourist attraction, which attract thousands of travellers all around the world '
        else:
            prediction33 = 'Beautiful city with so many tourist attraction, which attract thousands of travellers all around the world '
            prediction44 = 'Each tourist attraction in this place promises a unique and lively experience that will leave you in awe for many days to come'
            prediction55 = 'One of the cleanest cities in India, This Place is an important business center and is known for its amazing beaches, seaports and a diverse culture.'


        return render_template('resultpred.html', prediction=x[1],prediction3 = prediction33, prediction1=x[2], prediction4=prediction44, prediction2=x[3], prediction5= prediction55)


@app.route('/Mangalore', methods=["GET", "POST"])
def city5():
    return render_template('Places/mangalore.html')

@app.route('/predictinfo')
def predictin():
   return render_template('info.html')

@app.route('/predict',methods = ['POST', 'GET'])
def predcrop():
    if request.method == 'POST':
        x = [0,0,0,0]
        comment = request.form['comment']
        comment1 = request.form['comment1']
        comment2 = request.form['comment2']
        comment3 = request.form['comment3']
        x[0] = comment
        x[1] = comment1
        x[2] = comment2
        x[3] = comment3
        # type(data2)
        with open('b1.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x[0], x[1], x[2], x[3]])
            print("CSV File is generated")

        response = 'Review Saved Successfully'
    return render_template('review_success.html',prediction107=response)


# Now Rahul's edit begins ******
# Rendering the Places Of "read more" ******
@app.route('/Bangalore')
def city1():
   return render_template('Places/bangalore.html')

@app.route('/Bijapur')
def city2():
   return render_template('Places/bijapur.html')

@app.route('/Kuduremukh')
def city3():
   return render_template('Places/kuduremukh.html')

@app.route('/Madikeri')
def city4():
   return render_template('Places/madikeri.html')



@app.route('/Mysore')
def city6():
   return render_template('Places/mysore.html')

@app.route('/Ooty')
def city7():
   return render_template('Places/ooty.html')

@app.route('/Shimoga')
def city8():
   return render_template('Places/shimoga.html')

@app.route('/Udupi')
def city9():
   return render_template('Places/udupi.html')

@app.route('/Uttara Kannada')
def city10():
   return render_template('Places/uttaraKannada.html')

@app.route('/review_det',methods = ['POST'])
def city20():
    # copy this code-----
    from flask import request

    get_name_of_place = request.form['name_of_my_place']
    name_of_place = get_name_of_place.capitalize()

    print(" Review Place name is --------------------->",name_of_place)
    import pandas as pd

    df = pd.read_csv("b1.csv", usecols=['Rating', 'Place', 'Sub_Place', 'Review'],
                     dtype={'Rating': 'int32', 'Place': 'str', 'Sub_Place': 'str', 'Review': 'str'})

    rating = df["Rating"]
    place_type = df["Place"]
    place_name = df["Sub_Place"]
    review = df["Review"]

    lis1 = [rating, place_type, place_name, review]

    review_sec = []
    review_rev = []

    count = -1

    ex = []

    for i in review:
        review_rev.append(i)

    for i in rating:
        review_sec.append(i)


    for i in place_name:
        count = count + 1
        if (i == name_of_place):
            ex.append(count)

    print("The ex is --",ex)
    final_lis = []
    k_count = 0
    for k in ex:
        answer = str(review_sec[ex[k_count]]) +" : "+ str(review_rev[ex[k_count]])
        k_count = k_count + 1
        # print(answer)
        final_lis.append(answer)
        str1 =  '[ ' + ' ] - [ '.join(final_lis) + ' ]'
    print(str1)

    global invalid_place_name
    flag = 0
    for i in place_name:
        if (i == name_of_place):
            invalid_place_name = "Invalid Place Name!! Please Try Again"






    return render_template('Places/Review_details.html', print_answer = str1, place_name = name_of_place, invalid_place=invalid_place_name)

    # upto this -----------

@app.route('/contact',methods = ['POST', 'GET'])        # mulpa ------------------ 4th
def predcontact():
    if request.method == 'POST':
        x = [0,0,0,0]
        comment = request.form['user_name']
        comment1 = request.form['user_email']
        comment2 = request.form['user_number']
        comment3 = request.form['user_comment']
        x[0] = comment
        x[1] = comment1
        x[2] = comment2
        x[3] = comment3
        # type(data2)
        with open('b2.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x[0], x[1], x[2], x[3]])
            print("CSV File is generated")

        response = 'Thank You... Contact Saved Successfully'
    return render_template('review_success.html',prediction_contact=response)



if __name__ == '__main__':
   app.run(debug = True)
