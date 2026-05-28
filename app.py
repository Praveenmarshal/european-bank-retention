import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="European Bank · Retention Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Theme ─────────────────────────────────────────────────────────────────────
COLORS = {
    "primary":   "#0C447C",
    "blue":      "#185FA5",
    "blue_light":"#378ADD",
    "teal":      "#0F6E56",
    "teal_light":"#1D9E75",
    "amber":     "#BA7517",
    "red":       "#A32D2D",
    "red_dark":  "#791F1F",
    "pink":      "#993556",
    "gray":      "#5F5E5A",
    "bg":        "#F8F9FB",
}

TIER_COLORS = {
    "Active · Multi-product":   COLORS["teal"],
    "Inactive · Multi-product": COLORS["blue"],
    "Active · Single-product":  COLORS["amber"],
    "Inactive · Single-product":COLORS["red"],
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0C447C;
    border-right: none;
}
section[data-testid="stSidebar"] * { color: #B5D4F4 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] h1, h2, h3 { color: #E6F1FB !important; }
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background: #185FA5 !important; }
section[data-testid="stSidebar"] hr { border-color: #185FA5 !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E8ECF0;
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 1px 4px rgba(12,68,124,0.06);
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 11px !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #888780 !important;
    font-weight: 500;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 600;
    color: #0C447C !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* Header */
.ecb-header {
    background: linear-gradient(135deg, #0C447C 0%, #185FA5 100%);
    border-radius: 12px;
    padding: 22px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.ecb-header h1 { color: #E6F1FB; font-size: 20px; font-weight: 600; margin: 0; }
.ecb-header p  { color: #85B7EB; font-size: 13px; margin: 4px 0 0; }
.ecb-badge {
    background: rgba(255,255,255,0.12);
    border-radius: 8px;
    padding: 10px 18px;
    text-align: center;
    color: #E6F1FB;
}
.ecb-badge .val  { font-size: 24px; font-weight: 600; }
.ecb-badge .lbl  { font-size: 10px; color: #85B7EB; letter-spacing: 0.08em; }

/* Section headers */
.section-hdr {
    font-size: 14px;
    font-weight: 600;
    color: #0C447C;
    border-left: 4px solid #185FA5;
    padding-left: 10px;
    margin: 8px 0 16px;
    letter-spacing: -0.01em;
}

/* Insight box */
.insight-box {
    background: #EBF3FB;
    border-left: 4px solid #185FA5;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: #0C447C;
    line-height: 1.6;
    margin-top: 8px;
}
.insight-box.warn  { background: #FDF3E0; border-color: #BA7517; color: #633806; }
.insight-box.danger{ background: #FBEDED; border-color: #A32D2D; color: #4A1B0C; }
.insight-box.good  { background: #E8F4EF; border-color: #0F6E56; color: #04342C; }

/* Tier cards */
.tier-card {
    background: #fff;
    border: 1px solid #E8ECF0;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* Footer */
.footer {
    text-align: center;
    color: #B4B2A9;
    font-size: 11px;
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #E8ECF0;
}

div[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: #F1F4F8;
    border-radius: 8px !important;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 500;
    color: #5F5E5A;
}
.stTabs [aria-selected="true"] {
    background: #0C447C !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("European_Bank.csv")
    df.columns = df.columns.str.strip()

    # Derived columns
    df["IsActiveMember"]  = df["IsActiveMember"].astype(int)
    df["HasCrCard"]       = df["HasCrCard"].astype(int)
    df["Exited"]          = df["Exited"].astype(int)

    def engagement_tier(row):
        active   = row["IsActiveMember"] == 1
        products = row["NumOfProducts"]
        if active and products >= 2:   return "Active · Multi-product"
        if active and products == 1:   return "Active · Single-product"
        if not active and products >= 2: return "Inactive · Multi-product"
        return "Inactive · Single-product"

    df["EngagementTier"] = df.apply(engagement_tier, axis=1)

    # Relationship Strength Index
    df["RSI"] = (
        df["IsActiveMember"] * 40
        + df["NumOfProducts"].clip(upper=2) * 20
        + df["HasCrCard"] * 10
        + df["Tenure"].clip(upper=10) * 3
    )
    df["RSI_Tier"] = pd.cut(df["RSI"],
        bins=[0, 49, 79, 120],
        labels=["Low (RSI < 50)", "Medium (50–79)", "High (RSI ≥ 80)"],
        include_lowest=True
    )

    # Age bucket
    df["AgeBucket"] = pd.cut(df["Age"],
        bins=[17, 30, 40, 50, 60, 100],
        labels=["18–30", "31–40", "41–50", "51–60", "60+"]
    )

    # Balance tier
    df["BalanceTier"] = pd.cut(df["Balance"],
        bins=[-1, 0, 50000, 100000, 150000, 999999],
        labels=["Zero", "€1–50k", "€50–100k", "€100–150k", "€150k+"]
    )

    df["SalaryBucket"] = pd.cut(df["EstimatedSalary"],
        bins=[0, 50000, 100000, 150000, 200001],
        labels=["<€50k", "€50–100k", "€100–150k", "€150k+"]
    )

    return df

df_full = load_data()

# ─── Sidebar Filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 ECB Retention Analytics")
    st.markdown("---")

    st.markdown("### 🌍 Geography")
    geo_opts = ["All"] + sorted(df_full["Geography"].unique().tolist())
    selected_geo = st.multiselect("Country", geo_opts[1:], default=geo_opts[1:])

    st.markdown("### 👤 Gender")
    gender_opts = st.multiselect("Gender", ["Male", "Female"], default=["Male", "Female"])

    st.markdown("### 📦 Product Count")
    prod_range = st.slider("Number of products", 1, 4, (1, 4))

    st.markdown("### 💰 Balance Threshold (€)")
    bal_range = st.slider("Balance range", 0, 250_000, (0, 250_000), step=5000)

    st.markdown("### 💼 Salary Threshold (€)")
    sal_range = st.slider("Estimated salary range", 0, 200_000, (0, 200_000), step=5000)

    st.markdown("### 🎯 Membership Status")
    active_filter = st.multiselect("Activity", ["Active", "Inactive"], default=["Active", "Inactive"])

    st.markdown("### 📅 Tenure (years)")
    tenure_range = st.slider("Tenure", 0, 10, (0, 10))

    st.markdown("---")
    st.markdown("<div style='font-size:11px;color:#85B7EB;'>European Central Bank<br>Customer Behavior Analytics</div>", unsafe_allow_html=True)

# ─── Apply Filters ─────────────────────────────────────────────────────────────
df = df_full.copy()

if selected_geo:
    df = df[df["Geography"].isin(selected_geo)]
if gender_opts:
    df = df[df["Gender"].isin(gender_opts)]

df = df[df["NumOfProducts"].between(prod_range[0], prod_range[1])]
df = df[df["Balance"].between(bal_range[0], bal_range[1])]
df = df[df["EstimatedSalary"].between(sal_range[0], sal_range[1])]
df = df[df["Tenure"].between(tenure_range[0], tenure_range[1])]

active_map = {"Active": 1, "Inactive": 0}
if active_filter:
    active_vals = [active_map[a] for a in active_filter]
    df = df[df["IsActiveMember"].isin(active_vals)]

# ─── Header ────────────────────────────────────────────────────────────────────
churn_rate = df["Exited"].mean() * 100 if len(df) > 0 else 0
n_churned  = df["Exited"].sum()

st.markdown(f"""
<div class="ecb-header">
  <div>
    <h1>🏦 Customer Engagement & Retention Analytics</h1>
    <p>European Bank · Behavioral Churn Analysis · {len(df):,} customers in view</p>
  </div>
  <div class="ecb-badge">
    <div class="val">{churn_rate:.1f}%</div>
    <div class="lbl">CHURN RATE</div>
    <div style="font-size:12px;color:#85B7EB;">{n_churned:,} exited</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Engagement Overview",
    "📦 Product Utilization",
    "🔍 High-Value Detector",
    "🧮 Retention Strength"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: ENGAGEMENT OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-hdr">Engagement vs Churn Overview</div>', unsafe_allow_html=True)

    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    total      = len(df)
    n_active   = df["IsActiveMember"].sum()
    n_inactive = total - n_active
    active_churn   = df[df["IsActiveMember"]==1]["Exited"].mean()*100 if n_active else 0
    inactive_churn = df[df["IsActiveMember"]==0]["Exited"].mean()*100 if n_inactive else 0

    col1.metric("Total Customers",   f"{total:,}")
    col2.metric("Churn Rate",        f"{churn_rate:.1f}%",  f"{churn_rate-20.4:.1f}pp vs baseline")
    col3.metric("Active Members",    f"{n_active:,}",       f"{n_active/total*100:.0f}% of portfolio" if total else "N/A")
    col4.metric("Active Churn",      f"{active_churn:.1f}%",   f"{active_churn-14.3:.1f}pp vs baseline")
    col5.metric("Inactive Churn",    f"{inactive_churn:.1f}%", f"{inactive_churn-26.9:.1f}pp vs baseline")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Engagement Tier Analysis ─────────────────────────────────────────────
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown("**Churn rate by engagement tier**")
        tier_stats = (
            df.groupby("EngagementTier")
            .agg(Customers=("Exited","count"), Churned=("Exited","sum"))
            .assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100)
            .reset_index()
        )
        tier_order = ["Active · Multi-product","Inactive · Multi-product","Active · Single-product","Inactive · Single-product"]
        tier_stats = tier_stats.set_index("EngagementTier").reindex([t for t in tier_order if t in tier_stats.index]).reset_index()

        fig_tier = go.Figure()
        for _, row in tier_stats.iterrows():
            color = TIER_COLORS.get(row["EngagementTier"], COLORS["gray"])
            fig_tier.add_trace(go.Bar(
                x=[row["EngagementTier"]],
                y=[row["ChurnRate"]],
                marker_color=color,
                text=f"{row['ChurnRate']:.1f}%",
                textposition="outside",
                name=row["EngagementTier"],
                customdata=[[row["Customers"], row["Churned"]]],
                hovertemplate="<b>%{x}</b><br>Churn: %{y:.1f}%<br>Customers: %{customdata[0]:,}<br>Churned: %{customdata[1]:,}<extra></extra>",
                showlegend=False,
            ))

        fig_tier.add_hline(y=churn_rate, line_dash="dash", line_color="#888", annotation_text=f"Average {churn_rate:.1f}%", annotation_font_size=11)
        fig_tier.update_layout(
            height=320, paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0", range=[0, tier_stats["ChurnRate"].max()*1.25 if len(tier_stats) else 50]),
            xaxis=dict(title=""),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_tier, use_container_width=True)

    with col_r:
        st.markdown("**Customer distribution across tiers**")
        if len(tier_stats) > 0:
            fig_pie = go.Figure(go.Pie(
                labels=tier_stats["EngagementTier"],
                values=tier_stats["Customers"],
                marker_colors=[TIER_COLORS.get(t, COLORS["gray"]) for t in tier_stats["EngagementTier"]],
                hole=0.5,
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>%{value:,} customers<br>%{percent}<extra></extra>",
                textfont_size=12,
            ))
            fig_pie.update_layout(
                height=320, paper_bgcolor="white", plot_bgcolor="white",
                margin=dict(t=20, b=10, l=0, r=40),
                legend=dict(font=dict(size=11), orientation="v"),
                font=dict(family="Inter"),
                annotations=[dict(text=f"{total:,}<br>customers", x=0.5, y=0.5, font_size=13, showarrow=False)]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # Engagement insight
    if len(tier_stats) >= 2:
        best = tier_stats.loc[tier_stats["ChurnRate"].idxmin(), "EngagementTier"]
        worst = tier_stats.loc[tier_stats["ChurnRate"].idxmax(), "EngagementTier"]
        best_rate = tier_stats["ChurnRate"].min()
        worst_rate = tier_stats["ChurnRate"].max()
        st.markdown(f'<div class="insight-box"><b>📌 Key finding:</b> <b>{worst}</b> customers churn at {worst_rate:.1f}% — <b>{worst_rate/best_rate:.1f}×</b> higher than <b>{best}</b> customers ({best_rate:.1f}%). Engagement combined with product depth is the strongest combined retention lever in this dataset.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Geography + Age ──────────────────────────────────────────────────────
    col_g, col_a = st.columns(2)

    with col_g:
        st.markdown("**Churn rate by geography**")
        geo_stats = df.groupby("Geography").agg(
            Customers=("Exited","count"), Churned=("Exited","sum")
        ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100).reset_index()

        fig_geo = px.bar(geo_stats, x="Geography", y="ChurnRate",
            color="ChurnRate",
            color_continuous_scale=[[0,"#0F6E56"],[0.5,"#BA7517"],[1,"#A32D2D"]],
            text=geo_stats["ChurnRate"].apply(lambda x: f"{x:.1f}%"),
            hover_data={"Customers": True, "Churned": True},
        )
        fig_geo.update_traces(textposition="outside", marker_line_width=0)
        fig_geo.update_layout(
            height=280, paper_bgcolor="white", plot_bgcolor="white",
            coloraxis_showscale=False,
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0"),
            xaxis=dict(title=""),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    with col_a:
        st.markdown("**Churn rate by age group**")
        age_stats = df.groupby("AgeBucket", observed=True).agg(
            Customers=("Exited","count"), Churned=("Exited","sum")
        ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100).reset_index()

        fig_age = px.bar(age_stats, x="AgeBucket", y="ChurnRate",
            color="ChurnRate",
            color_continuous_scale=[[0,"#1D9E75"],[0.4,"#BA7517"],[1,"#791F1F"]],
            text=age_stats["ChurnRate"].apply(lambda x: f"{x:.1f}%"),
        )
        fig_age.update_traces(textposition="outside", marker_line_width=0)
        fig_age.update_layout(
            height=280, paper_bgcolor="white", plot_bgcolor="white",
            coloraxis_showscale=False,
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0"),
            xaxis=dict(title="Age Group"),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_age, use_container_width=True)

    # ── Gender + Tenure ──────────────────────────────────────────────────────
    col_gen, col_ten = st.columns(2)

    with col_gen:
        st.markdown("**Churn rate by gender**")
        gen_stats = df.groupby("Gender").agg(
            Customers=("Exited","count"), Churned=("Exited","sum")
        ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100).reset_index()

        fig_gen = px.bar(gen_stats, x="Gender", y="ChurnRate",
            color="Gender",
            color_discrete_map={"Male": COLORS["blue"], "Female": COLORS["pink"]},
            text=gen_stats["ChurnRate"].apply(lambda x: f"{x:.1f}%"),
        )
        fig_gen.update_traces(textposition="outside", marker_line_width=0)
        fig_gen.update_layout(
            height=260, paper_bgcolor="white", plot_bgcolor="white",
            showlegend=False,
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0"),
            xaxis=dict(title=""),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_gen, use_container_width=True)

    with col_ten:
        st.markdown("**Churn rate by tenure (years)**")
        ten_stats = df.groupby("Tenure").agg(
            Customers=("Exited","count"), Churned=("Exited","sum")
        ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100).reset_index()

        fig_ten = go.Figure()
        fig_ten.add_trace(go.Scatter(
            x=ten_stats["Tenure"], y=ten_stats["ChurnRate"],
            mode="lines+markers",
            line=dict(color=COLORS["blue"], width=2.5),
            marker=dict(size=8, color=COLORS["primary"]),
            fill="tozeroy", fillcolor="rgba(24,95,165,0.08)",
            hovertemplate="Tenure %{x} yrs → %{y:.1f}% churn<extra></extra>",
        ))
        fig_ten.add_hline(y=churn_rate, line_dash="dash", line_color="#ccc", annotation_text=f"Avg {churn_rate:.1f}%", annotation_font_size=10)
        fig_ten.update_layout(
            height=260, paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0"),
            xaxis=dict(title="Tenure (years)"),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_ten, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: PRODUCT UTILIZATION
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-hdr">Product Utilization Impact Analysis</div>', unsafe_allow_html=True)

    prod_stats = df.groupby("NumOfProducts").agg(
        Customers=("Exited","count"), Churned=("Exited","sum")
    ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100,
             Retained=lambda x: x["Customers"]-x["Churned"]).reset_index()

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    opt_prod = prod_stats.loc[prod_stats["ChurnRate"].idxmin(), "NumOfProducts"] if len(prod_stats) else "N/A"
    single_prod = prod_stats[prod_stats["NumOfProducts"]==1]["ChurnRate"].values
    two_prod    = prod_stats[prod_stats["NumOfProducts"]==2]["ChurnRate"].values
    c1.metric("Single-product churn",  f"{single_prod[0]:.1f}%" if len(single_prod) else "N/A")
    c2.metric("Two-product churn",     f"{two_prod[0]:.1f}%"    if len(two_prod)    else "N/A")
    c3.metric("Optimal product count", str(opt_prod))
    cr_diff = (single_prod[0] - two_prod[0]) if (len(single_prod) and len(two_prod)) else 0
    c4.metric("Retention uplift (1→2)", f"{cr_diff:.1f}pp")

    st.markdown("<br>", unsafe_allow_html=True)

    col_bar, col_stack = st.columns(2)

    with col_bar:
        st.markdown("**Churn rate by number of products**")
        prod_colors = {1: COLORS["amber"], 2: COLORS["teal"], 3: COLORS["red_dark"], 4: COLORS["red"]}
        fig_prod = go.Figure()
        for _, row in prod_stats.iterrows():
            fig_prod.add_trace(go.Bar(
                x=[f"{int(row['NumOfProducts'])} product{'s' if row['NumOfProducts']>1 else ''}"],
                y=[row["ChurnRate"]],
                marker_color=prod_colors.get(int(row["NumOfProducts"]), COLORS["gray"]),
                text=f"{row['ChurnRate']:.1f}%",
                textposition="outside",
                name=str(int(row["NumOfProducts"])),
                customdata=[[row["Customers"], row["Churned"]]],
                hovertemplate="<b>%{x}</b><br>Churn: %{y:.1f}%<br>Customers: %{customdata[0]:,}<br>Churned: %{customdata[1]:,}<extra></extra>",
                showlegend=False,
            ))
        fig_prod.add_hline(y=churn_rate, line_dash="dash", line_color="#888", annotation_text=f"Avg {churn_rate:.1f}%", annotation_font_size=11)
        fig_prod.update_layout(
            height=300, paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0", range=[0, 115]),
            xaxis=dict(title=""),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    with col_stack:
        st.markdown("**Retained vs churned by product count**")
        if len(prod_stats) > 0:
            fig_stack = go.Figure()
            fig_stack.add_trace(go.Bar(
                name="Retained",
                x=[f"{int(p)} product{'s' if p>1 else ''}" for p in prod_stats["NumOfProducts"]],
                y=prod_stats["Retained"],
                marker_color=COLORS["teal"],
                hovertemplate="%{x}<br>Retained: %{y:,}<extra></extra>",
            ))
            fig_stack.add_trace(go.Bar(
                name="Churned",
                x=[f"{int(p)} product{'s' if p>1 else ''}" for p in prod_stats["NumOfProducts"]],
                y=prod_stats["Churned"],
                marker_color=COLORS["red"],
                hovertemplate="%{x}<br>Churned: %{y:,}<extra></extra>",
            ))
            fig_stack.update_layout(
                barmode="stack", height=300,
                paper_bgcolor="white", plot_bgcolor="white",
                margin=dict(t=20, b=10, l=0, r=0),
                yaxis=dict(title="Customers", gridcolor="#F0F0F0"),
                xaxis=dict(title=""),
                legend=dict(orientation="h", y=1.12, font=dict(size=11)),
                font=dict(family="Inter", size=12),
            )
            st.plotly_chart(fig_stack, use_container_width=True)

    # Product × Active heatmap
    st.markdown("**Product count × Activity status — churn rate heatmap**")
    heat_df = df.groupby(["NumOfProducts","IsActiveMember"]).agg(
        Customers=("Exited","count"), Churned=("Exited","sum")
    ).assign(ChurnRate=lambda x: (x["Churned"]/x["Customers"]*100).round(1)).reset_index()

    heat_pivot = heat_df.pivot(index="IsActiveMember", columns="NumOfProducts", values="ChurnRate")
    heat_pivot.index = ["Inactive", "Active"]

    fig_heat = px.imshow(heat_pivot,
        color_continuous_scale=[[0,"#0F6E56"],[0.3,"#BA7517"],[0.6,"#A32D2D"],[1,"#501313"]],
        text_auto=".1f",
        labels=dict(x="Number of Products", y="Membership Status", color="Churn %"),
        aspect="auto",
    )
    fig_heat.update_layout(
        height=220, paper_bgcolor="white",
        margin=dict(t=10, b=10, l=0, r=0),
        font=dict(family="Inter", size=13),
        coloraxis_colorbar=dict(title="Churn %", len=0.8),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # Balance × Products
    col_bp1, col_bp2 = st.columns(2)

    with col_bp1:
        st.markdown("**Churn by balance tier**")
        bal_stats = df.groupby("BalanceTier", observed=True).agg(
            Customers=("Exited","count"), Churned=("Exited","sum")
        ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100).reset_index()

        fig_bal = px.bar(bal_stats, x="BalanceTier", y="ChurnRate",
            color="ChurnRate",
            color_continuous_scale=[[0,"#0F6E56"],[0.5,"#BA7517"],[1,"#A32D2D"]],
            text=bal_stats["ChurnRate"].apply(lambda x: f"{x:.1f}%"),
        )
        fig_bal.update_traces(textposition="outside", marker_line_width=0)
        fig_bal.update_layout(
            height=260, paper_bgcolor="white", plot_bgcolor="white",
            coloraxis_showscale=False,
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0"),
            xaxis=dict(title="Balance Tier"),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_bal, use_container_width=True)

    with col_bp2:
        st.markdown("**Credit card ownership vs churn**")
        cc_stats = df.groupby("HasCrCard").agg(
            Customers=("Exited","count"), Churned=("Exited","sum")
        ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100).reset_index()
        cc_stats["Label"] = cc_stats["HasCrCard"].map({1: "Has Credit Card", 0: "No Credit Card"})

        fig_cc = px.bar(cc_stats, x="Label", y="ChurnRate",
            color="Label",
            color_discrete_map={"Has Credit Card": COLORS["blue"], "No Credit Card": COLORS["gray"]},
            text=cc_stats["ChurnRate"].apply(lambda x: f"{x:.1f}%"),
        )
        fig_cc.update_traces(textposition="outside", marker_line_width=0)
        fig_cc.update_layout(
            height=260, paper_bgcolor="white", plot_bgcolor="white",
            showlegend=False,
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0"),
            xaxis=dict(title=""),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_cc, use_container_width=True)

    st.markdown('<div class="insight-box warn"><b>⚠️ Non-linear product effect:</b> The 1→2 product transition delivers massive churn reduction (27.7% → 7.6%), but 3–4 products dramatically increase churn (82–100%). This signals over-selling: customers with 3–4 products likely feel overwhelmed or mis-sold, leading to exit. The optimal product strategy is a deliberate 2-product bundle.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: HIGH-VALUE DISENGAGED DETECTOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-hdr">High-Value Disengaged Customer Detector</div>', unsafe_allow_html=True)

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    with col_ctrl1:
        hv_balance_thresh = st.slider("Minimum balance threshold (€)", 0, 200_000, 100_000, step=5000)
    with col_ctrl2:
        hv_salary_thresh  = st.slider("Minimum salary threshold (€)", 0, 200_000, 50_000, step=5000)
    with col_ctrl3:
        hv_prod_max = st.slider("Max products (over-sold filter)", 1, 4, 4)

    hv_df = df[
        (df["Balance"] >= hv_balance_thresh) &
        (df["IsActiveMember"] == 0) &
        (df["EstimatedSalary"] >= hv_salary_thresh) &
        (df["NumOfProducts"] <= hv_prod_max)
    ]
    hv_retained = hv_df[hv_df["Exited"] == 0]
    hv_churned  = hv_df[hv_df["Exited"] == 1]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("At-risk segment",  f"{len(hv_df):,}",  "High-bal. inactive customers")
    c2.metric("Already churned",  f"{len(hv_churned):,}", f"{len(hv_churned)/len(hv_df)*100:.1f}% churn rate" if len(hv_df) else "0%")
    c3.metric("Still retained",   f"{len(hv_retained):,}", "Immediate rescue priority")
    c4.metric("Avg balance",      f"€{hv_df['Balance'].mean():,.0f}" if len(hv_df) else "N/A", "vs €0 for zero-balance")

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown("**At-risk premium customers — geography × churn status**")
        if len(hv_df) > 0:
            hv_geo = hv_df.groupby(["Geography","Exited"]).size().reset_index(name="Count")
            hv_geo["Status"] = hv_geo["Exited"].map({0:"Retained", 1:"Churned"})
            fig_hv_geo = px.bar(hv_geo, x="Geography", y="Count", color="Status",
                color_discrete_map={"Retained": COLORS["teal"], "Churned": COLORS["red"]},
                barmode="group",
                text="Count",
            )
            fig_hv_geo.update_traces(textposition="outside")
            fig_hv_geo.update_layout(
                height=300, paper_bgcolor="white", plot_bgcolor="white",
                margin=dict(t=20, b=10, l=0, r=0),
                yaxis=dict(title="Customers", gridcolor="#F0F0F0"),
                xaxis=dict(title=""),
                legend=dict(orientation="h", y=1.12, font=dict(size=11)),
                font=dict(family="Inter", size=12),
            )
            st.plotly_chart(fig_hv_geo, use_container_width=True)

    with col_r:
        st.markdown("**Risk breakdown by age group**")
        if len(hv_df) > 0:
            hv_age = hv_df.groupby("AgeBucket", observed=True).agg(
                Total=("Exited","count"), Churned=("Exited","sum")
            ).assign(Rate=lambda x: x["Churned"]/x["Total"]*100).reset_index()

            fig_hv_age = px.bar(hv_age, y="AgeBucket", x="Rate",
                orientation="h",
                color="Rate",
                color_continuous_scale=[[0,"#1D9E75"],[0.5,"#BA7517"],[1,"#A32D2D"]],
                text=hv_age["Rate"].apply(lambda x: f"{x:.1f}%"),
            )
            fig_hv_age.update_traces(textposition="outside")
            fig_hv_age.update_layout(
                height=300, paper_bgcolor="white", plot_bgcolor="white",
                coloraxis_showscale=False,
                margin=dict(t=20, b=10, l=40, r=30),
                xaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0"),
                yaxis=dict(title=""),
                font=dict(family="Inter", size=12),
            )
            st.plotly_chart(fig_hv_age, use_container_width=True)

    # Scatter: Balance vs Salary colored by churn
    st.markdown("**Balance vs salary — high-value inactive customers (colored by churn status)**")
    if len(hv_df) > 0:
        scatter_df = hv_df.copy()
        scatter_df["Status"] = scatter_df["Exited"].map({0: "Retained", 1: "Churned"})
        scatter_df["RSI_disp"] = scatter_df["RSI"].round(0)

        fig_scatter = px.scatter(
            scatter_df.sample(min(len(scatter_df), 800), random_state=42),
            x="EstimatedSalary", y="Balance",
            color="Status",
            color_discrete_map={"Retained": COLORS["teal"], "Churned": COLORS["red"]},
            size="RSI_disp", size_max=14,
            hover_data={"Geography": True, "Age": True, "NumOfProducts": True, "RSI_disp": True},
            opacity=0.7,
            labels={"EstimatedSalary": "Estimated Salary (€)", "Balance": "Account Balance (€)"},
        )
        fig_scatter.update_layout(
            height=360, paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(t=20, b=10, l=0, r=0),
            legend=dict(orientation="h", y=1.06, font=dict(size=11)),
            font=dict(family="Inter", size=12),
            xaxis=dict(gridcolor="#F0F0F0"),
            yaxis=dict(gridcolor="#F0F0F0"),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Customer table
    st.markdown("**🔴 Priority rescue list — retained high-value inactive customers**")
    if len(hv_retained) > 0:
        display_cols = ["CustomerId","Geography","Gender","Age","Balance","EstimatedSalary","NumOfProducts","Tenure","CreditScore","RSI"]
        rescue_df = hv_retained[display_cols].sort_values("Balance", ascending=False).head(20).copy()
        rescue_df["Balance"] = rescue_df["Balance"].apply(lambda x: f"€{x:,.0f}")
        rescue_df["EstimatedSalary"] = rescue_df["EstimatedSalary"].apply(lambda x: f"€{x:,.0f}")
        rescue_df["RSI"] = rescue_df["RSI"].round(0).astype(int)
        st.dataframe(rescue_df, use_container_width=True, hide_index=True)
        st.caption(f"Showing top 20 of {len(hv_retained):,} retained high-value inactive customers, sorted by balance. Prioritize for immediate relationship manager outreach.")
    else:
        st.info("No customers match the current filter criteria. Adjust the sliders above.")

    if len(hv_df) > 0:
        hv_rate = len(hv_churned)/len(hv_df)*100
        st.markdown(f'<div class="insight-box danger"><b>🚨 Silent premium churn alert:</b> {len(hv_df):,} customers meet the high-value + inactive criteria. Of these, {len(hv_churned):,} have already exited ({hv_rate:.1f}% churn rate vs {churn_rate:.1f}% average). The {len(hv_retained):,} still retained represent high-value relationships at elevated risk — assign dedicated relationship managers immediately.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: RETENTION STRENGTH SCORING
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-hdr">Retention Strength Scoring — Relationship Strength Index (RSI)</div>', unsafe_allow_html=True)

    # RSI explanation
    with st.expander("📐 RSI Formula & Methodology", expanded=False):
        st.markdown("""
        **Relationship Strength Index (RSI)** is a composite behavioral score (0–120) capturing four dimensions:

        | Dimension | Weight | Rationale |
        |---|---|---|
        | **IsActiveMember** | ×40 pts | Strongest single retention signal |
        | **NumOfProducts** (capped at 2) | ×20 pts | Optimal range is 1–2; 3+ signals over-selling |
        | **HasCrCard** | ×10 pts | Moderate stickiness indicator |
        | **Tenure** (capped at 10 yrs) | ×3 pts | Relationship depth proxy |

        **RSI Tiers:** Low < 50 · Medium 50–79 · High ≥ 80
        """)

    rsi_stats = df.groupby("RSI_Tier", observed=True).agg(
        Customers=("Exited","count"), Churned=("Exited","sum")
    ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100).reset_index()

    # KPI Row
    c1, c2, c3 = st.columns(3)
    for i, (_, row) in enumerate(rsi_stats.iterrows()):
        cols = [c1, c2, c3]
        cols[i].metric(
            str(row["RSI_Tier"]),
            f"{row['ChurnRate']:.1f}% churn",
            f"{row['Customers']:,} customers"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown("**RSI distribution — retained vs churned customers**")
        fig_rsi_hist = go.Figure()
        fig_rsi_hist.add_trace(go.Histogram(
            x=df[df["Exited"]==0]["RSI"], name="Retained",
            marker_color=COLORS["teal"], opacity=0.75,
            nbinsx=20,
            hovertemplate="RSI: %{x}<br>Count: %{y:,}<extra>Retained</extra>",
        ))
        fig_rsi_hist.add_trace(go.Histogram(
            x=df[df["Exited"]==1]["RSI"], name="Churned",
            marker_color=COLORS["red"], opacity=0.75,
            nbinsx=20,
            hovertemplate="RSI: %{x}<br>Count: %{y:,}<extra>Churned</extra>",
        ))
        fig_rsi_hist.update_layout(
            barmode="overlay", height=300,
            paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(t=20, b=10, l=0, r=0),
            xaxis=dict(title="RSI Score", gridcolor="#F0F0F0"),
            yaxis=dict(title="Customer Count", gridcolor="#F0F0F0"),
            legend=dict(orientation="h", y=1.1, font=dict(size=11)),
            font=dict(family="Inter", size=12),
        )
        fig_rsi_hist.add_vline(x=50, line_dash="dash", line_color=COLORS["amber"], annotation_text="Low/Medium boundary", annotation_font_size=10)
        fig_rsi_hist.add_vline(x=80, line_dash="dash", line_color=COLORS["teal"], annotation_text="High boundary", annotation_font_size=10)
        st.plotly_chart(fig_rsi_hist, use_container_width=True)

    with col_r:
        st.markdown("**Churn rate by RSI tier**")
        rsi_colors = {"Low (RSI < 50)": COLORS["red"], "Medium (50–79)": COLORS["amber"], "High (RSI ≥ 80)": COLORS["teal"]}
        fig_rsi_bar = go.Figure()
        for _, row in rsi_stats.iterrows():
            fig_rsi_bar.add_trace(go.Bar(
                x=[str(row["RSI_Tier"])],
                y=[row["ChurnRate"]],
                marker_color=rsi_colors.get(str(row["RSI_Tier"]), COLORS["gray"]),
                text=f"{row['ChurnRate']:.1f}%",
                textposition="outside",
                name=str(row["RSI_Tier"]),
                customdata=[[row["Customers"], row["Churned"]]],
                hovertemplate="%{x}<br>Churn: %{y:.1f}%<br>Customers: %{customdata[0]:,}<extra></extra>",
                showlegend=False,
            ))
        fig_rsi_bar.update_layout(
            height=300, paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(t=20, b=10, l=0, r=0),
            yaxis=dict(title="Churn Rate (%)", gridcolor="#F0F0F0", range=[0, rsi_stats["ChurnRate"].max()*1.25 if len(rsi_stats) else 50]),
            xaxis=dict(title=""),
            font=dict(family="Inter", size=12),
        )
        st.plotly_chart(fig_rsi_bar, use_container_width=True)

    # RSI × Geography
    st.markdown("**RSI tier distribution by geography**")
    rsi_geo = df.groupby(["Geography","RSI_Tier"], observed=True).agg(
        Customers=("Exited","count"), Churned=("Exited","sum")
    ).assign(ChurnRate=lambda x: x["Churned"]/x["Customers"]*100).reset_index()

    fig_rsi_geo = px.bar(rsi_geo, x="Geography", y="Customers",
        color="RSI_Tier",
        color_discrete_map={
            "Low (RSI < 50)": COLORS["red"],
            "Medium (50–79)": COLORS["amber"],
            "High (RSI ≥ 80)": COLORS["teal"],
        },
        barmode="stack",
        text="Customers",
    )
    fig_rsi_geo.update_traces(texttemplate="%{text:,}", textposition="inside")
    fig_rsi_geo.update_layout(
        height=300, paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(t=20, b=10, l=0, r=0),
        yaxis=dict(title="Customers", gridcolor="#F0F0F0"),
        xaxis=dict(title=""),
        legend=dict(title="RSI Tier", orientation="h", y=1.12, font=dict(size=11)),
        font=dict(family="Inter", size=12),
    )
    st.plotly_chart(fig_rsi_geo, use_container_width=True)

    # Sticky customer profile
    st.markdown("**🟢 'Sticky customer' profile analysis**")
    sticky_df = df[df["RSI"] >= 80]
    not_sticky = df[df["RSI"] < 50]

    if len(sticky_df) > 0 and len(not_sticky) > 0:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("*High RSI (≥80) — sticky customers*")
            profile_data = {
                "Metric": ["Churn Rate", "Avg Balance", "Avg Tenure", "% Active", "% With Credit Card"],
                "Sticky (RSI≥80)": [
                    f"{sticky_df['Exited'].mean()*100:.1f}%",
                    f"€{sticky_df['Balance'].mean():,.0f}",
                    f"{sticky_df['Tenure'].mean():.1f} yrs",
                    f"{sticky_df['IsActiveMember'].mean()*100:.0f}%",
                    f"{sticky_df['HasCrCard'].mean()*100:.0f}%",
                ],
                "At-Risk (RSI<50)": [
                    f"{not_sticky['Exited'].mean()*100:.1f}%",
                    f"€{not_sticky['Balance'].mean():,.0f}",
                    f"{not_sticky['Tenure'].mean():.1f} yrs",
                    f"{not_sticky['IsActiveMember'].mean()*100:.0f}%",
                    f"{not_sticky['HasCrCard'].mean()*100:.0f}%",
                ],
            }
            st.dataframe(pd.DataFrame(profile_data), use_container_width=True, hide_index=True)

        with col_s2:
            st.markdown("*RSI score composition*")
            rsi_components = df.groupby("RSI_Tier", observed=True).agg(
                Avg_Activity=("IsActiveMember","mean"),
                Avg_Products=("NumOfProducts","mean"),
                Avg_CrCard=("HasCrCard","mean"),
                Avg_Tenure=("Tenure","mean"),
            ).reset_index()

            fig_radar = go.Figure()
            categories = ["Activity Score", "Product Score", "Card Score", "Tenure Score"]
            tier_styles = {
                "Low (RSI < 50)":  (COLORS["red"],   "solid"),
                "Medium (50–79)":  (COLORS["amber"],  "dash"),
                "High (RSI ≥ 80)": (COLORS["teal"],  "solid"),
            }
            for _, row in rsi_components.iterrows():
                tier = str(row["RSI_Tier"])
                color, dash = tier_styles.get(tier, (COLORS["gray"], "solid"))
                vals = [
                    row["Avg_Activity"]*100,
                    min(row["Avg_Products"]/2,1)*100,
                    row["Avg_CrCard"]*100,
                    min(row["Avg_Tenure"]/10,1)*100,
                ]
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=categories + [categories[0]],
                    fill="toself" if tier=="High (RSI ≥ 80)" else "none",
                    fillcolor=f"rgba({','.join(str(int(color.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.1)" if tier=="High (RSI ≥ 80)" else "rgba(0,0,0,0)",
                    line=dict(color=color, dash=dash, width=2),
                    name=tier,
                ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0,100], ticksuffix="%", gridcolor="#E0E0E0")),
                height=280, paper_bgcolor="white",
                margin=dict(t=30, b=10, l=0, r=0),
                legend=dict(font=dict(size=10), orientation="h", y=-0.1),
                font=dict(family="Inter", size=11),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    rsi_low_rate  = rsi_stats[rsi_stats["RSI_Tier"]=="Low (RSI < 50)"]["ChurnRate"].values
    rsi_high_rate = rsi_stats[rsi_stats["RSI_Tier"]=="High (RSI ≥ 80)"]["ChurnRate"].values
    if len(rsi_low_rate) and len(rsi_high_rate):
        st.markdown(f'<div class="insight-box good"><b>✅ RSI validates the behavioral framework:</b> High RSI customers churn at just {rsi_high_rate[0]:.1f}% vs {rsi_low_rate[0]:.1f}% for Low RSI — a {rsi_low_rate[0]/rsi_high_rate[0]:.1f}× retention multiplier. The composite score effectively identifies customers at risk before they churn, enabling proactive intervention.</div>', unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">European Central Bank · Customer Engagement & Product Utilization Analytics for Retention Strategy · 2025 · All filters applied dynamically</div>', unsafe_allow_html=True)
