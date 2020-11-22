# 1. import
from flask import Flask, render_template, redirect, jsonify, request
import numpy as np
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# Load the model
import tensorflow
from tensorflow import keras
from tensorflow.keras.models import load_model
model = load_model("housing_model.h5", compile = False)


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

# cursor.execute(sql2, ("GAS","%(Decommissioned)"))
# gas_tables = cursor.fetchall()

# cursor.execute(sql2, ("OIL","%(Shutdown)"))
# oil_tables = cursor.fetchall()

# cursor.execute(sql2, ("HYDRO","%(Shutdown)"))
# hydro_tables = cursor.fetchall()

# cursor.execute(sql2, ("NUCLEAR","%(Shutdown)"))
# nuclear_tables = cursor.fetchall()

# cursor.execute(sql2, ("WIND","%(Shutdown)"))
# wind_tables = cursor.fetchall()

# cursor.execute(sql2, ("SOLAR_PV","%(Shutdown)"))
# solar_tables = cursor.fetchall()


# Set routes
@app.route('/')
def index():
    # Return the template
    return render_template('index.html')

@app.route('/introduction')
def introduction():
    # Return the template
    return render_template('introduction.html')

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
                        0.133069215, 0.022217043, 0.014837256, 0.022217043, 0.014837256]
    int_features.pop(3)
    int_features.extend(zip_census_items)
    
    for feature in int_features:
        final_features.append([feature])
    
    final_features = np.array(final_features)
    print(final_features.shape)
    print(final_features)

    prediction = model.predict(final_features)

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

# @app.route('/topusplanttype_data')
# def topusplanttype_data():
#     # Return the template with the teams list passed in
#     return render_template('topusplanttype.html', top10Rec=topUSPlantTypeRec)

# @app.route('/topusplanttype_api')
# def topusplanttype_api():
#     # Return the template with the teams list passed in
#     return jsonify(topUSPlantTypeRec)

# @app.route('/topworld_data')
# def topworld_data():
#     # Return the template with the teams list passed in
#     return render_template('topworld.html', top10Rec=topWorldRec)

# @app.route('/topworld_api')
# def topworld_api():
#     # Return the template with the teams list passed in
#     return jsonify(topWorldRec)

# @app.route('/country_data')
# def country_data():
#     # Return the template with the teams list passed in
#     return render_template('country.html', top10Rec=countryRec)

# @app.route('/country_api')
# def country_api():
#     # Return the template with the teams list passed in
#     return jsonify(countryRec)
  
# @app.route('/consumption')
# def consumption():
#     # Return the template
#     return render_template('consumption.html')   

# @app.route('/production')
# def production():
#     # Return the template
#     return render_template('production.html')

# @app.route('/consumption2')
# def production2():
#     # Return the template
#     return render_template('consumption2.html')

# @app.route('/datasources')
# def datasources():
#     # Return the template
#     return render_template('datasources.html')

# @app.route('/fundamentals')
# def fundamentals():
#     # Return the template
#     return render_template('fundamentals.html')

# @app.route('/fundamentals_raw')
# def fundamentals_raw():
#     # Return the template
#     return render_template('fundamentals_raw.html')

# @app.route('/csvdata1')
# def csvdata1():
#     # Return the template
#     return render_template('data/global-primary-energy.csv')

# @app.route('/csvdata2')
# def csvdata2():
#     # Return the template
#     return render_template('data/primary-energy-consumption-by-region.csv')

# @app.route('/csvdata3')
# def csvdata3():
#     # Return the template
#     return render_template('data/primary-energy-consumption-by-source.csv')

# @app.route('/csvdata4')
# def csvdata4():
#     # Return the template
#     return render_template('data/per-capita-energy-use.csv')

# @app.route('/csvdata5')
# def csvdata5():
#     # Return the template
#     return render_template('data/countries.json')

# @app.route('/map_data')
# def map_data():
#     # Return the template
#     return render_template('data/world-power-plants-list.geojson')

# @app.route('/map_raw')
# def map_raw():
#     # Return the template
#     return render_template('map_raw.html')

# @app.route('/map')
# def map():
#     # Return the template
#     return render_template('map.html')

# @app.route('/coal')
# def coal():
#     # Return the template with the teams list passed in
#     return render_template('coal.html', output_data=coal_tables)

# @app.route('/gas')
# def gas():
#     # Return the template with the teams list passed in
#     return render_template('gas.html', output_data=gas_tables)

# @app.route('/oil')
# def oil():
#     # Return the template with the teams list passed in
#     return render_template('oil.html', output_data=oil_tables)

# @app.route('/hydro')
# def hydro():
#     # Return the template with the teams list passed in
#     return render_template('hydro.html', output_data=hydro_tables)

# @app.route('/nuclear')
# def nuclear():
#     # Return the template with the teams list passed in
#     return render_template('nuclear.html', output_data=nuclear_tables)

# @app.route('/wind')
# def wind():
#     # Return the template with the teams list passed in
#     return render_template('wind.html', output_data=wind_tables)

# @app.route('/solar')
# def solar():
#     # Return the template with the teams list passed in
#     return render_template('solar.html', output_data=solar_tables)



if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
