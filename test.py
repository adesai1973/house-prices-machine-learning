# Import Dependencies
import os
import pandas as pd
import tensorflow as tf
#os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from tensorflow import keras
print("imports")

def run_model(bath, bed, sqft, zip):
    
    # Import necessary files
    census_df = pd.read_csv("../Resources/acs5_2018.csv")
    model = tf.keras.models.load_model("housing_model.h5")
    model = tf.keras.models.load_model("housing_model.h5")
    mean = pd.read_csv("mean_norm.csv")
    std = pd.read_csv("std_norm.csv")

    input_df =pd.DataFrame({"bathroom_ct": [bath],
                       "bedroom_ct": [bed],
                       "home_sqft": [sqft],
                       "zipcode": [zip]})
    merged_df = input_df.merge(census_df, how="inner")
    merged_df.drop("zipcode", axis=1, inplace=True)

    norm_df = (merged_df - mean) / std
    output = model.predict(norm_df)[0][0]
    return(output)

run_model(2,3,1666,85003)