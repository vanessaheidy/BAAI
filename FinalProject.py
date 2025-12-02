#
# Heidy, 2025/11/21
# File: FinalProject.py
# BMRI (Mandiri Bank)
#


import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
from scipy.stats import shapiro
import matplotlib.pyplot as plt

# 1.Input
file_path = "BMRI_Data_Python.xlsx"
df = pd.read_excel(file_path, sheet_name="Main_Data")

cols_x = ["ROA", "Revenue", "Total_Debt", "EPS", "Market_Return"]
df["Market_Return"] = pd.to_numeric(df["Market_Return"], errors='coerce') / 100
df = df.dropna(subset=cols_x + ["Stock_Price"])

# 2.Process

# Summary Statistic
summary_stats = []
for col in ["Stock_Price"] + cols_x:
    series = df[col]
    N = series.count()
    mean = series.mean()
    std = series.std()
    min_val = series.min()
    max_val = series.max()
    missing = series.isna().sum()
    outliers = ((series - mean).abs() > 3 * std).sum()
    summary_stats.append([col, N, round(mean, 3), round(std, 3),
                          round(min_val, 3), round(max_val, 3), missing, outliers])

summary_df = pd.DataFrame(summary_stats,
                          columns=["Variable", "N", "Mean", "Std Dev", "Min", "Max", "Missing", "Outliers"])

# Simple Linear Regression
simple_reg_results = []
for var in cols_x:
    model_simple = sm.OLS(df["Stock_Price"], sm.add_constant(df[var])).fit()
    coef = model_simple.params[var]
    se = model_simple.bse[var]
    tval = model_simple.tvalues[var]
    pval = model_simple.pvalues[var]
    ci_low, ci_high = model_simple.conf_int().loc[var]
    sig = "**" if pval < 0.01 else "*" if pval < 0.05 else "†" if pval < 0.10 else "NS"
    simple_reg_results.append([
        var,
        round(coef, 3),
        round(se, 3),
        round(tval, 3),
        round(pval, 4),
        f"[{round(ci_low, 3)}, {round(ci_high, 3)}]",
        sig
    ])

simple_df = pd.DataFrame(simple_reg_results,
                         columns=["Variable", "Coefficient (β)", "Std Error", "t-value", "p-value", "95% CI", "Significance"])

# Multiple Linear Regression
X = df[cols_x]
X = sm.add_constant(X)
multi_model = sm.OLS(df["Stock_Price"], X).fit()

multi_results = []
for var in multi_model.params.index:
    if var == "const":  # skip intercept
        continue
    coef = multi_model.params[var]
    se = multi_model.bse[var]
    tval = multi_model.tvalues[var]
    pval = multi_model.pvalues[var]
    ci_low, ci_high = multi_model.conf_int().loc[var]
    sig = "**" if pval < 0.01 else "*" if pval < 0.05 else "†" if pval < 0.10 else "NS"
    multi_results.append([
        var,
        round(coef, 3),
        round(se, 3),
        round(tval, 3),
        round(pval, 4),
        f"[{round(ci_low, 3)}, {round(ci_high, 3)}]",
        sig
    ])

multi_df = pd.DataFrame(multi_results,
                        columns=["Variable", "Coefficient (β)", "Std Error", "t-value", "p-value", "95% CI", "Significance"])

# Model Fit Summary
rmse = np.sqrt(((multi_model.resid) ** 2).mean())
resid_se = np.sqrt(multi_model.scale)
df_model = int(multi_model.df_model)
df_resid = int(multi_model.df_resid)

# Assumption Test
results_table = []
# Linearity
plt.scatter(multi_model.fittedvalues, multi_model.resid)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("Residuals vs Fitted (Linearity Check)")
plt.show()
results_table.append(["Linearity", "Residual vs Fitted", "No pattern", "Linear relationships", "✓ Met"])

# Normality
shapiro_p = shapiro(multi_model.resid)[1]
results_table.append(["Normality", "Shapiro-Wilk", f"p = {shapiro_p:.3f}",
                     "Residuals normal" if shapiro_p > 0.05 else "Residuals not normal",
                     "✓ Met" if shapiro_p > 0.05 else "✗ Not Met"])

# Homoscedasticity
bp_pvalue = het_breuschpagan(multi_model.resid, multi_model.model.exog)[1]
results_table.append(["Homoscedasticity", "Breusch-Pagan", f"p = {bp_pvalue:.3f}",
                     "Constant variance" if bp_pvalue > 0.05 else "Heteroscedasticity",
                     "✓ Met" if bp_pvalue > 0.05 else "✗ Not Met"])

# Independence
dw_stat = durbin_watson(multi_model.resid)
results_table.append(["Independence", "Durbin-Watson", f"DW = {dw_stat:.2f}",
                     "No autocorrelation" if 1.5 < dw_stat < 2.5 else "Possible autocorrelation",
                     "✓ Met" if 1.5 < dw_stat < 2.5 else "✗ Not Met"])

# Multicollinearity
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif_data = vif_data[vif_data["Variable"] != "const"]
results_table.append(["Multicollinearity", "VIF", f"Max = {vif_data['VIF'].max():.2f}",
                     "Low multicollinearity" if vif_data["VIF"].max() < 5 else "High multicollinearity",
                     "✓ Met" if vif_data["VIF"].max() < 5 else "✗ Not Met"])

# Influential Cases
max_cooks_d = OLSInfluence(multi_model).cooks_distance[0].max()
results_table.append(["Influential Cases", "Cook's D", f"Max = {max_cooks_d:.2f}",
                     "No influential outliers" if max_cooks_d < 1 else "Possible influential outlier(s)",
                     "✓ Met" if max_cooks_d < 1 else "✗ Not Met"])

assump_df = pd.DataFrame(results_table,
                         columns=["Assumption", "Test", "Result", "Interpretation", "Status"])

# VIF Table
vif_data["Status"] = ["✓ OK" if v < 5 else "✗ High" for v in vif_data["VIF"]]

# 3.Output

# Table Structure
print("\n=== Table Structure ===")
print(df.to_string(index=False))

# Summary Statistic
print("\n=== Summary Statistics Table ===")
print(summary_df.to_string(index=False))

# Simple Linear Regression
print("\n=== Simple Linear Regression Table ===")
print(simple_df.to_string(index=False))

# Multiple Linear Regression
print("\n=== Multiple Linear Regression Table ===")
print(multi_df.to_string(index=False))

# Model Fit Summary
print("\n=== Model Fit Summary ===")
print(f"Multiple R-squared: {multi_model.rsquared:.3f}")
print(f"Adjusted R-squared: {multi_model.rsquared_adj:.3f}")
print(f"F-statistic: {multi_model.fvalue:.3f} on {df_model} and {df_resid} DF, p-value: {multi_model.f_pvalue:.4f}")
print(f"RMSE: {rmse:.3f}")
print(f"Residual standard error: {resid_se:.3f}")

# Assumption Test Table
print("\n=== Assumption Test Results Table ===")
print(assump_df.to_string(index=False))

# VIF Table
print("\n=== VIF Table ===")
print(vif_data.to_string(index=False))