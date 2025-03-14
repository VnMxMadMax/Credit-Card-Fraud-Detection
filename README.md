# **💳 Credit Card Fraud Detection using Machine Learning**

🚀 This project detects fraudulent transactions using **Machine Learning models**. It uses **EDA, feature engineering, class balancing (SMOTE), model comparison, and explainability techniques (SHAP & LIME)** to build an accurate fraud detection system.

---

## **📌 Project Overview**
Credit card fraud is a major financial issue. This project aims to:
✔ **Identify fraudulent transactions** using ML models.
✔ **Handle imbalanced data** using SMOTE.
✔ **Compare multiple models** (Logistic Regression, Random Forest, XGBoost, Stacking).
✔ **Interpret model decisions** using **SHAP & LIME**.
✔ **Future Addition:** Fraud alert system (Email/SMS notifications).

---

## **🛠 Tech Stack & Libraries Used**
✅ **Programming Language:** Python 🐍  
✅ **Libraries:** Pandas, NumPy, Scikit-learn, XGBoost, Matplotlib, Seaborn, SHAP, LIME

---

## **📂 Project Structure**
```bash
/credit-card-fraud-detection
│── fraud_detection.py    # Main ML script
│── model.pkl             # Trained ML model
│── requirements.txt      # Dependencies
│── README.md             # Project details
│── data/                 # Raw & processed dataset
│── notebooks/            # Jupyter notebooks for analysis
```

---

## **🔬 Exploratory Data Analysis (EDA)**
- **Data Cleaning & Preprocessing:** Handling missing values, duplicates, and feature scaling.
- **Imbalanced Data Handling:** Fraud cases are rare, so **SMOTE (Synthetic Minority Over-sampling Technique)** is applied.
- **Feature Selection:** Checking correlation and importance of variables.
- **Visualization:** Distribution plots, box plots, fraud percentage analysis.

---

## **🤖 Machine Learning Models**
| Model                 | ROC-AUC Score |
|----------------------|--------------|
| Logistic Regression | 0.95 |
| Random Forest       | 0.91 |
| XGBoost            | 0.94 |
| **Stacking (Best)** | **0.95+** |

📌 **Stacking (Logistic Regression + XGBoost) was the best-performing model.**

---

## **🔍 Explainability with SHAP & LIME**
- **SHAP**: Identifies important features influencing fraud prediction.
- **LIME**: Explains individual predictions, making the model more transparent.

```python
import shap
explainer = shap.TreeExplainer(best_xgb)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)
```

---

## **📢 Future Enhancements**
✅ **Fraud Alert System:** Email/SMS notifications for suspicious transactions.  
✅ **Real-time Streaming:** Using Apache Kafka for real-time fraud detection.  
✅ **Deploying the Model:** Hosting the model as an API (Flask/FastAPI/Streamlit).  

---

## **🚀 How to Run the Project**
1️⃣ **Clone the repository:**  
```bash
git clone https://github.com/your-username/credit-card-fraud-detection.git
cd credit-card-fraud-detection
```
2️⃣ **Install dependencies:**  
```bash
pip install -r requirements.txt
```
3️⃣ **Run the model script:**  
```bash
python fraud_detection.ipynb
```
4️⃣ **Check Results:** Predictions and explanations will be generated.

---

## **📜 License**
This project is open-source under the **MIT License**. Feel free to modify and improve! 🚀

---

## **👨‍💻 Author & Contact**
📌 **Hammadur Rahman**  
📌 **GitHub:** [VnMxMadMax](https://github.com/your-username)  
📌 **Email:** hammadurrahman171@gmail.com  

🚀 If you found this useful, give it a ⭐ on GitHub!  

