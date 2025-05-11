import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# ----------------------------
# Generate Balanced Synthetic Dataset
# ----------------------------
def generate_data():
    np.random.seed(42)
    size = 300
    income_npr = np.random.normal(5000000, 3000000, size).clip(100000, 10000000)
    employment = np.random.choice([0, 1, 2, 3], size=size, p=[0.55, 0.15, 0.2, 0.1])
    education = np.random.choice([0, 1, 2, 3, 4], size=size, p=[0.1, 0.3, 0.4, 0.15, 0.05])
    housing = np.random.randint(3, 11, size)
    isolation = np.random.randint(1, 11, size)
    healthcare = np.random.randint(3, 11, size)
    community = np.random.randint(3, 11, size)
    activity = np.random.randint(0, 8, size)

    risk_score = (
        0.0000025 * (2000000 - income_npr) +
        0.25 * (10 - housing) +
        0.45 * isolation +
        0.2 * employment +
        0.1 * (4 - education) +
        0.2 * (10 - healthcare) +
        0.25 * (10 - community) +
        0.15 * (7 - activity) +
        np.random.normal(0, 0.6, size)
    )

    risk_score = np.clip(risk_score, 0, 10)

    return pd.DataFrame({
        "Income_NPR": income_npr,
        "Employment": employment,
        "Education": education,
        "Housing": housing,
        "Isolation": isolation,
        "Healthcare": healthcare,
        "Community": community,
        "Physical_Activity": activity,
        "Risk": risk_score
    })

# ----------------------------
# Train Model
# ----------------------------
df = generate_data()
features = ["Income_NPR", "Employment", "Education", "Housing", "Isolation",
            "Healthcare", "Community", "Physical_Activity"]
X = df[features]
y = df["Risk"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LinearRegression()
model.fit(X_scaled, y)

# ----------------------------
# Risk Equation LaTeX
# ----------------------------
equation_parts = [f"{coef:.4f} \\times {name}" for coef, name in zip(model.coef_, features)]
equation_lines = [" + ".join(equation_parts[i:i+3]) for i in range(0, len(equation_parts), 3)]
equation_string = r"\text{Risk Score} = " + r" \\ \text{ + } ".join(equation_lines)

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("🧠 Mental Health Risk Predictor (Nepal – SDOH Based)")
st.markdown("""
This tool estimates your mental health risk score using synthetic but contextually grounded socioeconomic and lifestyle data tailored for Nepal.  
While the model is not real in the clinical or diagnostic sense, it draws from patterns that closely reflect likely trends based on available information.

**Note:** This tool uses a simplified **0–10 risk score** scale. Higher scores indicate greater potential mental health risk.
""")

# ----------------------------
# Sidebar: User Input
# ----------------------------
st.sidebar.header("Input Your Socioeconomic Profile")
income_npr = st.sidebar.slider("Annual Income (NPR)", 100000, 10000000, 1200000, step=100000)
employment = st.sidebar.selectbox("Employment Status", ["Employed", "Unemployed", "Student", "Retired"])
education = st.sidebar.selectbox("Highest Education Level",
                                  ["No formal education", "High School", "Bachelor's", "Master's", "Doctorate"])
housing = st.sidebar.slider("Housing Quality (1 = Poor, 10 = Excellent)", 1, 10, 6)
isolation = st.sidebar.slider("Social Isolation (1 = Low, 10 = High)", 1, 10, 4)
healthcare = st.sidebar.slider("Access to Healthcare (1 = Poor, 10 = Excellent)", 1, 10, 6)
community = st.sidebar.slider("Community Support (1 = Weak, 10 = Strong)", 1, 10, 6)
activity = st.sidebar.slider("Physical Activity (days/week)", 0, 7, 3)

employment_dict = {"Employed": 0, "Unemployed": 1, "Student": 2, "Retired": 3}
education_dict = {"No formal education": 0, "High School": 1, "Bachelor's": 2, "Master's": 3, "Doctorate": 4}

input_array = np.array([[income_npr,
                         employment_dict[employment],
                         education_dict[education],
                         housing,
                         isolation,
                         healthcare,
                         community,
                         activity]])
input_scaled = scaler.transform(input_array)

# ----------------------------
# Real-Time Prediction Logic
# ----------------------------
if 'prediction_triggered' not in st.session_state:
    st.session_state['prediction_triggered'] = False

if st.button("Predict Mental Health Risk"):
    st.session_state['prediction_triggered'] = True

if st.session_state['prediction_triggered']:
    prediction = model.predict(input_scaled)[0]
    prediction = float(np.clip(prediction, 0, 10))
    st.session_state['predicted_risk'] = prediction

# ----------------------------
# Show Prediction and Suggestions
# ----------------------------
if 'predicted_risk' in st.session_state:
    prediction = st.session_state['predicted_risk']
    st.subheader("📉 Your Predicted Mental Health Risk Score:")
    st.write(f"**{prediction:.2f}** out of 10")

    # Interpretation
    if prediction > 7:
        st.error("High Risk: You may need professional support and stronger social engagement.")
    elif prediction > 4:
        st.warning("Moderate Risk: Consider improving lifestyle and community interactions.")
    else:
        st.success("Low Risk: Maintain your current healthy practices.")

    # Suggestions
    st.markdown("### 📌 Suggestions Based on Your Profile")
    if isolation >= 7:
        st.info("- High isolation levels detected. Try joining social or community groups.")
    if income_npr < 1200000:
        st.info("- Low income may cause stress. Seek financial aid or budgeting tools.")
    if healthcare < 5:
        st.info("- Improve access to healthcare via mobile clinics or community services.")
    if community < 4:
        st.info("- Weak community support noted. Consider joining local events or volunteering.")
    if activity < 3:
        st.info("- Physical activity boosts mood. Aim for 3–5 days/week.")
    if employment == "Unemployed":
        st.info("- Unemployment can cause stress. Seek job training, counseling, or community work.")
    if education in ["No formal education", "High School"]:
        st.info("- Learning, even informally, improves mental resilience.")
    if housing <= 4:
        st.info("- Poor housing impacts well-being. Consider local housing support options.")
    if prediction > 8:
        st.info("- Very high risk. Consider talking to a mental health professional.")
    if prediction < 3 and community >= 7:
        st.info("- Excellent community support! Consider helping others through outreach.")
    if prediction >= 5 and activity <= 2:
        st.info("- Combine regular exercise with social engagement to manage risk.")
    if income_npr >= 7000000 and prediction > 6:
        st.info("- Even with high income, stress can raise risk. Focus on balance and wellness.")
    if isolation >= 8 and community <= 4:
        st.info("- Social reconnection is critical. Join local meetups or support groups.")

# ----------------------------
# Show Risk Equation
# ----------------------------
if st.checkbox("Show Risk Equation"):
    st.markdown("#### Multiple Regression Equation")
    st.latex(equation_string)

# ----------------------------
# Plot: Risk vs Income
# ----------------------------
if st.checkbox("Plot: Risk vs Income"):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["Income_NPR"], df["Risk"], alpha=0.6, color='orange', label="Data Points")

    X_income = df["Income_NPR"].values.reshape(-1, 1)
    model_income = LinearRegression()
    model_income.fit(X_income, y)
    y_pred_income = model_income.predict(X_income)

    ax.plot(df["Income_NPR"], y_pred_income, color="blue", linewidth=2, label="Regression Line")
    ax.set_xlabel("Annual Income (NPR)")
    ax.set_ylabel("Predicted Risk Score")
    ax.set_title("Risk Score vs. Income")
    ax.legend()
    st.pyplot(fig)

# ----------------------------
# Plot: Risk vs Social Isolation
# ----------------------------
if st.checkbox("Plot: Risk vs Social Isolation"):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["Isolation"], df["Risk"], alpha=0.6, color='teal', label="Data Points")

    X_isolation = df["Isolation"].values.reshape(-1, 1)
    model_isolation = LinearRegression()
    model_isolation.fit(X_isolation, y)
    y_pred_isolation = model_isolation.predict(X_isolation)

    ax.plot(df["Isolation"], y_pred_isolation, color="red", linewidth=2, label="Regression Line")
    ax.set_xlabel("Social Isolation Level")
    ax.set_ylabel("Predicted Risk Score")
    ax.set_title("Risk Score vs. Social Isolation")
    ax.legend()
    st.pyplot(fig)

# ----------------------------
# Show Sample Data
# ----------------------------
if st.checkbox("Show Sample Dataset"):
    st.dataframe(df.head(20))
