# -*- coding: utf-8 -*-
"""DataAnalytics_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1i4RANvpjh6A69YqvTjssE0q5jtKVqA_1
"""

from google.colab import files
files.upload()

"""Data PreProcessing :
First Importing all the neccessary libraries and performing the exploratory data analysis (EDA)

EDA:
1.Null Values
2.Duplicated Values
3.Outliers
4.Label Encoding
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

hr=pd.read_csv('HR_Dataset.csv')

hr.info()

hr.shape

hr.head()

hr.isnull().sum()

hr.dropna(inplace=True)

hr.duplicated().sum()

hr.drop_duplicates(inplace=True)

cols=hr.columns

cols

for col in hr.columns:
  if hr[col].dtype !='object':
    plt.boxplot(hr[col])
    plt.xlabel(hr[col])
    plt.show()

def remove_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_filtered = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    return df_filtered, outliers

outliers_all = pd.DataFrame()
for col in outliers_all:
    hr, outliers = remove_outliers(hr, col)
    outliers_all = pd.concat([outliers_all, outliers], axis=0)

print("List of outliers:")
print(outliers_all)

print("\nDataFrame after removing outliers:")
hr

from sklearn.preprocessing import LabelEncoder

for col in hr.columns:
    if hr[col].dtype == 'object':
        le = LabelEncoder()
        hr[col] = le.fit_transform(hr[col])

hr.info()

hr.head()

"""Model Training"""

x=hr.drop(['Attrition'],axis=1)
y=hr['Attrition']

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=50)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

model=RandomForestClassifier()
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
accuracy=accuracy_score(y_pred,y_test)
print(accuracy*100)

from sklearn.model_selection import GridSearchCV

base_model=RandomForestClassifier()
param_grid={
    'n_estimators': [100,200,300],
    'max_depth': [10,20,30],
    'min_samples_split':[2,5,10],
    'min_samples_leaf':[1,2,4],
    'criterion':['entrophy','gini']
}
grid_search=GridSearchCV(estimator=base_model,param_grid=param_grid,cv=5)
grid_search.fit(x_train,y_train)

print(grid_search.best_params_)

class_model=RandomForestClassifier(n_estimators=100,max_depth=10,min_samples_split=2,min_samples_leaf=1,criterion='gini')
class_model.fit(x_train,y_train)
y_pred=class_model.predict(x_test)
acc=accuracy_score(y_pred,y_test)
print(acc*100)

"""## Regression Model"""

hr

from google.colab import files
files.upload()

nd=pd.read_csv('HR_Dataset_2.csv')

nd

nd.isnull().sum()

nd.duplicated().sum()

# Generate Outliers list and remove outliers

import pandas as pd
import numpy as np
def remove_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_filtered = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    return df_filtered, outliers

# Initialize an empty DataFrame to store all outliers
outliers_all = pd.DataFrame()

# Iterate through numerical columns to find and remove outliers
for col in nd.select_dtypes(include=np.number).columns:
    nd, outliers = remove_outliers(hr, col)
    outliers_all = pd.concat([outliers_all, outliers], axis=0)

print("List of outliers:")
print(outliers_all)

print("\nDataFrame after removing outliers:")

nd

nd

# Perform label encoding on nd

for col in nd.columns:
    if nd[col].dtype == 'object':
        le = LabelEncoder()
        nd[col] = le.fit_transform(nd[col])
nd.info()
nd.head()

# Perfrom random forest regressor on nd and target column is performance rating

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Assuming 'PerformanceRating' is your target variable
X = nd.drop('PerformanceRating', axis=1)
y = nd['PerformanceRating']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the RandomForestRegressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)  # You can adjust hyperparameters
rf_regressor.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_regressor.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# prompt: save both regression and classifier model using pickle

import pickle

# Save the classifier model
with open('classifier_model.pkl', 'wb') as file:
    pickle.dump(class_model, file)

# Save the regression model
with open('regression_model.pkl', 'wb') as file:
    pickle.dump(rf_regressor, file)

"""# WEB APP INTERFACE"""

# Commented out IPython magic to ensure Python compatibility.

import streamlit as st
import pickle
import pandas as pd
# 
# # Load models
clf = pickle.load(open("classifier_model.pkl", "rb"))
reg = pickle.load(open("regression_model.pkl", "rb"))
# 
st.set_page_config(page_title="HR Analytics Tool", layout="centered")
st.title("📊 HR Analytics Dashboard")
# 
tabs = st.tabs(["👥 Attrition Prediction", "📈 Performance Analysis"])
# 
# # --- Mappings ---
bt_map = {'Non-Travel': 0, 'Travel_Rarely': 1, 'Travel_Frequently': 2}
dept_map = {'Sales': 0, 'Research & Development': 1, 'Human Resources': 2}
edu_field_map = {'Life Sciences': 0, 'Medical': 1, 'Marketing': 2, 'Technical Degree': 3, 'Human Resources': 4, 'Other': 5}
job_role_map = {
     'Sales Executive': 0, 'Research Scientist': 1, 'Laboratory Technician': 2,
     'Manufacturing Director': 3, 'Healthcare Representative': 4, 'Manager': 5,
     'Sales Representative': 6, 'Research Director': 7, 'Human Resources': 8
 }
marital_map = {'Single': 0, 'Married': 1, 'Divorced': 2}
gender_map = {'Male': 1, 'Female': 0}
overtime_map = {'Yes': 1, 'No': 0}
over18_map = {'Y': 1}
attrition_map = {'Yes': 1, 'No': 0}
# 
# # --- Reusable Inputs ---
def get_common_inputs():
     return {
         "age": st.slider("Age", 18, 60, 30),
         "gender": st.selectbox("Gender", ['Male', 'Female']),
         "business_travel": st.selectbox("Business Travel", list(bt_map.keys())),
         "department": st.selectbox("Department", list(dept_map.keys())),
         "education": st.selectbox("Education Level", [1, 2, 3, 4, 5]),
         "education_field": st.selectbox("Education Field", list(edu_field_map.keys())),
         "job_role": st.selectbox("Job Role", list(job_role_map.keys())),
         "marital_status": st.selectbox("Marital Status", list(marital_map.keys())),
         "over_time": st.selectbox("OverTime", list(overtime_map.keys())),
         "over_18": st.selectbox("Over 18", ['Y']),
         "daily_rate": st.slider("Daily Rate", 100, 1500, 800),
         "distance_from_home": st.slider("Distance From Home", 1, 50, 10),
         "hourly_rate": st.slider("Hourly Rate", 30, 100, 60),
         "job_involvement": st.slider("Job Involvement", 1, 4, 3),
         "job_level": st.slider("Job Level", 1, 5, 2),
         "job_satisfaction": st.slider("Job Satisfaction", 1, 4, 3),
         "environment_satisfaction": st.slider("Environment Satisfaction", 1, 4, 3),
         "relationship_satisfaction": st.slider("Relationship Satisfaction", 1, 4, 3),
         "work_life_balance": st.slider("Work Life Balance", 1, 4, 3),
         "percent_salary_hike": st.slider("Percent Salary Hike", 10, 25, 15),
         "stock_option_level": st.slider("Stock Option Level", 0, 3, 1),
         "training_times": st.slider("Training Times Last Year", 0, 6, 2),
         "total_working_years": st.slider("Total Working Years", 0, 40, 10),
         "num_companies_worked": st.slider("Number of Companies Worked", 0, 10, 2),
         "years_at_company": st.slider("Years at Company", 0, 40, 5),
         "years_in_current_role": st.slider("Years in Current Role", 0, 20, 5),
         "years_since_last_promotion": st.slider("Years Since Last Promotion", 0, 15, 3),
         "years_with_curr_manager": st.slider("Years with Current Manager", 0, 20, 4),
         "monthly_income": st.slider("Monthly Income", 1000, 20000, 5000),
         "monthly_rate": st.slider("Monthly Rate", 1000, 25000, 10000)
     }
# 
# # --- Tab 1: Classifier ---
with tabs[0]:
     st.subheader("👥 Predict Employee Attrition")
# 
     with st.form("attrition_form"):
         data = get_common_inputs()
         performance_rating = st.selectbox("Performance Rating", [1, 2, 3, 4])
         submitted1 = st.form_submit_button("Predict Attrition")
 
     if submitted1:
         row = [
             data["age"], bt_map[data["business_travel"]], data["daily_rate"], dept_map[data["department"]],
             data["distance_from_home"], data["education"], edu_field_map[data["education_field"]], 1, 999999,
             data["environment_satisfaction"], gender_map[data["gender"]], data["hourly_rate"], data["job_involvement"],
             data["job_level"], job_role_map[data["job_role"]], data["job_satisfaction"], marital_map[data["marital_status"]],
             data["monthly_income"], data["monthly_rate"], data["num_companies_worked"], over18_map[data["over_18"]],
             overtime_map[data["over_time"]], data["percent_salary_hike"], performance_rating,
             data["relationship_satisfaction"], 8, data["stock_option_level"], data["total_working_years"],
             data["training_times"], data["work_life_balance"], data["years_at_company"],
             data["years_in_current_role"], data["years_since_last_promotion"], data["years_with_curr_manager"]
         ]
 
         clf_columns = clf.feature_names_in_
         input_df = pd.DataFrame([row], columns=clf_columns)
 
         prediction = clf.predict(input_df)[0]
         st.success(f"Attrition Prediction: **{'Yes' if prediction == 1 else 'No'}**")
 
 # --- Tab 2: Regressor ---
with tabs[1]:
     st.subheader("📈 Analyze Predicted Performance")
 
     with st.form("regression_form"):
         data = get_common_inputs()
         attrition_input = st.selectbox("Has the employee left?", ["No", "Yes"])
         submitted2 = st.form_submit_button("Predict Performance")
 
     if submitted2:
         row = [
             data["age"], attrition_map[attrition_input], bt_map[data["business_travel"]],
             data["daily_rate"], dept_map[data["department"]], data["distance_from_home"], data["education"],
             edu_field_map[data["education_field"]], 1, 999999, data["environment_satisfaction"],
             gender_map[data["gender"]], data["hourly_rate"], data["job_involvement"], data["job_level"],
             job_role_map[data["job_role"]], data["job_satisfaction"], marital_map[data["marital_status"]],
             data["monthly_income"], data["monthly_rate"], data["num_companies_worked"], over18_map[data["over_18"]],
             overtime_map[data["over_time"]], data["percent_salary_hike"], data["relationship_satisfaction"], 8,
             data["stock_option_level"], data["total_working_years"], data["training_times"], data["work_life_balance"],
             data["years_at_company"], data["years_in_current_role"], data["years_since_last_promotion"],
             data["years_with_curr_manager"]
         ]
 
         reg_columns = reg.feature_names_in_
         input_df = pd.DataFrame([row], columns=reg_columns)
 
         prediction = reg.predict(input_df)[0]
         st.info(f"Predicted Performance Score: **{prediction:.2f}**")


hr.columns

#!npm install localtunnel

#!streamlit run app.py &>/content/logs.txt & npx localtunnel --port 8501 & curl ipv4.icanhazip.com

#from pyngrok import ngrok
#ngrok.set_auth_token("2v5IArlnsiADJTXKU1Qs7kA5oJ0_3CzEvuzTFE7wvNKu1919J")  # Replace with your actual ngrok auth token
#public_url = ngrok.connect(addr="8501", proto="http")
#print("Streamlit App URL:", public_url)

#!streamlit run app.py &>/dev/null &

import pickle

# Load models
clf = pickle.load(open("classifier_model.pkl", "rb"))
reg = pickle.load(open("regression_model.pkl", "rb"))

print("Classifier expects:")
print(clf.feature_names_in_)

print("\nRegressor expects:")
print(reg.feature_names_in_)
