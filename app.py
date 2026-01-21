Python 3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import streamlit as st
... import pandas as pd
... import numpy as np
... import plotly.graph_objects as go
... from fpdf import FPDF
... import base64
... 
... # --- Page Configuration ---
... st.set_page_config(page_title="Retirement SWP Optimizer", layout="wide")
... 
... # --- PDF Generation Function ---
... def create_pdf(success_rate, median_balance, years, withdrawal, scenario):
...     pdf = FPDF()
...     pdf.add_page()
...     pdf.set_font("Arial", 'B', 16)
...     pdf.cell(200, 10, "Retirement SWP Simulation Report", ln=True, align='C')
...     pdf.ln(10)
...     
...     pdf.set_font("Arial", size=12)
...     pdf.cell(200, 10, f"Stress Test Scenario: {scenario}", ln=True)
...     pdf.cell(200, 10, f"Success Probability: {success_rate:.1f}%", ln=True)
...     pdf.cell(200, 10, f"Median Ending Balance: ${median_balance:,.2f}", ln=True)
...     pdf.cell(200, 10, f"Retirement Duration: {years} years", ln=True)
...     pdf.cell(200, 10, f"Initial Monthly Withdrawal: ${withdrawal:,.2f}", ln=True)
...     
...     pdf.ln(20)
...     pdf.set_font("Arial", 'I', 10)
...     pdf.multi_cell(0, 10, "Disclaimer: This simulation uses a normal distribution of returns. "
...                           "Historical stress tests simulate early-retirement shocks. "
...                           "Past performance is not indicative of future results.")
...     return pdf.output(dest='S').encode('latin-1')
... 
... # --- UI Header ---
st.title("🛡️ Retirement SWP Optimizer & Stress Tester")
st.markdown("Simulate market volatility and historical crashes to see if your money lasts.")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("📈 Financial Inputs")
    initial_investment = st.number_input("Current Portfolio Value ($)", value=1000000, step=50000)
    monthly_withdrawal = st.number_input("Monthly Withdrawal ($)", value=4000, step=500)
    years = st.slider("Years in Retirement", 10, 50, 30)
    
    st.header("🎲 Market Assumptions")
    avg_return = st.slider("Expected Annual Return (%)", 0.0, 15.0, 7.0) / 100
    volatility = st.slider("Annual Volatility (%)", 0.0, 25.0, 12.0) / 100
    inflation = st.slider("Expected Inflation (%)", 0.0, 10.0, 3.0) / 100
    
    st.header("⚠️ Stress Test")
    crash_scenario = st.selectbox(
        "Apply Historical Shock?",
        ["None", "2008 Financial Crisis", "2000 Dot-com Bubble", "1929 Great Depression"]
    )
    
    simulations = st.selectbox("Number of Simulations", [100, 500, 1000], index=1)

# --- Calculation Engine ---
def run_monte_carlo():
    n_months = years * 12
    monthly_return = (1 + avg_return)**(1/12) - 1
    monthly_vol = volatility / np.sqrt(12)
    monthly_inflation = (1 + inflation)**(1/12) - 1
    
    shocks = {
        "None": {"drop": 0, "duration": 0},
        "2008 Financial Crisis": {"drop": -0.50, "duration": 18},
        "2000 Dot-com Bubble": {"drop": -0.45, "duration": 36},
        "1929 Great Depression": {"drop": -0.89, "duration": 33}
    }
    
    selected_shock = shocks[crash_scenario]
    all_paths = np.zeros((simulations, n_months))
    
    for s in range(simulations):
        current_balance = initial_investment
        current_withdrawal = monthly_withdrawal
        for m in range(n_months):
            # Market Return
            m_return = np.random.normal(monthly_return, monthly_vol)
            
            # Apply Stress Test if in the shock period
            if m < selected_shock["duration"]:
                m_return += (selected_shock["drop"] / selected_shock["duration"])
            
            # Update Balance
            current_balance = (current_balance * (1 + m_return)) - current_withdrawal
            
            # Inflation Adjust for next month
            current_withdrawal *= (1 + monthly_inflation)
            
            if current_balance <= 0:
                all_paths[s, m:] = 0
                break
            all_paths[s, m] = current_balance
            
    return all_paths

# Run Sim
results = run_monte_carlo()
success_rate = (results[:, -1] > 0).mean() * 100
median_final = np.median(results[:, -1])

# --- Main Dashboard ---
col1, col2, col3 = st.columns(3)
col1.metric("Success Rate", f"{success_rate:.1f}%")
col2.metric("Median Ending Balance", f"${median_final:,.0f}")
col3.metric("Stress Test Active", crash_scenario)

# --- Plotting ---
fig = go.Figure()
x_axis = np.arange(years * 12) / 12

for i in range(min(simulations, 100)):
    fig.add_trace(go.Scatter(x=x_axis, y=results[i], mode='lines', 
                             line=dict(width=0.7), opacity=0.3, showlegend=False))

fig.update_layout(
    title=f"Portfolio Projections ({crash_scenario} scenario)",
    xaxis_title="Years in Retirement",
    yaxis_title="Portfolio Balance ($)",
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)

# --- PDF Download ---
st.divider()
pdf_bytes = create_pdf(success_rate, median_final, years, monthly_withdrawal, crash_scenario)
st.download_button(
    label="📥 Download Detailed PDF Report",
    data=pdf_bytes,
    file_name="Retirement_Stress_Test.pdf",
    mime="application/pdf"
)

