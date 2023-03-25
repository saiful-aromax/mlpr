from django.db import connection

from pandas import read_csv, DataFrame, concat
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import BaggingClassifier
from imblearn.over_sampling import RandomOverSampler
from collections import Counter


#*****************Read Data*****************

def get_prediction(file_url):
    
    data = read_csv(file_url)
    X = data.drop('HeartDisease', axis=1)  # input
    y = data['HeartDisease']   # output
    oversample = RandomOverSampler(sampling_strategy='minority')
    X_over, y_over = oversample.fit_resample(X, y)
    
    X_over = data_prep(X_over)
    
    # model = BaggingClassifier(estimator=LogisticRegression(max_iter=10000), n_estimators=50, max_samples=0.8, max_features=0.8)
    model = LogisticRegression(max_iter=10000)
    model.fit(X_over, y_over)
    
    input = X_over.tail(1)
    prediction = model.predict(input)
    return prediction


#*****************Data Preprocessing*****************

def data_prep(X_over):
    OHE = OneHotEncoder(handle_unknown='ignore')

    data_sex_OHE = OHE.fit_transform(X_over[['Sex']])
    data_sex_DF = DataFrame(data_sex_OHE.toarray())
    data_sex_DF.columns = OHE.get_feature_names_out()

    data_ChestPainType_OHE = OHE.fit_transform(X_over[['ChestPainType']])
    data_ChestPainType_DF = DataFrame(data_ChestPainType_OHE.toarray())
    data_ChestPainType_DF.columns = OHE.get_feature_names_out()

    data_RestingECG_OHE = OHE.fit_transform(X_over[['RestingECG']])
    data_RestingECG_DF = DataFrame(data_RestingECG_OHE.toarray())
    data_RestingECG_DF.columns = OHE.get_feature_names_out()

    data_ExerciseAngina_OHE = OHE.fit_transform(X_over[['ExerciseAngina']])
    data_ExerciseAngina_DF = DataFrame(data_ExerciseAngina_OHE.toarray())
    data_ExerciseAngina_DF.columns = OHE.get_feature_names_out()

    data_ST_Slope_OHE = OHE.fit_transform(X_over[['ST_Slope']])
    data_ST_Slope_DF = DataFrame(data_ST_Slope_OHE.toarray())
    data_ST_Slope_DF.columns = OHE.get_feature_names_out()

    #***********************Merging multiple DataFrames***********************

    X_binary = concat([data_sex_DF, data_ChestPainType_DF, data_RestingECG_DF, data_ExerciseAngina_DF, data_ST_Slope_DF, X_over[['FastingBS']]], axis=1)
    X_scalable = X_over[['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']]  # Orginal numeric columns

    #***********************Applying MinMaxScaler***********************

    X_scaled = MinMaxScaler().fit_transform(X_scalable)
    X_scaled_DF = DataFrame(X_scaled)
    X_scaled_DF.columns = X_scalable.columns

    X_PREP = concat([X_scalable, X_binary], axis=1)  # Prepared Data

    return X_PREP