
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(initial_sidebar_state="expanded")
# ─── Page config ─────────────────────────────────────────────────
st.set_page_config(
    page_title="AI PersonaMatch — Syria FMCG Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #1a2744; }
[data-testid="stSidebarContent"] { color: white; }
#MainMenu, footer, header { visibility: hidden; }

/* Hide the collapse button — sidebar always stays open */
[data-testid="stSidebarHeader"] button { display: none !important; }
[data-testid="collapsedControl"] {
    background: #1a2744 !important;
    border: 2px solid #4fc3f7 !important;
    border-radius: 0 12px 12px 0 !important;
    min-height: 100px !important;
    min-width: 28px !important;
}
[data-testid="collapsedControl"] svg { color: #4fc3f7 !important; }
.main-title {
    font-size: 2rem; font-weight: 700;
    color: #1F4E79; margin-bottom: 2px;
}
.sub-title {
    font-size: 0.95rem; color: #546E7A; margin-bottom: 24px;
}
.kpi-card {
    background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
    border-radius: 12px; padding: 20px 14px;
    text-align: center; color: white;
}
.kpi-num {
    font-size: 2rem; font-weight: 700; color: #DEEAF1;
}
.kpi-lbl {
    font-size: 0.78rem; color: #BDD7EE; margin-top: 4px;
}
.insight {
    background: #DEEAF1; border-left: 4px solid #2E75B6;
    border-radius: 0 8px 8px 0; padding: 10px 14px;
    font-size: 0.88rem; color: #1F4E79; margin: 6px 0;
}
.finding {
    background: #E8F5E9; border-left: 4px solid #2E7D32;
    border-radius: 0 8px 8px 0; padding: 10px 14px;
    font-size: 0.88rem; color: #1B5E20; margin: 6px 0;
}
.warning {
    background: #FDECEA; border-left: 4px solid #C62828;
    border-radius: 0 8px 8px 0; padding: 10px 14px;
    font-size: 0.88rem; color: #B71C1C; margin: 6px 0;
}
.rec-card {
    background: #F8F9FA; border: 1px solid #DEE2E6;
    border-radius: 10px; padding: 16px; margin: 8px 0;
}
.nav-btn {
    background: transparent; border: none; width: 100%;
    text-align: left; padding: 8px 12px; color: white;
    border-radius: 8px; cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ─── Users ───────────────────────────────────────────────────────
USERS = {
    "admin":    {"password": "admin123",   "name": "Administrator",     "role": "Admin"},
    "company1": {"password": "company123", "name": "FMCG Company User", "role": "Company"},
    "analyst":  {"password": "analyst123", "name": "Market Analyst",    "role": "Analyst"},
}

# ─── Login ───────────────────────────────────────────────────────
def login_page():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white; border-radius:16px; padding:40px 32px;
             box-shadow:0 4px 24px rgba(0,0,0,0.08); text-align:center;">
            <div style="font-size:3.5rem; margin-bottom:12px;">🎯</div>
            <h2 style="color:#1F4E79; margin:0 0 4px;">AI PersonaMatch</h2>
            <p style="color:#546E7A; font-size:0.9rem; margin:0 0 6px;">
                Syria FMCG Consumer Intelligence Platform
            </p>
            <p style="color:#90A4AE; font-size:0.8rem; margin:0;">
                Precision Demand Forecasting · Consumer-Centric Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit   = st.form_submit_button("Sign In", use_container_width=True, type="primary")

            if submit:
                if username in USERS and USERS[username]["password"] == password:
                    st.session_state["logged_in"]  = True
                    st.session_state["username"]   = username
                    st.session_state["user_name"]  = USERS[username]["name"]
                    st.session_state["user_role"]  = USERS[username]["role"]
                    st.session_state["page"]       = "Home"
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        st.markdown("""
        <div style="text-align:center; margin-top:16px; padding:12px;
             background:#F8F9FA; border-radius:8px; font-size:0.78rem; color:#888;">
            Demo credentials:<br>
            <b>admin</b> / admin123 &nbsp;·&nbsp;
            <b>company1</b> / company123 &nbsp;·&nbsp;
            <b>analyst</b> / analyst123
        </div>
        """, unsafe_allow_html=True)

# ─── Data loading ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    base  = "data/"
    files = {
        "segments":         "syria_consumer_segments.csv",
        "scores":           "syria_market_entry_scores.csv",
        "affordability":    "syria_affordability_index.csv",
        "income_share":     "syria_income_share.csv",
        "wtp":              "syria_wtp_thresholds.csv",
        "bread":            "syria_bread_affordability_gap.csv",
        "volatility":       "syria_regional_volatility.csv",
        "forecast_basket":  "forecast_basket_cost.csv",
        "forecast_afford":  "forecast_affordability.csv",
        "forecast_tartous": "forecast_tartous.csv",
        "forecast_hama":    "forecast_hama.csv",
        "forecast_aleppo":  "forecast_aleppo.csv",
    }
    data = {}
    for key, fname in files.items():
        path = base + fname
        if os.path.exists(path):
            df = pd.read_csv(path)
            for col in ["date", "ds"]:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col])
            data[key] = df
        else:
            data[key] = pd.DataFrame()
    return data

# ─── Sidebar ─────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:24px 10px 16px;">
            <div style="font-size:2.5rem;">🎯</div>
            <div style="color:white; font-size:1.05rem; font-weight:600; margin-top:8px;">
                AI PersonaMatch
            </div>
            <div style="color:#90CAF9; font-size:0.72rem; margin-top:4px;">
                Syria FMCG Intelligence
            </div>
        </div>
        <div style="background:#243b5e; border-radius:8px; padding:10px 12px; margin:0 8px 16px;">
            <div style="color:#90CAF9; font-size:0.72rem;">Signed in as</div>
            <div style="color:white; font-weight:500; font-size:0.9rem; margin-top:2px;">
                {st.session_state.get("user_name", "User")}
            </div>
            <div style="color:#64B5F6; font-size:0.72rem;">
                {st.session_state.get("user_role", "")}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Role badge
        role = st.session_state.get("user_role", "")
        role_color = {"Admin": "#C62828", "Company": "#2E7D32", "Analyst": "#1F4E79"}.get(role, "#888")
        st.markdown(f"""
        <div style="text-align:center; margin:8px 8px 0;">
            <span style="background:{role_color}; color:white; font-size:0.72rem;
                 padding:3px 12px; border-radius:999px; font-weight:500;">
                {role} Access
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚪  Sign Out", use_container_width=True):
            for key in ["logged_in","username","user_name","user_role","page"]:
                st.session_state.pop(key, None)
            st.rerun()

        st.markdown("""
        <div style="text-align:center; color:#546E7A; font-size:0.68rem;
             padding:12px 8px; margin-top:8px; line-height:1.7;">
            Source: WFP Food Price Database<br>
            Syria · Apr 2011 — Jun 2021<br>
            14 Governorates · 116,588 records
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────────

COLORS = {
    "Viable coastal & admin markets"  : "#2E7D32",
    "Stressed interior markets"       : "#E65100",
    "Fragmented major urban centers"  : "#C62828",
}
CUTOFF = pd.Timestamp("2021-06-01")

# ── Home ──────────────────────────────────────────────────────────
def page_home(data):
    st.markdown("<h1 class=\"main-title\">🎯  AI PersonaMatch</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class=\"sub-title\">Syria FMCG Consumer Intelligence Platform — "
        "Precision Demand Forecasting & Consumer-Centric Analytics</p>",
        unsafe_allow_html=True
    )

    # KPI strip
    kpis = [
        ("116,588", "Price observations"),
        ("14",      "Governorates"),
        ("124",     "Months of data"),
        ("96",      "Market locations"),
        ("35",      "FMCG products"),
    ]
    cols = st.columns(5)
    for col, (num, lbl) in zip(cols, kpis):
        with col:
            st.markdown(
                f"<div class=\"kpi-card\">"
                f"<div class=\"kpi-num\">{num}</div>"
                f"<div class=\"kpi-lbl\">{lbl}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; justify-content:flex-end; margin-bottom:8px;">
        <span style="background:#1a2744; color:#90CAF9; font-size:0.75rem;
             padding:4px 14px; border-radius:999px; border:1px solid #2d4a7a;">
            📅  Data last updated: June 2021 · Source: WFP Food Price Database
        </span>
    </div>
    """, unsafe_allow_html=True)
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("### What this platform does")
        st.markdown("""
        <div class="insight">
            <b>AI PersonaMatch</b> answers the core business question for Syria's
            reconstruction market: <b>Who buys what, where, and when?</b>
        </div>
        <div class="insight">
            It transforms WFP humanitarian monitoring data into commercial consumer
            intelligence — the only structured, data-driven FMCG analytics tool
            built specifically for the Syrian market.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Five analytical modules")
        modules = [
            ("A", "Consumer Segmentation",  "K-Means ML → 3 distinct consumer profiles"),
            ("B", "Geographic Demand Maps", "Interactive Syria choropleth maps"),
            ("C", "Price Sensitivity",      "WTP thresholds & income share analysis"),
            ("D", "Demand Forecasting",     "Prophet AI → 12-month projections"),
            ("E", "Market Entry Scoring",   "Composite ranking of all 14 governorates"),
        ]
        for letter, name, desc in modules:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:8px 10px;
                 margin:4px 0; background:#F8F9FA; border-radius:8px;">
                <div style="background:#1F4E79; color:white; width:28px; height:28px;
                     border-radius:50%; display:flex; align-items:center;
                     justify-content:center; font-weight:700; font-size:0.82rem;
                     flex-shrink:0;">{letter}</div>
                <div>
                    <div style="font-weight:600; color:#1F4E79; font-size:0.88rem;">{name}</div>
                    <div style="color:#666; font-size:0.78rem;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown("### Key findings")
        findings = [
            ("🏆", "Tartous ranks #1 (84.9/100)",
             "Highest purchasing power and price stability in Syria"),
            ("📍", "3 distinct consumer segments",
             "Coastal viable, stressed interior, fragmented urban"),
            ("💸", "67.4% of region-months are food insecure",
             "Households cannot afford the basic food basket"),
            ("🍞", "Idleb crisis detected",
             "Actual bread price is 4× above what households can afford"),
            ("📈", "Basket cost projected to 1.2M SYP",
             "By March 2022 — Prophet AI detected structural price break"),
            ("🌙", "Ramadan seasonal signal found",
             "Prophet detected shifting annual demand peaks from price data"),
        ]
        for icon, title, desc in findings:
            st.markdown(f"""
            <div class="finding">
                <b>{icon}  {title}</b><br>
                <span style="font-size:0.82rem;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Market entry quick view")
    if not data["scores"].empty:
        sc = data["scores"].sort_values("rank")
        fig = go.Figure(go.Bar(
            x=sc["composite_score"], y=sc["adm1_name"], orientation="h",
            marker_color=[COLORS.get(s, "#888") for s in sc["segment_name"]],
            text=sc["composite_score"].round(1), textposition="outside",
        ))
        fig.update_layout(
            height=420, xaxis=dict(title="Composite Score (0–100)", range=[0, 115]),
            yaxis=dict(autorange="reversed"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=70, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Consumer Profiles ─────────────────────────────────────────────
def page_consumer_profiles(data):
    st.markdown("## 👤  Consumer Profiles")
    st.markdown("*K-Means machine learning identified 3 natural consumer segments across Syria's 14 governorates*")

    if data["segments"].empty:
        st.error("Segments data not found in data/ folder.")
        return

    segs = data["segments"]

    seg_info = {
        "Viable coastal & admin markets": {
            "icon": "🟢", "color": "#2E7D32",
            "desc": "The most commercially attractive segment. Households consistently earn above the food basket cost threshold. Coastal access provides supply chain advantages.",
            "strategy": "Immediate market entry. Full product range. Standard market pricing.",
        },
        "Stressed interior markets": {
            "icon": "🟠", "color": "#E65100",
            "desc": "The largest segment — 9 governorates covering most of Syria's geographic area. Households generally below the affordability threshold. Viable with adjusted pricing.",
            "strategy": "Entry viable with competitive pricing. Focus on high-volume staples.",
        },
        "Fragmented major urban centers": {
            "icon": "🔴", "color": "#C62828",
            "desc": "High price volatility from dual official/parallel market systems. Large populations but complex, unpredictable operating environment.",
            "strategy": "Secondary entry after coastal establishment. Requires dual-market strategy.",
        },
    }

    for seg_name, info in seg_info.items():
        subset = segs[segs["segment_name"] == seg_name]
        govs   = ", ".join(subset["adm1_name"].tolist())
        with st.expander(
            f"{info['icon']}  {seg_name}  —  {len(subset)} governorates",
            expanded=True
        ):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**About this segment:** {info['desc']}")
                st.markdown(f"**Recommended strategy:** {info['strategy']}")
                st.markdown(f"**Governorates:** {govs}")
            with c2:
                if not subset.empty:
                    avg_a = subset["avg_affordability"].mean()
                    avg_v = subset["volatility_index"].mean()
                    st.metric("Avg Affordability",
                              f"{avg_a:.3f}",
                              delta="Above threshold ✓" if avg_a >= 1.0 else "Below threshold")
                    st.metric("Avg Price Volatility", f"{avg_v:.1f}%")

    st.markdown("---")
    st.markdown("### Segment positioning — Volatility vs Affordability")
    fig = px.scatter(
        segs,
        x="volatility_index", y="avg_affordability",
        color="segment_name", text="adm1_name",
        size="avg_basket_cost",
        color_discrete_map=COLORS,
        labels={
            "volatility_index"  : "Price Volatility Index (CoV %)",
            "avg_affordability" : "Average Affordability Index",
            "segment_name"      : "Segment",
        },
        title="Consumer Segment Map — each bubble is one Syrian governorate",
    )
    fig.add_hline(y=1.0, line_dash="dash", line_color="gray",
                  annotation_text="Affordability threshold (1.0)")
    fig.update_traces(textposition="top center")
    fig.update_layout(height=480, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ── Geographic Maps ───────────────────────────────────────────────
def page_geographic_maps(data):
    st.markdown("## 🗺️  Geographic Intelligence")
    st.markdown("*Three interactive maps — hover over any governorate for detailed analytics*")

    tab1, tab2, tab3 = st.tabs([
        "🟢🟠🔴  Consumer Segments",
        "💚  Affordability Heatmap",
        "🔴  Price Volatility Risk",
    ])

    def load_map(filename, tab, description):
        with tab:
            st.markdown(description, unsafe_allow_html=True)
            path = f"data/maps/{filename}"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    st.components.v1.html(f.read(), height=560, scrolling=False)
            else:
                st.warning(f"Map file `{filename}` not found in `data/maps/`. "
                           "Please copy your HTML map files to this folder.")

    load_map("map_consumer_segments.html", tab1, """
        <div class="insight">
            🟢 <b>Green</b> = Viable coastal markets — Tartous, Lattakia, City Damascus<br>
            🟠 <b>Orange</b> = Stressed interior markets — 9 governorates<br>
            🔴 <b>Red/Dark</b> = Fragmented urban centers — Damascus, Aleppo
        </div>
    """)
    load_map("map_affordability.html", tab2, """
        <div class="insight">
            Color gradient: deep red (severe food insecurity) → yellow (near threshold) → green (above 1.0).<br>
            The 1.0 threshold means monthly income equals monthly basket cost.
        </div>
    """)
    load_map("map_volatility.html", tab3, """
        <div class="insight">
            Darker red = more unstable prices = higher business operating risk.<br>
            Damascus (95% CoV) and Aleppo (72% CoV) are the most volatile markets nationally.
        </div>
    """)

    st.markdown("---")
    st.markdown("### Full geographic summary")
    if not data["segments"].empty:
        disp = data["segments"][[
            "adm1_name","segment_name","avg_affordability",
            "volatility_index","avg_basket_cost"
        ]].copy()
        disp.columns = ["Governorate","Segment","Avg Affordability",
                        "Volatility (%)","Avg Basket Cost (SYP)"]
        disp["Avg Affordability"]      = disp["Avg Affordability"].round(3)
        disp["Volatility (%)"]         = disp["Volatility (%)"].round(1)
        disp["Avg Basket Cost (SYP)"]  = disp["Avg Basket Cost (SYP)"].apply(lambda x: f"{x:,.0f}")
        st.dataframe(disp.sort_values("Avg Affordability", ascending=False),
                     use_container_width=True, hide_index=True)

# ── Price Intelligence ────────────────────────────────────────────
def page_price_intelligence(data):
    st.markdown("## 💰  Price Intelligence")
    st.markdown("*Income share burden, willingness-to-pay thresholds, and market price accessibility*")

    tab1, tab2, tab3 = st.tabs([
        "📊  Income Share per Product",
        "🎯  WTP Calculator",
        "🍞  Bread Affordability Gap",
    ])

    # ── Tab 1 ─────────────────────────────────────────────────────
    with tab1:
        if data["income_share"].empty:
            st.info("income_share data not found.")
        else:
            df = data["income_share"].head(15).copy()
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df["cm_name"],
                y=df["avg_share"],
                marker_color=["#C62828" if v > 20 else "#2E75B6" for v in df["avg_share"]],
                error_y=dict(
                    type="data", symmetric=False,
                    array=df["max_share"] - df["avg_share"],
                    arrayminus=df["avg_share"] - df["min_share"],
                ),
            ))
            fig.add_hline(y=20, line_dash="dash", line_color="red",
                          annotation_text="20% stress threshold")
            fig.update_layout(
                title="% of monthly household income consumed by each FMCG product",
                xaxis_tickangle=-45, height=480,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""
            <div class="insight">
                Products whose bar crosses the red 20% line create financial stress —
                they crowd out spending on rent, medicine, and education.
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2 ─────────────────────────────────────────────────────
    with tab2:
        if data["wtp"].empty:
            st.info("WTP data not found.")
        else:
            wtp = data["wtp"]
            c1, c2 = st.columns(2)
            with c1:
                gov = st.selectbox("Select Governorate",
                                   sorted(wtp["adm1_name"].unique()), key="wtp_gov")
            with c2:
                com = st.selectbox("Select Commodity",
                                   sorted(wtp["commodity"].unique()), key="wtp_com")

            row = wtp[(wtp["adm1_name"]==gov) & (wtp["commodity"]==com)]
            if not row.empty:
                r = row.iloc[0]
                ca, cb, cc = st.columns(3)
                ca.metric("Monthly Income (SYP)", f"{r['monthly_income']:,.0f}")
                cb.metric("20% Budget (SYP)",     f"{r['max_budget_syp']:,.0f}")
                cc.metric("WTP Ceiling / unit",   f"{r['wtp_ceiling_syp']:,.1f} SYP")

                st.markdown(f"""
                <div class="finding">
                    A household in <b>{gov}</b> can pay up to
                    <b>{r['wtp_ceiling_syp']:,.1f} SYP</b> per unit of
                    <b>{com.replace(" - Retail","")}</b>
                    before that product consumes more than 20% of their monthly income
                    ({r['monthly_income']:,.0f} SYP/month).
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### WTP ceiling across all governorates")
            wtp_com = wtp[wtp["commodity"]==com].sort_values("wtp_ceiling_syp", ascending=False)
            if not data["scores"].empty:
                wtp_com = wtp_com.merge(
                    data["scores"][["adm1_name","segment_name"]], on="adm1_name", how="left"
                )
            fig2 = px.bar(
                wtp_com, x="adm1_name", y="wtp_ceiling_syp",
                color="segment_name" if "segment_name" in wtp_com.columns else None,
                color_discrete_map=COLORS,
                labels={"wtp_ceiling_syp": "Max Price (SYP)", "adm1_name": "Governorate"},
                title=f"WTP Ceiling — {com.replace(' - Retail','')}",
            )
            fig2.update_layout(xaxis_tickangle=-45, height=380,
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 3 ─────────────────────────────────────────────────────
    with tab3:
        if data["bread"].empty:
            st.info("Bread comparison data not found.")
        else:
            bread = data["bread"].sort_values("wtp_ceiling_syp", ascending=False)
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(
                name="WTP ceiling (max affordable)", x=bread["adm1_name"],
                y=bread["wtp_ceiling_syp"], marker_color="#2E7D32",
            ))
            fig3.add_trace(go.Bar(
                name="Actual market price", x=bread["adm1_name"],
                y=bread["actual_price_syp"], marker_color="#C62828",
            ))
            fig3.update_layout(
                barmode="group",
                title="Bread — WTP Ceiling vs Actual Price per Governorate (June 2021)",
                xaxis_tickangle=-45, height=460,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig3, use_container_width=True)

            ok  = (bread["price_gap"] <= 0).sum()
            bad = len(bread) - ok
            st.markdown(f"""
            <div class="finding">
                <b>{ok} of {len(bread)} governorates</b>: bread price is within the
                household WTP ceiling — market is financially accessible.
            </div>
            <div class="warning">
                <b>{bad} governorates</b>: actual prices exceed what households can afford.
                Idleb: 4× over ceiling. Aleppo: 2× over ceiling.
            </div>
            """, unsafe_allow_html=True)

# ── Forecasting ───────────────────────────────────────────────────
def page_forecasting(data):
    st.markdown("## 📈  Demand Forecasting")
    st.markdown("*Prophet AI time series model — trained on 124 months of historical data, projecting 12 months forward*")

    tab1, tab2, tab3 = st.tabs([
        "🛒  Basket Cost Forecast",
        "💸  Affordability Forecast",
        "📍  Segment Forecasts",
    ])

    def forecast_chart(fc, title, y_label, color, threshold=None):
        if fc.empty:
            st.info("Forecast data not found.")
            return
        hist = fc[fc["ds"] <= CUTOFF]
        fut  = fc[fc["ds"] >  CUTOFF]
        fig  = go.Figure()

        fig.add_trace(go.Scatter(
            x=pd.concat([fut["ds"], fut["ds"][::-1]]),
            y=pd.concat([fut["yhat_upper"], fut["yhat_lower"][::-1]]),
            fill="toself", fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(color)) + [40])}",
            line=dict(color="rgba(0,0,0,0)"), name="80% confidence interval",
        ))
        fig.add_trace(go.Scatter(
            x=hist["ds"], y=hist["yhat"], mode="lines",
            name="Historical (model fit)", line=dict(color="#1F4E79", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=fut["ds"], y=fut["yhat"], mode="lines",
            name="12-month forecast", line=dict(color=color, width=2.5, dash="dash"),
        ))
        if threshold is not None:
            fig.add_shape(type="line", x0=0, x1=1, xref="paper",
                          y0=threshold, y1=threshold,
                          line=dict(dash="dash", color="green", width=1.5))
            fig.add_annotation(x=0.01, xref="paper", y=threshold,
                               text=f"Threshold ({threshold})", showarrow=False,
                               xanchor="left", yanchor="bottom",
                               font=dict(color="green", size=11))
        fig.add_shape(type="line", x0="2021-06-01", x1="2021-06-01",
                      y0=0, y1=1, yref="paper",
                      line=dict(dash="dot", color="gray", width=1.5))
        fig.add_annotation(x="2021-06-01", y=0.96, yref="paper",
                           text="Forecast begins", showarrow=False,
                           xanchor="left", font=dict(color="gray", size=11))
        fig.update_layout(
            title=title, xaxis_title="Date", yaxis_title=y_label,
            height=480, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Forecast table
        if not fut.empty:
            t = fut[["ds","yhat","yhat_lower","yhat_upper"]].copy()
            t.columns = ["Month","Forecast","Lower Bound","Upper Bound"]
            t["Month"] = t["Month"].dt.strftime("%B %Y")
            for c in ["Forecast","Lower Bound","Upper Bound"]:
                t[c] = t[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(t, use_container_width=True, hide_index=True)

    with tab1:
        forecast_chart(data["forecast_basket"],
                       "National Monthly Food Basket Cost — Historical + 12-Month Forecast (SYP)",
                       "Monthly Basket Cost (SYP)", "#E65100")

    with tab2:
        forecast_chart(data["forecast_afford"],
                       "National Affordability Index — Historical + 12-Month Forecast",
                       "Affordability Index", "#C62828", threshold=1.0)
        st.markdown("""
        <div class="warning">
            <b>Critical projection:</b> The model forecasts the national affordability index
            falling below 0.0 by early 2022, indicating basket costs will exceed household
            income by a factor of 2× or more — consistent with WFP's 2021 Syria
            food security crisis reports.
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("*One representative governorate per consumer segment*")
        fig3 = go.Figure()
        govs = {
            "Tartous": ("#2E7D32", data["forecast_tartous"]),
            "Hama"   : ("#E65100", data["forecast_hama"]),
            "Aleppo" : ("#C62828", data["forecast_aleppo"]),
        }
        for gov, (color, fc) in govs.items():
            if fc.empty: continue
            hist = fc[fc["ds"] <= CUTOFF]
            fut  = fc[fc["ds"] >  CUTOFF]
            fig3.add_trace(go.Scatter(
                x=hist["ds"], y=hist["yhat"], mode="lines",
                name=f"{gov} — historical", line=dict(color=color, width=2),
            ))
            fig3.add_trace(go.Scatter(
                x=fut["ds"], y=fut["yhat"], mode="lines",
                name=f"{gov} — forecast", line=dict(color=color, width=2, dash="dash"),
            ))
        fig3.add_shape(type="line", x0=0, x1=1, xref="paper",
                       y0=1.0, y1=1.0, line=dict(dash="dash", color="gray", width=1))
        fig3.add_shape(type="line", x0="2021-06-01", x1="2021-06-01",
                       y0=0, y1=1, yref="paper",
                       line=dict(dash="dot", color="gray", width=1.5))
        fig3.update_layout(
            title="Affordability Index Forecast — by Consumer Segment",
            xaxis_title="Date", yaxis_title="Affordability Index",
            height=500, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig3, use_container_width=True)

# ── Market Entry ──────────────────────────────────────────────────
def page_market_entry(data):
    st.markdown("## 🏆  Market Entry Ranking")
    st.markdown("*Composite scoring model combining all 5 analytical modules — ranked by commercial attractiveness*")

    if data["scores"].empty:
        st.error("Scoring data not found.")
        return

    sc = data["scores"].sort_values("rank")

    with st.expander("ℹ️  How the composite score is calculated"):
        dims = [("Purchasing Power","30%"), ("Price Stability","25%"),
                ("Price Accessibility","25%"), ("Market Density","10%"),
                ("Segment Quality","10%")]
        cols = st.columns(5)
        for col, (dim, wt) in zip(cols, dims):
            with col:
                st.markdown(f"""
                <div style="text-align:center; padding:12px 8px; background:#F0F4F8;
                     border-radius:8px;">
                    <div style="font-size:1.5rem; font-weight:700; color:#1F4E79;">{wt}</div>
                    <div style="font-size:0.78rem; color:#546E7A; margin-top:4px;">{dim}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊  Full Ranking", "🕸️  Radar Profile", "📋  Recommendations"])

    with tab1:
        fig = go.Figure(go.Bar(
            x=sc["composite_score"], y=sc["adm1_name"], orientation="h",
            marker_color=[COLORS.get(s, "#888") for s in sc["segment_name"]],
            text=sc["composite_score"].round(1), textposition="outside",
            customdata=sc[["segment_name","score_purchasing",
                           "score_stability","score_access","rank"]],
            hovertemplate=(
                "<b>%{y}</b><br>Rank: #%{customdata[4]}<br>"
                "Score: %{x:.1f}/100<br>Segment: %{customdata[0]}<br>"
                "Purchasing Power: %{customdata[1]:.1f}<br>"
                "Price Stability: %{customdata[2]:.1f}<br>"
                "Price Access: %{customdata[3]:.1f}<extra></extra>"
            ),
        ))
        fig.update_layout(
            title="Syria FMCG Market Entry Ranking — Composite Score",
            xaxis_title="Composite Score (0–100)",
            yaxis=dict(autorange="reversed"),
            xaxis=dict(range=[0, 115]),
            height=540, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=80, t=50, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

        disp = sc[["rank","adm1_name","segment_name","composite_score",
                   "score_purchasing","score_stability","score_access"]].copy()
        disp.columns = ["Rank","Governorate","Segment","Score",
                        "Purchasing Power","Price Stability","Price Access"]
        for c in ["Score","Purchasing Power","Price Stability","Price Access"]:
            disp[c] = disp[c].round(1)
        st.dataframe(disp, use_container_width=True, hide_index=True)

    with tab2:
        dims = ["score_purchasing","score_stability","score_access",
                "score_density","score_segment"]
        labs = ["Purchasing Power","Price Stability","Price Access",
                "Market Density","Segment Quality"]
        fig2 = go.Figure()
        ctop = ["#2E7D32","#43A047","#66BB6A"]
        cbot = ["#C62828","#E53935","#EF5350"]
        for i, (_, row) in enumerate(sc.head(3).iterrows()):
            v = [row[d] for d in dims] + [row[dims[0]]]
            fig2.add_trace(go.Scatterpolar(
                r=v, theta=labs+[labs[0]], fill="toself",
                name=f"#{int(row['rank'])} {row['adm1_name']}",
                line_color=ctop[i], opacity=0.75,
            ))
        for i, (_, row) in enumerate(sc.tail(3).iterrows()):
            v = [row[d] for d in dims] + [row[dims[0]]]
            fig2.add_trace(go.Scatterpolar(
                r=v, theta=labs+[labs[0]], fill="toself",
                name=f"#{int(row['rank'])} {row['adm1_name']}",
                line_color=cbot[i], opacity=0.5, line_dash="dash",
            ))
        fig2.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,100])),
            title="Dimension Profile — Top 3 vs Bottom 3 Governorates",
            height=540,
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        recs = {
            1: "Highest purchasing power (98.8/100) and perfect price access (100/100). Coastal location reduces import costs. Recommended for immediate market entry.",
            2: "Highest purchasing power score in the dataset (100/100). Strong stability. Recommended for simultaneous entry with Tartous.",
            3: "Near-perfect price access (97.3/100) and strong stability. Rural Damascus provides administrative hub access. Recommended as third entry point.",
            4: "Highest price stability score nationally (100/100). Entry viable with a competitive pricing strategy targeting lower-income households.",
            5: "Strong price stability (93.2/100) and good price access. Pilot a focused product range before committing to full distribution.",
        }
        for _, row in sc.head(5).iterrows():
            rank  = int(row["rank"])
            color = "#2E7D32" if rank <= 3 else "#E65100"
            st.markdown(f"""
            <div class="rec-card">
                <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
                    <div style="background:{color}; color:white; width:38px; height:38px;
                         border-radius:50%; display:flex; align-items:center;
                         justify-content:center; font-weight:700; font-size:1.1rem;
                         flex-shrink:0;">{rank}</div>
                    <div style="flex:1;">
                        <div style="font-size:1.05rem; font-weight:600; color:#1F4E79;">
                            {row["adm1_name"]}
                        </div>
                        <div style="font-size:0.8rem; color:#666;">{row["segment_name"]}</div>
                    </div>
                    <div style="font-size:1.9rem; font-weight:700; color:{color};">
                        {row["composite_score"]:.1f}
                    </div>
                </div>
                <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:8px;
                     margin-bottom:12px;">
                    <div style="text-align:center; background:#F0F4F8; border-radius:7px; padding:7px;">
                        <div style="font-size:1.1rem; font-weight:700; color:#1F4E79;">
                            {row["score_purchasing"]:.0f}
                        </div>
                        <div style="font-size:0.72rem; color:#666;">Purchasing Power</div>
                    </div>
                    <div style="text-align:center; background:#F0F4F8; border-radius:7px; padding:7px;">
                        <div style="font-size:1.1rem; font-weight:700; color:#1F4E79;">
                            {row["score_stability"]:.0f}
                        </div>
                        <div style="font-size:0.72rem; color:#666;">Price Stability</div>
                    </div>
                    <div style="text-align:center; background:#F0F4F8; border-radius:7px; padding:7px;">
                        <div style="font-size:1.1rem; font-weight:700; color:#1F4E79;">
                            {row["score_access"]:.0f}
                        </div>
                        <div style="font-size:0.72rem; color:#666;">Price Access</div>
                    </div>
                </div>
                <div style="font-size:0.85rem; color:#333;">{recs.get(rank,"")}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Decision Support ──────────────────────────────────────────────
def page_decision_support(data):
    st.markdown("## 🎯  Decision Support Tool")
    st.markdown("*Enter your product and investment context — receive a data-driven market entry recommendation*")

    st.markdown("""
    <div class="insight">
        This tool combines all five analytical modules to generate a customised market entry
        recommendation specific to your product category and risk tolerance.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Advisory input")
    c1, c2, c3 = st.columns(3)
    with c1:
        product = st.selectbox("Product category", [
            "Staple Foods (flour, rice, sugar, oil)",
            "Fresh & Protein (eggs, dairy, chicken)",
            "Household Goods (soap, cleaning products)",
            "Personal Care (toothpaste, hygiene)",
        ])
    with c2:
        risk = st.select_slider("Risk tolerance",
            options=["Very Low","Low","Medium","High","Very High"], value="Medium")
    with c3:
        horizon = st.selectbox("Entry timeline", [
            "Immediate (0–3 months)",
            "Short-term (3–6 months)",
            "Medium-term (6–12 months)",
            "Long-term (12+ months)",
        ])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🎯  Generate Recommendation", type="primary", use_container_width=True):
        if data["scores"].empty:
            st.error("Scoring data unavailable.")
            return

        sc  = data["scores"].sort_values("rank")
        min_score = {"Very Low":75,"Low":65,"Medium":55,"High":45,"Very High":30}[risk]
        rec = sc[sc["composite_score"] >= min_score]

        st.markdown("---")
        st.markdown(f"""
        <div style="background:#1F4E79; color:white; padding:16px 20px;
             border-radius:10px; margin-bottom:16px;">
            <div style="font-size:0.82rem; color:#BDD7EE;">AI PersonaMatch Advisory Report</div>
            <div style="font-size:1.15rem; font-weight:600; margin-top:4px;">
                {product.split("(")[0].strip()} — Syria Market Entry Strategy
            </div>
            <div style="font-size:0.82rem; color:#BDD7EE; margin-top:8px;">
                Risk: {risk} · Timeline: {horizon} ·
                Qualifying markets (≥{min_score} pts): {len(rec)} governorates
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not rec.empty:
            top = rec.iloc[0]
            st.markdown(f"""
            <div class="finding">
                <b>🏆  Primary recommendation: {top["adm1_name"]}</b><br>
                Composite score {top["composite_score"]:.1f}/100 — {top["segment_name"]}.<br>
                Purchasing Power {top["score_purchasing"]:.0f}/100 ·
                Price Stability {top["score_stability"]:.0f}/100 ·
                Price Access {top["score_access"]:.0f}/100
            </div>
            """, unsafe_allow_html=True)

            if len(rec) > 1:
                others = ", ".join(rec.iloc[1:4]["adm1_name"].tolist())
                st.markdown(f"""
                <div class="insight">
                    <b>Secondary markets for phased expansion:</b> {others}
                </div>
                """, unsafe_allow_html=True)

        cat_insights = {
            "Staple": "Staple foods have the highest income share burden. Bread and flour consume 15–40% of household income across most regions. Prioritise volume over margin.",
            "Fresh" : "Fresh products require cold chain infrastructure. Coastal regions offer the best logistics. Eggs and dairy show the most stable demand.",
            "Household": "Monitoring data is limited post-2021. Strong demand signal in coastal viable markets. Lower income share burden than food — households can absorb moderate pricing.",
            "Personal": "Monitoring began 2020. Diaspora returnees in coastal markets represent the highest purchasing power segment for personal care products.",
        }
        for key, text in cat_insights.items():
            if key.lower() in product.lower():
                st.markdown(f"<div class='insight'><b>📦  Category insight:</b> {text}</div>",
                            unsafe_allow_html=True)

        if risk in ["Very Low","Low"]:
            st.markdown("""
            <div class="warning">
                <b>⚠️  Low-risk profile:</b> Only coastal viable markets qualify under your
                risk tolerance. Start with Tartous (#1, 84.9/100) before expanding inland.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### All qualifying markets")
        disp = rec[["rank","adm1_name","segment_name","composite_score"]].copy()
        disp.columns = ["Rank","Governorate","Consumer Segment","Score"]
        disp["Score"] = disp["Score"].round(1)
        st.dataframe(disp, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
        return

    data = load_data()
    sidebar()

# ── Top navigation bar — always visible, never collapsible ────
    page_keys = [
        "Home", "Consumer Profiles", "Geographic Maps",
        "Price Intelligence", "Forecasting",
        "Market Entry", "Decision Support"
    ]
    page_labels = [
        "🏠 Home", "👤 Profiles", "🗺️ Maps",
        "💰 Prices", "📈 Forecast",
        "🏆 Ranking", "🎯 Advisory"
    ]

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    current_idx = page_keys.index(st.session_state["page"]) \
                  if st.session_state["page"] in page_keys else 0

    st.markdown("""
    <div style="background:#1a2744; padding:6px 16px; margin:-1rem -1rem 1.5rem;
         border-bottom:1px solid #2d4a7a;">
    </div>
    """, unsafe_allow_html=True)

    chosen = st.radio(
        "Navigate",
        page_labels,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="top_nav"
    )
    selected_page = page_keys[page_labels.index(chosen)]
    if selected_page != st.session_state["page"]:
        st.session_state["page"] = selected_page
        st.rerun()

    page = st.session_state["page"]
    
    if   page == "Home":              page_home(data)
    elif page == "Consumer Profiles": page_consumer_profiles(data)
    elif page == "Geographic Maps":   page_geographic_maps(data)
    elif page == "Price Intelligence":page_price_intelligence(data)
    elif page == "Forecasting":       page_forecasting(data)
    elif page == "Market Entry":      page_market_entry(data)
    elif page == "Decision Support":  page_decision_support(data)

if __name__ == "__main__":
    main()
