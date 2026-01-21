# 🛡️ Retirement SWP Optimizer & Stress Tester

A comprehensive financial planning tool built with Python and Streamlit to simulate retirement portfolio longevity using **Monte Carlo Simulations** and **Historical Market Stress Tests** in Indian Rupees (₹).



## 🚀 Overview
Standard retirement planning often fails because it assumes a linear "average" return. This tool accounts for **Sequence of Returns Risk**—the risk that a market crash early in retirement can deplete a portfolio even if long-term averages are positive.

This application allows users to simulate thousands of market paths to find their **Probability of Success** while accounting for inflation and significant historical crashes.

## ✨ Key Features
- **Monte Carlo Engine:** Simulates up to 1,000 unique market paths based on volatility and mean returns.
- **INR-Centric Assumptions:** Default parameters (10% returns, 6% inflation) are optimized for the Indian economy.
- **Historical Stress Tests:** Simulate the impact of the 2008 Financial Crisis, 2000 Dot-com Bubble, or 1929 Great Depression on your specific plan.
- **Inflation-Adjusted SWP:** Automatically scales your monthly withdrawals to maintain purchasing power over decades.
- **Professional PDF Export:** Generate a full report containing both your results and the underlying methodology.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/monte-carlo-simulation-swp-retirement-optimizer-tool.git](https://github.com/YOUR_USERNAME/monte-carlo-simulation-swp-retirement-optimizer-tool.git)
   cd monte-carlo-simulation-swp-retirement-optimizer-tool

Install dependencies:Ensure you have a requirements.txt file in your directory with the following contents:
streamlit
pandas
numpy
plotly
fpdf
Then run:
Bash
pip install -r requirements.txt
Run the app:
Bash
streamlit run app.py

