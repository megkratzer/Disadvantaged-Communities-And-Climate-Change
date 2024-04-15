#%%
#read in data and modules

import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

#read in trimmed data
df = pd.read_csv('../data/trimmed_data.csv')
df = df.set_index(['Census tract 2010 ID','County Name','State/Territory'])

#%%
#get data ready for pipeline

#check data for any nulls
len(df)
df.isna().sum()
#histric underinvestment is almost entirely null, so we will delete that col and impute all other missing values later
df = df.drop('Underinvestment',axis=1)

#create aggregated climate change column from all climate indicators (as defined in data source)
#this will be our predictor column in order to understand what other tract factors most influence climate change
df['climate_all'] = df['Agriculture_Loss'] + df['Building_Loss'] +  df['Population_Loss'] + df['Flood_Risk'] + df['Fire_Risk']
df = df.drop(['Agriculture_Loss','Building_Loss','Population_Loss','Flood_Risk','Fire_Risk'], axis=1)
#also drop disadvantaged since this is calculated using all other indicators 
df = df.drop('Disadvantaged',axis=1)

#delete any rows where the target variable (climate_all is NA)
df = df.dropna(subset=['climate_all'])

#save this new dataset for future modeling
df.to_csv('../data/modeling_data.csv')

#create X and y datasets
y = df['climate_all']
X = df.drop('climate_all', axis=1)

#training/testing split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

#separate numeric and categorical features (just Low_Income) for pipeline
numeric_features = X_train.drop('Low_Income',axis=1).columns
categorical_features = X_train[['Low_Income']].columns #has 0 missing values, no need for imputation in next step

#%%
#create pipeline

numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer(n_neighbors=10)),
    ('scaling', RobustScaler()) #scaling is not hugely important for random forest, but it is still good to include
])
categorical_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore', drop='first'))])

#combine preprocessers and specify columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

#create random forest pipeline
rf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=123, n_estimators=500))
])

#%%
#visualize variable importances

#fit model
rf_pipeline.fit(X_train, y_train)

#extract feature importances
feature_importances = rf_pipeline.named_steps['regressor'].feature_importances_

#get feature names
feature_names = []
preprocessor = rf_pipeline.named_steps['preprocessor']
for transformer_name, transformer, feature_names_subset in preprocessor.transformers_:
    if 'encoder' in transformer.named_steps:  # For categorical features
        transformed_names = transformer.named_steps['encoder'].get_feature_names_out(feature_names_subset)
        feature_names.extend(transformed_names)
    elif 'scaling' in transformer.named_steps: 
        feature_names.extend(feature_names_subset)

#sort feature importances and match feature names
indices = np.argsort(feature_importances)[::-1]
sorted_feature_importances = feature_importances[indices]
sorted_feature_names = [feature_names[i] for i in indices]

#plot the importances
plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(len(sorted_feature_importances)), sorted_feature_importances)
plt.xticks(range(len(sorted_feature_names)), sorted_feature_names, rotation=90)
plt.xlabel('Features')
plt.ylabel('Importance')
plt.tight_layout()
plt.savefig('../images/rf_feature_importances.png')

#%%
#calculate mse during cross validation and predict on test set
#the main goal with using random forest was to generate the feature importances, so how the model performed is not as relevent,
#but we will calculate it anyways

rf_scores = cross_val_score(rf_pipeline, X_train, y_train, cv=5, scoring='neg_mean_squared_error')

# The mean score is negative due to the convention 'higher is better',
# so we take the negative of the scores to get positive error values.
mse = -np.mean(rf_scores)
print(f"The average cross validation MSE is {mse}")

#predict on test set
y_pred = rf_pipeline.predict(X_test)
test_mse = mean_squared_error(y_test, y_pred)
print("Test Set MSE Score:", test_mse)

