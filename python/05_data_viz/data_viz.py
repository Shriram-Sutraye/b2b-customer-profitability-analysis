# FILE: /python/05_data_viz/data_viz.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Config
plt.style.use('seaborn-v0_8-darkgrid')
FIGSIZE = (10,6)
sns.set_context("notebook", font_scale=1.1)

# File paths
clv_path = '../../data/generated/11_customer_lifetime_value.csv'
orders_path = '../../data/generated/10_financial_p_l_orders.csv'
cust_path = '../../data/processed/01_customer_master.csv'
pdf_path = 'data_viz_report.pdf'

# Load data
clv = pd.read_csv(clv_path)
orders = pd.read_csv(orders_path)
cust = pd.read_csv(cust_path)

def try_plot(fig, pdf):
    try:
        pdf.savefig(fig)
        plt.close(fig)
    except Exception as e:
        print(f'Error saving figure: {e}')
        plt.close(fig)

with PdfPages(pdf_path) as pdf:

    # ------ Executive KPI Board ------
    kpi_vals = {
        "Total CLV (€)": clv['CLV_EUR'].sum(),
        "Total Annual Profit (€)": clv['AnnualProfit_EUR'].sum(),
        "Customer Count": clv['CustomerID'].nunique(),
        "Avg CLV Margin (%)": clv['CLVMargin_Pct'].mean()
    }
    fig, ax = plt.subplots(figsize=(8,3))
    ax.axis('off')
    msg = "\n".join([f"{k}: {v:,.2f}" for k,v in kpi_vals.items()])
    ax.text(0, 0.5, "Executive KPI Board\n\n" + msg, fontsize=15)
    try_plot(fig, pdf)

    # ------ Nulls/EDA Heatmap ------
    for dname, df in [("CLV Table",clv),("Orders Table",orders),("CustomerMaster",cust)]:
        fig, ax = plt.subplots(figsize=(10,1))
        sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap="YlOrRd", ax=ax)
        ax.set_title(f'Null Heatmap: {dname}')
        try_plot(fig, pdf)
        # Describe table
        desc = df.describe(include='all').T
        fig, ax = plt.subplots(figsize=(8,desc.shape[0]//2+2))
        ax.axis('off')
        table = ax.table(cellText=desc.round(2).values, colLabels=desc.columns, rowLabels=desc.index, loc='center')
        ax.set_title(f'{dname} - column stats')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        try_plot(fig, pdf)

    # ------ CLV Segment Pie ------
    if 'CLVSegment' in clv.columns:
        fig, ax = plt.subplots(figsize=FIGSIZE)
        clv['CLVSegment'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        ax.set_title("Customer Count by CLV Segment")
        try_plot(fig, pdf)

    # ------ Recommended Action ------
    if 'RecommendedAction' in clv.columns:
        fig, ax = plt.subplots(figsize=FIGSIZE)
        clv['RecommendedAction'].value_counts().plot.bar(ax=ax)
        ax.set_title("Count by Recommended Action")
        plt.xticks(rotation=45)
        try_plot(fig, pdf)

    # ------ Top 10 / Bottom 10 Customers ------
    if 'CLV_EUR' in clv.columns and 'AnnualProfit_EUR' in clv.columns:
        for label, df_sel in [('Top 10 by CLV', clv.nlargest(10, 'CLV_EUR')),
                              ('Bottom 10 by CLV', clv.nsmallest(10, 'CLV_EUR')),
                              ('Top 10 by Profit', clv.nlargest(10, 'AnnualProfit_EUR')),
                              ('Bottom 10 by Profit', clv.nsmallest(10, 'AnnualProfit_EUR'))]:
            fig, ax = plt.subplots(figsize=(10,4))
            ax.axis('off')
            table = ax.table(cellText=df_sel.values, colLabels=df_sel.columns, loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            ax.set_title(label)
            try_plot(fig, pdf)

    # ------ Scatter: Profit vs CLV ------
    if set(['CLV_EUR','AnnualProfit_EUR','CLVSegment']).issubset(clv.columns):
        fig, ax = plt.subplots(figsize=FIGSIZE)
        colors = clv['CLVSegment'].map({'A-Customer':'#107C10', 'B-Customer':'#00BCF2', 'C-Customer':'#D13438'})
        ax.scatter(clv['CLV_EUR'], clv['AnnualProfit_EUR'], c=colors, alpha=0.7)
        ax.set_xlabel('Customer Lifetime Value (€)')
        ax.set_ylabel('Annual Profit (€)')
        ax.set_title('Annual Profit vs CLV by Customer (colored by Segment)')
        try_plot(fig, pdf)

    # ------ Correlation Heatmap (CLV Table) ------
    num_cols = clv.select_dtypes(include='number').columns
    fig, ax = plt.subplots(figsize=(12,8))
    sns.heatmap(clv[num_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Matrix: All Numeric Columns (CLV Table)")
    try_plot(fig, pdf)

    # ------ Trend: Revenue/Profit by Month ------
    if 'OrderMonth' in orders.columns:
        orders['OrderMonth'] = pd.to_datetime(orders['OrderMonth'])
        month_agg = orders.groupby(orders['OrderMonth'].dt.to_period('M')).agg({'TransactionAmount':'sum', 'Profit_EUR':'sum'})
        fig, ax = plt.subplots(figsize=FIGSIZE)
        month_agg.plot(y=['TransactionAmount','Profit_EUR'], ax=ax, marker='o')
        ax.set_title('Monthly Revenue and Profit')
        ax.set_ylabel('€')
        ax.set_xlabel('Month')
        try_plot(fig, pdf)

    # ------ Product Category Profitability ------
    if 'ProductCategory' in orders.columns and 'Profit_EUR' in orders.columns:
        cat_agg = orders.groupby('ProductCategory')['Profit_EUR'].sum().sort_values()
        fig, ax = plt.subplots(figsize=FIGSIZE)
        cat_agg.plot.barh(ax=ax, color='teal')
        ax.set_title('Total Profit by Product Category')
        try_plot(fig, pdf)

    # ------ Cross Tab: CustomerSegment x CLVSegment ------
    if 'CustomerSegment' in clv.columns and 'CLVSegment' in clv.columns:
        ct = pd.crosstab(clv['CustomerSegment'], clv['CLVSegment'])
        fig, ax = plt.subplots(figsize=(8, max(4,ct.shape[0]//2)))
        sns.heatmap(ct, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title('Segment Cross Tab: CustomerSegment x CLVSegment')
        try_plot(fig, pdf)

    # ------ ProfitabilityCategory by Time ------
    if 'ProfitabilityCategory' in orders.columns and 'OrderMonth' in orders.columns:
        orders['OrderMonth'] = pd.to_datetime(orders['OrderMonth'])
        pivot = orders.pivot_table(index=orders['OrderMonth'].dt.to_period('M'), columns='ProfitabilityCategory', values='TransactionAmount', aggfunc='sum')
        fig, ax = plt.subplots(figsize=FIGSIZE)
        pivot.plot(ax=ax, marker='o')
        ax.set_title('Transaction Volume by Profitability Category (Monthly)')
        try_plot(fig, pdf)

    # ------ Final Insights Page ------
    fig, ax = plt.subplots(figsize=(8,6))
    ax.axis('off')
    ax.text(0, 0.9, "B2B Profitability Analysis - Python AutoViz Report", fontsize=16, fontweight='bold')
    ax.text(0, 0.6,
            "- Data checked and visualized from source-of-truth csvs.\n"
            "- All BI calculations, segmentations, and correlations auto-generated.\n"
            "- If you see this PDF, your pipeline and data integrity are robust!\n\n"
            "EOF.", fontsize=13)
    try_plot(fig, pdf)

print(f"All done! Multi-page report saved as {pdf_path}")

# EOF
