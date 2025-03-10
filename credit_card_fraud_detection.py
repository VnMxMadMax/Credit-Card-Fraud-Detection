# -*- coding: utf-8 -*-
"""Credit Card Fraud Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_Ro84vDAwB_ZvCdGNgaxPqLCkgfmvSeU

# <h1><center><u><font color='yellow'>Credit Card Fraud Detection<font></u></center></h1>

This script implements various machine learning models (Logistic Regression Random Forest, XGBoost) to detect fraudlent transaction in a highly imbalanced dataset.
It includes data preprocessing, class imbalance handling using SMOTE, hyperparameter tuning, and model eveluation using key performance metrics.

**Importing Libraries**
"""

! pip install xgboost
! pip install imblearn

# import necessary files
import numpy as np                # For Numerical Operation and array Handling
import pandas as pd               # For Data manipulation and analysis
import matplotlib.pyplot as plt   # For Static plotting
import seaborn as sns             # For Statistical graphics
import plotly.express as px       # For Interactive plotting and visualizations
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

"""# **Reading the Data**"""

# Load the Dataset
df = pd.read_csv('/content/drive/MyDrive/Data for projects/creditcard.csv')

print(df.head()) # Display First few rows

df.shape # Shows Dimensions of dataset

df.info() # Column data types and missing values

"""**Data Description**"""

# Check for missing values
print(df.isnull().sum())

# Check Class distribution (Fraud vs Non-Fraud)
df['Class'].value_counts()

df["Class"].value_counts(normalize=True) * 100  # Show percentages

"""# **Performing EDA(Exploratory data analysis)**"""

# Outlier Detection in 'Amount' features
import numpy as np
Q1 = df["Amount"].quantile(0.25)
Q3 = df["Amount"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
print(f"Outliers: {df[(df['Amount'] < lower_bound) | (df['Amount'] > upper_bound)].shape[0]}")

# Calculate class counts and percentages
class_counts = df['Class'].value_counts()
total = class_counts.sum()
percentages = (class_counts / total) * 100

# Create a DataFrame for better visualization
class_df = pd.DataFrame({'Class': class_counts.index, 'Count': class_counts.values, 'Percentage': percentages.values})

# Create interactive bar chart using Plotly
fig = px.bar(class_df, x='Class', y='Count', text=class_df['Percentage'].apply(lambda x: f"{x:.2f}%"),
             color='Class', color_continuous_scale=px.colors.sequential.Viridis,
             labels={'Class': 'Transaction Type', 'Count': 'Number of Transactions', 'text': 'Percentage'},
             title="Class Distribution (Fraud vs. Non-Fraud)")

# Customize layout
fig.update_traces(textposition='outside', marker=dict(line=dict(color='black', width=2)))
fig.update_layout(xaxis=dict(showgrid=False, linecolor='black', linewidth=2, tickmode='array', tickvals=[0, 1], ticktext=['Non-Fraud', 'Fraud']),
                  yaxis=dict(showgrid=False, linecolor='black', linewidth=2),
                  yaxis_title='Count', xaxis_title='Class',
                  template="plotly_white",  # Light backgroud
                  font=dict(family="Arial", size=16, color="black"),
                  margin=dict(l=70, r=50, b=150, t=100, pad=4),  # Adjust margins
                  width=700,  # Increase plot width
                  height=700,   # Increase plot height
                  )
# Show plot
fig.show()

# Print counts and percentages
print(class_df)

"""99.8% of the transactions are non-fraudulent, while only 0.17% are fraudulent. This indicates that the dataset is highly imbalanced."""

df.describe() #Summary statistics of the dataset to understand distribution and detect anomalies

# Create interactive histograms
fig1 = px.histogram(df, x="Amount", nbins=50, title="Transaction Amount Distribution",
                    labels={'Amount': 'Transaction Amount'}, template='plotly_white')
fig1.update_traces(marker_line_width=1, marker_line_color='black')
fig1.show()

fig2 = px.histogram(df, x="Time", nbins=50, title="Transaction Time Distribution",
                    labels={'Time': 'Transaction Time'}, template='plotly_white')
fig2.update_traces(marker_line_width=1, marker_line_color='black')
fig2.show()

corr = df.corr()

# Print correlations with 'Class', sorted in descending order
print("\nCorrelations with Class:\n", corr['Class'].sort_values(ascending=False))

# Create the correlation heatmap
plt.figure(figsize=(20, 20))  # Set figure size
sns.heatmap(
    corr,
    cmap='coolwarm',       # Color scheme (red-blue gradient)
    annot=True,            # Show correlation values in cells
    fmt='.3f',            # Format numbers to 2 decimal places
    vmin=-1, vmax=1,      # Set color scale range (-1 to 1)
    center=0,             # Center the colormap at 0
    square=True,          # Make the plot square-shaped
    linewidths=0.5,       # Add grid lines between cells
    cbar_kws={'shrink': .5}  # Customize color bar size
)

# Add title and adjust layout
plt.title("Correlation Matrix Heatmap", fontsize=16, pad=15)
plt.tight_layout()

# Display the plot
plt.show()

# Highly Correlated Features with Fraud
high_corr_features = corr[abs(corr["Class"]) > 0.2]["Class"].index
sns.heatmap(df[high_corr_features].corr(), cmap="coolwarm", annot=True, linewidths=0.5)
plt.title("Highly Correlated Features with Fraud")
plt.show()

"""# **Data Preprocessing & Class Imbalance Handling**"""

# Drop 'Time' column (not useful for fraud detection)
df = df.drop('Time', axis=1)

df.head()

"""Feature Scaling (Standardization)

* The Amount feature is highly skewed and needs to be standardized to improve model performance.
"""

#Standardize 'Amount' feature
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df["Amount"] = scaler.fit_transform(df["Amount"].values.reshape(-1, 1))

"""# Splitting Data(Train/test Split)
* 80% of the data is used for training, and 20% for testing
"""

from sklearn.model_selection import train_test_split

X = df.drop('Class', axis=1) # Features
y = df['Class'] # Target Variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

print("Train Fraud Cases", sum(y_train == 1))
print("Test Fraud Cases", sum(y_test ==1))

"""**Handling Class Imbalance using SMOTE**

* Since fraud cases make up only  0.17% of the data, we use SOMTE (Synthetic Minority Over-sampling Technique) to balance the dataset and improve model learning
"""

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("Train Fraud Cases", sum(y_train_resampled == 1))
print("Test Fraud Cases", sum(y_test ==1))

"""# Training Machine Learning Model

* We Start with a simple model like Logistic Regression as a baseline and then experiment with more advanced models to improve performance.
"""

# Standardize features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

# Train the Logistic Regression model
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train_scaled, y_train_resampled)

# Evaluate the model
from sklearn.metrics import accuracy_score  # Import accuracy_score

y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:{:.2f}%".format(accuracy * 100))

# evaluate the model
from sklearn.metrics import confusion_matrix, classification_report

print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

from sklearn.metrics import roc_auc_score

roc_auc = roc_auc_score(y_test, y_pred)
print(f"ROC AUC Score: {roc_auc:.2f}")

"""**Conclusion**
The model achieves a high overall accuracy of 97%, but this is misleading due to the class imbalance

* The confusion matrix shows that while the model correctly identifies most non-fraud transactions (55,353 out of 56,864), it misclassifies 1,522 non-fraud transaction as fraud, which could lead to false alarms.
* The model performs poorly in detecting fraud transactions with a low precision (0.06) but high recall (0.92). This means that while most actual fraud cases are detected, there are many false positives.
* The F1-score for fraud detection (0.11) is very low, indicating an imbalance between precision and recall
* A high <u>ROC AUC score</u> of 0.95 indicates that the Logistic Regression model performs well in distinguish between fraud and non-fraud transactions.

**Key Takeaways**
* The high recall for fraud cases suggests that the model is effective in identifying fraud transactions but at the cost of many false positives.
* The very low precision indicates that a large number of flagged fraud cases are actually non-fraudulent.

While Logistic Regression works well, further tuning or exploring more complex models may enhance precision and overall performance.

--------------------------------------------------------------------------------

**Using a More Powerful Model: Random Forest**
"""

from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_resampled, y_train_resampled)

y_pred_rf = rf_model.predict(X_test_scaled)

print(classification_report(y_test, y_pred_rf))

roc_auc = roc_auc_score(y_test, y_pred_rf)
print(f"ROC AUC Score: {roc_auc:.2f}")

"""**Conclusion**
The Random Forest model achieves near-prefect accuracy, but its performance in detecting fraud is concerning.

* Non-fraud transactions (Class 0) are detected almost perfectly, with 100% precision and recall.
* Fraud transactions (Class 1) have high precision (1.00) but very low recall (0.10), meaning that the model correctly classifies fraud when it predicts fraud, but it misses 90% of actual fraud cases.
* The F1-score for fraud detection is only 0.19, indicating poor overall effectiveness in identifying fraud
* The ROC AUC score of 0.55 indicates that the Random Forest model is performing poorly in distinguish between fraud and non-fraud transactions. A score clost to 0.50 suggests that the model is only slightly better than random guessing.

**Key Takeways**
* The model is heavily biased towards the majority class, likely due to the severe class imbalance*
* The low recall suggests that the model rearely predicts fraud, making it effective for real-world fraud detection.

--------------------------------------------------------------------------------

**Using Advance Model Like XGboost**


To improve fraud detection, we now use XGBoost (Extreme Gradient Boosting), a powerful ensemble learning algorithm known for:

* Handling imbalanced data effectively with built-in class weighting.
* Capturing non-linear relationships better than traditional models.
* Being highly efficient and scalable for large datasets.
"""

!pip install xgboost  # Install the xgboost library

from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score

fraud_ratio = sum(y_train_resampled == 0) / sum(y_train_resampled == 1)  # Compute proper weight

# Initialize XGBoost Classifier
xgb_model = XGBClassifier(
    n_estimators=100,       # Number of trees
    learning_rate=0.1,      # Controls how much the model learns per iteration
    max_depth=5,            # Limits tree depth (prevents overfitting)
    subsample=0.8,          # Uses 80% of data per tree (reduces overfitting)
    colsample_bytree=0.8,   # Uses 80% of features per tree (prevents dominance of any one feature)
    random_state=42,        # Ensures reproducibility
    scale_pos_weight=fraud_ratio     # Increases focus on fraud cases
)

# Train the model on SMOTE-balanced data
xgb_model.fit(X_train_resampled, y_train_resampled)

# Make predictions
y_pred_xgb = xgb_model.predict(X_test_scaled)

# Classification Report
print("Classification Report:\n", classification_report(y_test, y_pred_xgb))

# Compute AUC-ROC Score
roc_auc = roc_auc_score(y_test, y_pred_xgb)
print(f"ROC AUC Score: {roc_auc:.2f}")

"""**Conclusion**
The XGBoost model shows some improvement in detecting fraud but still struggles with recall.

* Non-fraudulent transactions (Class 0) are detected almost perfectly, with 1.00 precision and recall.
* Fraudulent transactions (Class 1) now have a much higher precision (0.76) compared to previous models, meaning fewer false positives.
* However, recall is still low (0.16), meaning the model correctly identifies only 16% of actual fraud cases.
* The F1-score for fraud (0.27) suggests the model is not effectively balancing precision and recall.
* The ROC AUC score (0.58) is slightly better than random guessing but still very low, indicating that the model struggles to separate fraudulent and non-fraudulent transactions.

**Key Takeaways**
* Precision has improved, meaning the model makes fewer false fraud predictions.
* Recall is still too low, meaning it misses many actual fraud cases.

----------------------------------------------------------------------------------------------------------------------------------------------------------------

**<U>Random Forest & XGBoost with Hyperparameter Tuning</u>**
"""

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import RandomizedSearchCV

# 🚀 **Fix: Use Unscaled Data for Tree-Based Models**
X_train_rf_xgb, X_test_rf_xgb = X_train_resampled, X_test  # Keep unscaled

# ✅ **Fix: Adjust scale_pos_weight for XGBoost**
fraud_ratio = sum(y_train_resampled == 0) / sum(y_train_resampled == 1)  # Compute proper weight

# **🔥 Random Forest with RandomizedSearchCV**
rf_param_dist = {
    'n_estimators': [100, 200],    # Number of trees
    'max_depth': [None, 10, 20],   # Tree depth
    'min_samples_split': [2, 5]    # Minimum samples needted to split a node
}
rf_random = RandomizedSearchCV(RandomForestClassifier(random_state=42), rf_param_dist, scoring='roc_auc', cv=3, n_iter=5, n_jobs=-1)
rf_random.fit(X_train_rf_xgb, y_train_resampled)

best_rf = rf_random.best_estimator_
y_pred_rf = best_rf.predict(X_test_rf_xgb)

print("Best RF Parameters:", rf_random.best_params_)
print("Random Forest Classification Report:\n", classification_report(y_test, y_pred_rf))
print(f"Random Forest ROC AUC Score: {roc_auc_score(y_test, y_pred_rf):.2f}")

# **🔥 XGBoost with RandomizedSearchCV**
xgb_param_dist = {
    'n_estimators': [100, 200],         # No. of boosting rounds
    'max_depth': [3, 5],                # Maximum depth of trees
    'learning_rate': [0.05, 0.1],       # Smaller values slow learning but improve generalization
    'subsample': [0.7, 0.8, 0.9],       # Fraction of training data used per tree (Helps prevent overfitting)
    'colsample_bytree': [0.7, 0.8, 0.9] # Fraction of features used per tree (Ensures diversity in trees)
}
xgb_random = RandomizedSearchCV(XGBClassifier(scale_pos_weight=fraud_ratio, random_state=42), xgb_param_dist, scoring='roc_auc', cv=3, n_iter=5, n_jobs=-1)
xgb_random.fit(X_train_rf_xgb, y_train_resampled)

best_xgb = xgb_random.best_estimator_
y_pred_xgb = best_xgb.predict(X_test_rf_xgb)

print("Best XGBoost Parameters:", xgb_random.best_params_)
print("XGBoost Classification Report:\n", classification_report(y_test, y_pred_xgb))
print(f"XGBoost ROC AUC Score: {roc_auc_score(y_test, y_pred_xgb):.2f}")

"""**Conclusion**

🔹 Random Forest Performance
* Achieves high recall (0.83) and precision (0.87) for fraud detection.
* ROC AUC Score: 0.91, meaning it distinguishes fraud and non-fraud well.
* Key Strength: Well-balanced precision and recall, making it a strong model for fraud detection.

🔹 XGBoost Performance
* Higher recall (0.89) than Random Forest, meaning it detects more fraud cases.
* Lower precision (0.43) indicates some false positives, but still an improvement.
* ROC AUC Score: 0.94, showing superior fraud detection ability.
* Key Strength: Higher recall, making it a better option if detecting fraud is a top priority.

**Key Takeaways**
* XGBoost outperforms Random Forest in recall (0.89 vs. 0.83), making it better for fraud detection.
* Random Forest has better precision (0.87 vs. 0.43), meaning fewer false alarms.
* Final choice depends on business needs:
    * If minimizing false fraud alerts → Random Forest is better.
    * If catching more fraud cases is crucial → XGBoost is preferred.
* Fine-tuning XGBoost further (adjusting class weights, threshold tuning) may help improve precision.

-----------------------------------------------------------

# **Using Ensemble Learning: Stacking Logistic Regression & XGBoost**
By combining XGBoost (which excels at detecting fraud patterns) with Logistic Regression (which provides interpretability), we aim to build a stronger fraud detection model.
* XGBoost: Handles complex fraud patterns well and has high recall.
* Logistic Regression: Provides transparency in decision-making and generalizes well.
* Stacking these models helps leverage the strengths of both for better fraud detection.
"""

pip install mlxtend # Needed for StackingClassifier)

from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

# Define Base Learners
xgb_model = XGBClassifier(
    scale_pos_weight=fraud_ratio, n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42
)

# Meta-learner (Final Model)
meta_learner = LogisticRegression()

# Stacking Classifier
stacked_model = StackingClassifier(
    estimators=[('xgb', xgb_model)],  # Base learners
    final_estimator=meta_learner,  # Meta-learner
    passthrough=True  # Pass original features to final estimator
)

# Train Stacked Model on SMOTE-balanced Data
stacked_model.fit(X_train_resampled, y_train_resampled)

# Make Predictions
y_pred_stack = stacked_model.predict(X_test)

# Print Classification Report
print("\n🔹 Stacking Model (XGBoost + LR) Classification Report:\n", classification_report(y_test, y_pred_stack))

# Compute AUC-ROC Score
stack_roc_auc = roc_auc_score(y_test, y_pred_stack)
print(f"🔹 Stacking Model ROC AUC Score: {stack_roc_auc:.2f}")

"""**Conclusion**
* Precision (0.57) & Recall (0.88) for Fraud Cases
    * Higher recall than Random Forest(0.83), detects more fraud cases
    * Better precision than XGBoost alone(0.43), fewerr false positives.
* Macro Average F1-Score 0.85, shows a strong balance between fraud detection and accuracy
* ROC AUC Score likely improved compared to individual models.

**Key Takeaways**
* Stacking Logistic Regression & XGBoost significantly improves fraud detection.
* Higher recall than random Forest & better precision than standalone XGBoost
* Logistic Regression enhances interpretability while XGBoost boosts recall.
* A well-balanced model for fraud detection with fewer false alarms and better fraud detection rate

This stacked model is currently the best-performing model and can be used for real-world fraud detection deployment.

---------------------------------------------------------------------

# **Saving the Model**
"""

import pickle

# Save the trained models as a pickle string
saved_model = pickle.dumps(stacked_model)

# Load the saved model
loaded_model = pickle.loads(saved_model)

from joblib import parallel, delayed
import joblib

# Save the model as a pickle in a file
joblib.dump(stacked_model, 'fraud_detection_model.pkl')

# Load the model from the file
loaded_model = joblib.load('fraud_detection_model.pkl')

