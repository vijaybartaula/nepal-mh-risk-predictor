# Mental Health Risk Predictor

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Status](https://img.shields.io/badge/status-beta-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

## 🧠 Overview

The Mental Health Risk Predictor is a data-driven tool designed to estimate potential mental health risk levels in Nepal based on social determinants of health (SDOH). This application analyzes socioeconomic factors and lifestyle data to generate a personal risk assessment on a 0-10 scale, where higher scores indicate potentially greater vulnerability to mental health issues.

## Key Features

- **Personalized Risk Assessment**: Generate an individualized mental health risk score based on your specific socioeconomic profile.
- **Evidence-Informed Recommendations**: Receive tailored suggestions based on your risk profile and contributing factors.
- **Visual Analytics**: Explore the relationships between different socioeconomic factors and mental health risk through interactive visualizations.
- **Educational Resources**: Learn about the social determinants affecting mental health in the Nepal context.
- **Privacy-Focused**: All data processing happens locally on your device with no external data storage.

## Social Determinants Analyzed

The predictor evaluates the following factors:

- Income level (NPR)
- Employment status
- Education level
- Housing quality
- Social isolation
- Healthcare access
- Community support
- Physical activity

## Getting Started

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vijaybartaula/nepal-mh-risk-predictor.git
   cd mental-health-risk-predictor
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the application:
   ```bash
   streamlit run app.py
   ```

5. Open your browser and navigate to: `http://localhost:8501`

## 📖 Usage Guide

1. **Input Your Data**: Use the sidebar sliders and dropdown menus to enter your socioeconomic profile.
2. **Generate Prediction**: Click the "Predict Mental Health Risk" button to calculate your risk score.
3. **Review Results**: Examine your risk score and personalized recommendations.
4. **Explore Relationships**: Toggle the visualization options to better understand how different factors affect mental health risk.

## 🧪 Model Information

The core prediction engine uses a multiple linear regression model trained on a synthetic dataset that mirrors expected societal patterns in Nepal. While not trained on clinical data, the model incorporates realistic correlations based on global mental health research and Nepal-specific socioeconomic contexts.

The risk equation is a weighted sum of standardized inputs:

```
Risk Score = β₀ + β₁×Income + β₂×Employment + β₃×Education + β₄×Housing + 
             β₅×Isolation + β₆×Healthcare + β₇×Community + β₈×Physical_Activity
```

Where βᵢ are the coefficients derived from our regression analysis.

## 📝 Important Notes

- This tool is for **educational and informational purposes only**.
- It is **not a clinical diagnostic tool** and should not replace professional medical advice.
- The model is based on synthetic data informed by research but not validated in clinical settings.
- Risk scores should be interpreted as relative indicators rather than absolute assessments.

## 🛠️ Development

### Tech Stack

- **Frontend & Backend**: Python with Streamlit
- **Data Processing**: NumPy, Pandas
- **Machine Learning**: scikit-learn
- **Visualization**: Matplotlib

### Running Tests

```bash
pytest tests/
```
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 More Information

For detailed information, you can check the [Whitepaper](https://github.com/vijaybartaula/nepal-mh-risk-predictor/blob/main/WHITEPAPER.md).
