# 1. import
from flask import Flask, render_template, redirect, jsonify, request
import numpy as np
import pandas as pd
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# Load the model
import tensorflow
from tensorflow import keras
from tensorflow.keras.models import load_model


#model = keras.models.load_model("housing_model.h5")
model = keras.models.load_model("housing_model.h5", compile = False)

from sqlalchemy import create_engine
import psycopg2

from config import username, password
# import os
# username = os.environ.get('DB_USER_NAME')
# password = os.environ.get('DB_PASSWORD')
# DATABASE_URL will contain the database connection string:
# database_url = os.environ.get('DATABASE_URL')

from sqlalchemy import create_engine
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/houses_db')
# engine = create_engine(database_url)
conn = engine.connect()
connection = psycopg2.connect(user = username,
                                  password = password,
                                  host = "localhost",
                                  port = "5432",
                                  database = "houses_db")

# connection = psycopg2.connect(user = username,
#                                   password = password,
#                                   host = "ec2-34-232-24-202.compute-1.amazonaws.com",
#                                   port = "5432",
#                                   database = "d9fctba151jt90")

cursor = connection.cursor()

# top10ussql = 'select "PLANT_NAME", "PLANT_DESIGN_CAPACITY_MWE" from WORLD_PLANT_LIST where "PLANT_COUNTRY" = %s ORDER BY "PLANT_DESIGN_CAPACITY_MWE" DESC NULLS LAST LIMIT 10'
# cursor.execute(top10ussql, ("United States of America",))
# top10USrecords = cursor.fetchall()

# topustypesql = 'SELECT p."TYPE", MAX(p."PLANT_DESIGN_CAPACITY_MWE") AS max_mwe FROM WORLD_PLANT_LIST p \
#     where p."PLANT_COUNTRY" = %s \
#     GROUP BY p."TYPE" \
#     ORDER BY max_mwe DESC'

# cursor.execute(topustypesql, ("United States of America",))
# topUSPlantTypeRec = cursor.fetchall()

# topworldsql = 'select "TYPE", "PLANT_DESIGN_CAPACITY_MWE", "PLANT_NAME",  "PLANT_STATE" from WORLD_PLANT_LIST  \
#     ORDER BY "PLANT_DESIGN_CAPACITY_MWE" DESC NULLS LAST LIMIT 10'
# cursor.execute(topworldsql)
# topWorldRec = cursor.fetchall()

# countrysql = 'select "PLANT_COUNTRY", "TYPE", count(*) from WORLD_PLANT_LIST  \
#     where "PLANT_COUNTRY" IS NOT NULL GROUP BY "TYPE", "PLANT_COUNTRY" '
# cursor.execute(countrysql)
# countryRec = cursor.fetchall()
#print(countryRec)

# sql2 = 'select "PLANT_NAME","PLANT_COUNTRY","PLANT_STATE","TYPE" FROM world_plant_list WHERE "TYPE" = %s and "PLANT_NAME" NOT LIKE %s ORDER BY "PLANT_DESIGN_CAPACITY_MWE" DESC FETCH FIRST 20 ROW ONLY'

# cursor.execute(sql2, ("COAL","%(Shutdown)"))
# coal_tables = cursor.fetchall()


# Set routes
@app.route('/')
def index():
    # Return the template
    return render_template('index.html')

@app.route('/introduction')
def introduction():
    # Return the template
    return render_template('introduction.html')

@app.route('/model')
def model():
    # Return the template
    return render_template('model.html')

@app.route('/plot1')
def plot1():
    # Return the template
    return render_template('plot1.html')

@app.route('/predict1')
def predict1():
    # Return the template
    return render_template('predict.html')

@app.route('/predict',methods=['POST'])
def predict():

    int_features = [int(x) for x in request.form.values()]
    final_features = []
    print(int_features)
    #   sold_price,bathroom_ct,bedroom_ct,home_sqft,zipcode,Population,Median Age,
    #   Household Income,Per Capita Income,Poverty Rate,Population 25 and Over,
    #   Rate 25 and Over w/ less than 1st grade,Rate 25 and Over w/ Some or Completed Elementary School,
    #   Rate 25 and Over w/ Some or Completed Middle School,Rate 25 and Over w/ Some High School,
    #   Rate 25 and Over w/ Completed High School or Equivalent,
    #   "Rate 25 and Over w/ Some college, less than 1 year","Rate 25 and Over w/ Some college, 1 or more years",
    #   Rate 25 and Over w/ Associate's degree,Rate 25 and Over w/ Bachelor's degree,
    #   Rate 25 and Over w/ Master's degree,Rate 25 and Over w/ Professional school degree,
    #   Rate 25 and Over w/ Doctorate degree
    zip_census_items = [19605, 39.2, 109750, 41426,	0.026472839, 12873,	0.017478443, 0.001475957,	
                        0.002252777, 0.150858386, 0.071001321, 0.184960771, 0.084284937, 0.317563893,
                        0.133069215, 0.022217043, 0.014837256, 0.022217043]
    int_features.pop(3)
    int_features.extend(zip_census_items)
    
    for feature in int_features:
        final_features.append([feature])
    
    final_features = np.array(final_features)
    print(final_features.shape)
    print(final_features)

    #df_features = pd.DataFrame(int_features) 

    new_df = pd.read_csv('random_sample_noprice.csv') 
    print(new_df)

    prediction = model.predict(new_df)

    output = round(prediction[0], 2)

    return render_template('predict.html', prediction_text='Predicted House Price: $ {}'.format(output))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

# @app.route('/top10us_data')
# def top10us_data():
#     # Return the template with the teams list passed in
#     return render_template('top10us.html', top10Rec=top10USrecords)

# @app.route('/top10us_api')
# def top10us_api():
#     # Return the template with the teams list passed in
#     return jsonify(top10USrecords)

# @app.route('/csvdata1')
# def csvdata1():
#     # Return the template
#     return render_template('data/global-primary-energy.csv')

# @app.route('/map_data')
# def map_data():
#     # Return the template
#     return render_template('data/world-power-plants-list.geojson')

# @app.route('/map')
# def map():
#     # Return the template
#     return render_template('map.html')



if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
