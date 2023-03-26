from django.db import connection

from pandas import read_csv, DataFrame, concat
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import BaggingClassifier
from imblearn.over_sampling import RandomOverSampler

#*****************Read Data*****************

def get_prediction(file_url, input_data):
    
    data = read_csv(file_url)
    X = data.drop('HeartDisease', axis=1)  # input
    y = data['HeartDisease']   # output
    oversample = RandomOverSampler(sampling_strategy='minority')
    X_over, y_over = oversample.fit_resample(X, y)
    
    X_over = data_prep(X_over)
    
    model = BaggingClassifier(estimator=LogisticRegression(max_iter=10000), n_estimators=50, max_samples=0.8, max_features=0.8)
    # model = LogisticRegression(max_iter=10000)
    model.fit(X_over, y_over)
    input = prepare_input_data(input_data)
    # input = X_over.tail(1)
    prediction = model.predict(input)
    if 1 in prediction:
        return 1
    else:
        return 0

def prepare_input_data(input_data):
    input_data_prepared = {}
    if input_data['Sex'] == 'M':
        input_data_prepared['Sex_M'] = 1.0
        input_data_prepared['Sex_F'] = 0.0
    else:
        input_data_prepared['Sex_M'] = 0.0
        input_data_prepared['Sex_F'] = 1.0

    if input_data['ChestPainType'] == 'ASY':
        input_data_prepared['ChestPainType_ASY'] = 1.0
        input_data_prepared['ChestPainType_ATA'] = 0.0
        input_data_prepared['ChestPainType_NAP'] = 0.0
        input_data_prepared['ChestPainType_TA'] = 0.0
    elif input_data['ChestPainType'] == 'ATA':
        input_data_prepared['ChestPainType_ASY'] = 0.0
        input_data_prepared['ChestPainType_ATA'] = 1.0
        input_data_prepared['ChestPainType_NAP'] = 0.0
        input_data_prepared['ChestPainType_TA'] = 0.0
    elif input_data['ChestPainType'] == 'NAP':
        input_data_prepared['ChestPainType_ASY'] = 0.0
        input_data_prepared['ChestPainType_ATA'] = 0.0
        input_data_prepared['ChestPainType_NAP'] = 1.0
        input_data_prepared['ChestPainType_TA'] = 0.0
    else:
        input_data_prepared['ChestPainType_ASY'] = 0.0
        input_data_prepared['ChestPainType_ATA'] = 0.0
        input_data_prepared['ChestPainType_NAP'] = 0.0
        input_data_prepared['ChestPainType_TA'] = 1.0
        
    if input_data['RestingECG'] == 'LVH':
        input_data_prepared['RestingECG_LVH'] = 1.0
        input_data_prepared['RestingECG_Normal'] = 0.0
        input_data_prepared['RestingECG_ST'] = 0.0
    elif input_data['RestingECG'] == 'Normal':
        input_data_prepared['RestingECG_LVH'] = 0.0
        input_data_prepared['RestingECG_Normal'] = 1.0
        input_data_prepared['RestingECG_ST'] = 0.0
    else:
        input_data_prepared['RestingECG_LVH'] = 0.0
        input_data_prepared['RestingECG_Normal'] = 0.0
        input_data_prepared['RestingECG_ST'] = 1.0
        
    if input_data['ExerciseAngina'] == 'N':
        input_data_prepared['ExerciseAngina_N'] = 1.0
        input_data_prepared['ExerciseAngina_Y'] = 0.0
    else:
        input_data_prepared['ExerciseAngina_N'] = 0.0
        input_data_prepared['ExerciseAngina_Y'] = 1.0
        
    if input_data['ST_Slope'] == 'Down':
        input_data_prepared['ST_Slope_Down'] = 1.0
        input_data_prepared['ST_Slope_Flat'] = 0.0
        input_data_prepared['ST_Slope_Up'] = 0.0
    elif input_data['ST_Slope'] == 'Flat':
        input_data_prepared['ST_Slope_Down'] = 0.0
        input_data_prepared['ST_Slope_Flat'] = 1.0
        input_data_prepared['ST_Slope_Up'] = 0.0
    else:
        input_data_prepared['ST_Slope_Down'] = 0.0
        input_data_prepared['ST_Slope_Flat'] = 0.0
        input_data_prepared['ST_Slope_Up'] = 1.0
    
    input_data_prepared.update({'Age': input_data['Age']})
    input_data_prepared.update({'RestingBP': input_data['RestingBP']})
    input_data_prepared.update({'Cholesterol': input_data['Cholesterol']})
    input_data_prepared.update({'MaxHR': input_data['MaxHR']})
    input_data_prepared.update({'Oldpeak': input_data['Oldpeak']})
    input_data_prepared.update({'FastingBS': input_data['FastingBS']})
    
    input_data_0 = {}
    input_data_0[0] = input_data_prepared
    
    input_data_DF = DataFrame(input_data_0).transpose()
    X_binary = input_data_DF[['Sex_F', 'Sex_M', 'ChestPainType_ASY', 'ChestPainType_ATA', 'ChestPainType_NAP', 'ChestPainType_TA', 'RestingECG_LVH',
                       'RestingECG_Normal', 'RestingECG_ST', 'ExerciseAngina_N', 'ExerciseAngina_Y', 'ST_Slope_Down', 'ST_Slope_Flat', 'ST_Slope_Up', 'FastingBS']]
    
    X_scalable = input_data_DF[['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']]  # Orginal numeric columns
    
    X_scaled = MinMaxScaler().fit_transform(X_scalable)
    X_scaled_DF = DataFrame(X_scaled)
    X_scaled_DF.columns = X_scalable.columns

    X_PREP = concat([X_scaled_DF, X_binary], axis=1)  # Prepared Data
    # return X_PREP.loc[0]
    return X_PREP


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

    X_PREP = concat([X_scaled_DF, X_binary], axis=1)  # Prepared Data

    return X_PREP