import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings("ignore")

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
section[data-testid="stSidebar"] { display: none !important; }
div[data-testid="collapsedControl"] { display: none !important; }

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

# Apply RTL CSS if Arabic
if st.session_state.get("lang", "en") == "ar":
    st.markdown("""
        <style>
        body, .stMarkdown, p, h1, h2, h3 {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Noto Sans Arabic', Arial, sans-serif !important;
        }
        [data-testid="stDataFrame"],
        [data-testid="stDataFrame"] *,
        .stPlotlyChart, .stSelectbox, .stTextInput,
        .stMetric, .stExpander, table, th, td {
            direction: ltr !important;
            text-align: left !important;
        }
        .stRadio > div { flex-direction: row-reverse !important; }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;600;700&display=swap" rel="stylesheet">
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

        role = st.session_state.get("user_role", "")
        role_color = {
            "Admin"  : "#C62828",
            "Company": "#2E7D32",
            "Analyst": "#1F4E79",
        }.get(role, "#888888")
        st.markdown(
            f'''<div style="text-align:center; margin:8px 8px 4px;">
            <span style="background:{role_color}; color:white;
                 font-size:0.72rem; padding:3px 14px;
                 border-radius:999px; font-weight:500;">
                {role} Access
            </span></div>''',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        lang_sb = st.session_state.get("lang", "en")
        if st.button(T("sign_out", lang_sb), use_container_width=True):
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


# ─── Translations ────────────────────────────────────────────────
TRANS = {
    "en": {
        "nav": ["🏠 Home","👤 Profiles","🗺️ Maps","💰 Prices",
                "📈 Forecast","🏆 Ranking","🎯 Advisory","📤 Upload","📖 Method"],
        "nav_company": ["🏠 Home","🗺️ Maps","💰 Prices","🏆 Ranking","🎯 Advisory","📤 Upload"],
        "sign_out"      : "🚪  Sign Out",
        "signed_in_as"  : "Signed in as",
        "data_updated"  : "📅  Data last updated: June 2021 · Source: WFP",
        "company_msg"   : "🏢  Company Access — Geographic Maps, Price Intelligence, Market Entry Ranking, and Decision Support.",
        "home_title"    : "🎯  AI PersonaMatch",
        "home_sub"      : "Syria FMCG Consumer Intelligence Platform — Precision Demand Forecasting & Consumer-Centric Analytics",
        "what_title"    : "What this platform does",
        "what_1"        : "<b>AI PersonaMatch</b> answers the core business question for Syria's reconstruction market: <b>Who buys what, where, and when?</b>",
        "what_2"        : "It transforms WFP humanitarian monitoring data into commercial consumer intelligence — the only structured, data-driven FMCG analytics tool built specifically for the Syrian market.",
        "modules_title" : "Five analytical modules",
        "findings_title": "Key findings",
        "quickview"     : "Market entry quick view",
        "kpi_labels"    : ["Price observations","Governorates","Months of data","Market locations","FMCG products"],
        "login_title"   : "AI PersonaMatch",
        "login_sub"     : "Syria FMCG Consumer Intelligence Platform",
        "login_tag"     : "Precision Demand Forecasting · Consumer-Centric Analytics",
        "login_user"    : "Username",
        "login_pass"    : "Password",
        "login_btn"     : "Sign In",
        "login_err"     : "Invalid username or password",
        "login_demo"    : "Demo credentials:",
        "findings": [
            ("🏆","Tartous ranks #1 (84.9/100)","Highest purchasing power and price stability in Syria"),
            ("📍","3 distinct consumer segments","Coastal viable, stressed interior, fragmented urban"),
            ("💸","67.4% of region-months are food insecure","Households cannot afford the basic food basket"),
            ("🍞","Idlib crisis detected","Actual bread price is 4× above what households can afford"),
            ("📈","Basket cost projected to 1.2M SYP","By March 2022 — Prophet AI detected structural price break"),
            ("🌙","Ramadan seasonal signal found","Prophet detected shifting annual demand peaks from price data"),
        ],
        "modules_list": [
            ("A","Consumer Segmentation","K-Means ML → 3 distinct consumer profiles"),
            ("B","Geographic Demand Maps","Interactive Syria choropleth maps"),
            ("C","Price Sensitivity","WTP thresholds & income share analysis"),
            ("D","Demand Forecasting","Prophet AI → 12-month projections"),
            ("E","Market Entry Scoring","Composite ranking of all 14 governorates"),
        ],
    },
    "ar": {
        "nav": ["🏠 الرئيسية","👤 الملفات","🗺️ الخرائط","💰 الأسعار",
                "📈 التنبؤ","🏆 التصنيف","🎯 الاستشارة","📤 رفع","📖 المنهجية"],
        "nav_company": ["🏠 الرئيسية","🗺️ الخرائط","💰 الأسعار","🏆 التصنيف","🎯 الاستشارة","📤 رفع"],
        "sign_out"      : "🚪  تسجيل الخروج",
        "signed_in_as"  : "مسجّل الدخول بوصفك",
        "data_updated"  : "📅  آخر تحديث: يونيو 2021 · المصدر: برنامج الغذاء العالمي",
        "company_msg"   : "🏢  وصول الشركة — الخرائط الجغرافية وذكاء الأسعار وتصنيف دخول السوق وأداة دعم القرار.",
        "home_title"    : "🎯  AI PersonaMatch",
        "home_sub"      : "منصة ذكاء المستهلك للسلع الاستهلاكية في سوريا — تنبؤ دقيق بالطلب وتحليلات متمحورة حول المستهلك",
        "what_title"    : "ما الذي تفعله هذه المنصة",
        "what_1"        : "<b>AI PersonaMatch</b> يجيب على السؤال التجاري الجوهري لسوق إعادة الإعمار السوري: <b>من يشتري ماذا، وأين، ومتى؟</b>",
        "what_2"        : "يحوّل بيانات برنامج الغذاء العالمي الإنسانية إلى ذكاء تجاري — الأداة الوحيدة المبنية على البيانات لتحليل السوق الاستهلاكية السورية.",
        "modules_title" : "خمس وحدات تحليلية",
        "findings_title": "النتائج الرئيسية",
        "quickview"     : "نظرة سريعة على دخول السوق",
        "kpi_labels"    : ["سجل أسعار","محافظة","شهراً من البيانات","موقع سوق","منتج استهلاكي"],
        "login_title"   : "AI PersonaMatch",
        "login_sub"     : "منصة ذكاء المستهلك للسلع الاستهلاكية في سوريا",
        "login_tag"     : "تنبؤ دقيق بالطلب · تحليلات متمحورة حول المستهلك",
        "login_user"    : "اسم المستخدم",
        "login_pass"    : "كلمة المرور",
        "login_btn"     : "تسجيل الدخول",
        "login_err"     : "اسم المستخدم أو كلمة المرور غير صحيحة",
        "login_demo"    : "بيانات اعتماد تجريبية:",
        "findings": [
            ("🏆","طرطوس في المرتبة الأولى (84.9/100)","أعلى قدرة شرائية واستقرار في الأسعار في سوريا"),
            ("📍","3 شرائح استهلاكية مميزة","الساحل الجديد، الداخل المتأزم، المراكز الحضرية المجزأة"),
            ("💸","67.4% من الفترات الإقليمية تعاني انعدام الأمن الغذائي","الأسر لا تستطيع تحمّل تكلفة السلة الغذائية الأساسية"),
            ("🍞","أزمة إدلب مرصودة","سعر الخبز الفعلي يتجاوز 4 أضعاف ما يمكن للأسر تحمّله"),
            ("📈","تكلفة السلة متجهة نحو 1.2 مليون ل.س","بحلول مارس 2022 — Prophet AI رصد كسراً هيكلياً في الأسعار"),
            ("🌙","رصد إشارة موسمية رمضانية","Prophet رصد ذُرى طلب سنوية متحركة من بيانات الأسعار"),
        ],
        "modules_list": [
            ("A","تجميع المستهلكين","K-Means ML → 3 ملفات تعريفية مميزة"),
            ("B","خرائط الطلب الجغرافي","خرائط كوروبليث تفاعلية لسوريا"),
            ("C","حساسية الأسعار","حدود الاستعداد للدفع وتحليل حصة الدخل"),
            ("D","التنبؤ بالطلب","Prophet AI → توقعات 12 شهراً"),
            ("E","تسجيل دخول السوق","تصنيف مركّب لجميع المحافظات الـ 14"),
        ],
    },
}

def T(key, lang=None):
    """Return translated string for current language"""
    if lang is None:
        lang = st.session_state.get("lang", "en")
    return TRANS.get(lang, TRANS["en"]).get(key, TRANS["en"].get(key, key))

# ─── Page-level translations ──────────────────────────────────────
TRANS_PAGES = {
    "en": {
        "profiles_title" : "## 👤  Consumer Profiles",
        "profiles_sub"   : "*K-Means ML identified 3 natural consumer segments across Syria's 14 governorates*",
        "profiles_seg"   : "### Segment positioning — Volatility vs Affordability",
        "profiles_about" : "About this segment",
        "profiles_strat" : "Recommended strategy",
        "profiles_govs"  : "Governorates",
        "maps_title"     : "## 🗺️  Geographic Intelligence",
        "maps_sub"       : "*Three interactive maps — hover over any governorate for detailed analytics*",
        "maps_summary"   : "### Full geographic summary",
        "maps_tabs"      : ["🟢🟠🔴  Consumer Segments","💚  Affordability Heatmap","🔴  Price Volatility Risk"],
        "price_title"    : "## 💰  Price Intelligence",
        "price_sub"      : "*Income share burden, willingness-to-pay thresholds, and market price accessibility*",
        "price_tabs"     : ["📊  Income Share per Product","🎯  WTP Calculator","🍞  Bread Affordability Gap"],
        "price_wtp_gov"  : "Select Governorate",
        "price_wtp_com"  : "Select Commodity",
        "price_wtp_inc"  : "Monthly Income (SYP)",
        "price_wtp_bud"  : "20% Budget (SYP)",
        "price_wtp_ceil" : "WTP Ceiling / unit",
        "price_wtp_all"  : "#### WTP ceiling across all governorates",
        "forecast_title" : "## 📈  Demand Forecasting",
        "forecast_sub"   : "*Prophet AI time series — trained on 124 months, projecting 12 months forward*",
        "forecast_tabs"  : ["🛒  Basket Cost Forecast","💸  Affordability Forecast","📍  Segment Forecasts"],
        "forecast_seg_note": "*One representative governorate per consumer segment*",
        "ranking_title"  : "## 🏆  Market Entry Ranking",
        "ranking_sub"    : "*Composite scoring model — ranked by commercial attractiveness*",
        "ranking_tabs"   : ["📊  Full Ranking","🕸️  Radar Profile","📋  Recommendations"],
        "ranking_how"    : "ℹ️  How the composite score is calculated",
        "advisory_title" : "## 🎯  Decision Support Tool",
        "advisory_sub"   : "*Enter your product and investment context — receive a data-driven market entry recommendation*",
        "advisory_input" : "### Advisory input",
        "advisory_prod"  : "Product category",
        "advisory_risk"  : "Risk tolerance",
        "advisory_horiz" : "Entry timeline",
        "advisory_btn"   : "🎯  Generate Recommendation",
        "advisory_all"   : "#### All qualifying markets",
        "method_title"   : "## 📖  Methodology",
        "method_sub"     : "*Full documentation of data sources, analytical methods, and platform architecture*",
        "method_ds"      : "### Data source",
        "method_modules" : "### Five analytical modules",
        "method_limits"  : "### Limitations and notes",
        "method_tech"    : "### Technology stack",
    },
    "ar": {
        "profiles_title" : "## 👤  ملفات المستهلكين",
        "profiles_sub"   : "*حدّد K-Means 3 شرائح استهلاكية طبيعية عبر 14 محافظة سورية*",
        "profiles_seg"   : "### تموضع الشرائح — التذبذب مقابل القدرة الشرائية",
        "profiles_about" : "عن هذه الشريحة",
        "profiles_strat" : "الاستراتيجية الموصى بها",
        "profiles_govs"  : "المحافظات",
        "maps_title"     : "## 🗺️  الذكاء الجغرافي",
        "maps_sub"       : "*ثلاث خرائط تفاعلية — مرّر فوق أي محافظة للاطلاع على التحليلات*",
        "maps_summary"   : "### الملخص الجغرافي الكامل",
        "maps_tabs"      : ["🟢🟠🔴  شرائح المستهلكين","💚  خريطة حرارية للقدرة الشرائية","🔴  مخاطر تذبذب الأسعار"],
        "price_title"    : "## 💰  ذكاء الأسعار",
        "price_sub"      : "*عبء حصة الدخل وحدود الاستعداد للدفع وإمكانية الوصول إلى السوق*",
        "price_tabs"     : ["📊  حصة الدخل لكل منتج","🎯  حاسبة الاستعداد للدفع","🍞  فجوة تحمّل سعر الخبز"],
        "price_wtp_gov"  : "اختر المحافظة",
        "price_wtp_com"  : "اختر السلعة",
        "price_wtp_inc"  : "الدخل الشهري (ل.س)",
        "price_wtp_bud"  : "20% من الميزانية (ل.س)",
        "price_wtp_ceil" : "سقف الاستعداد للدفع / وحدة",
        "price_wtp_all"  : "#### سقف الاستعداد للدفع عبر جميع المحافظات",
        "forecast_title" : "## 📈  التنبؤ بالطلب",
        "forecast_sub"   : "*نموذج Prophet AI — مُدرَّب على 124 شهراً، مع توقعات 12 شهراً قادمة*",
        "forecast_tabs"  : ["🛒  توقع تكلفة السلة","💸  توقع القدرة الشرائية","📍  توقعات الشرائح"],
        "forecast_seg_note": "*محافظة تمثيلية لكل شريحة استهلاكية*",
        "ranking_title"  : "## 🏆  تصنيف دخول السوق",
        "ranking_sub"    : "*نموذج تسجيل مركّب — مُصنَّف حسب الجاذبية التجارية*",
        "ranking_tabs"   : ["📊  التصنيف الكامل","🕸️  الملف الشعاعي","📋  التوصيات"],
        "ranking_how"    : "ℹ️  كيف يُحسب الدرجة المركّبة",
        "advisory_title" : "## 🎯  أداة دعم القرار",
        "advisory_sub"   : "*أدخل فئة منتجك وسياق استثمارك — احصل على توصية مبنية على البيانات*",
        "advisory_input" : "### مدخلات الاستشارة",
        "advisory_prod"  : "فئة المنتج",
        "advisory_risk"  : "مستوى تحمّل المخاطر",
        "advisory_horiz" : "الجدول الزمني للدخول",
        "advisory_btn"   : "🎯  توليد التوصية",
        "advisory_all"   : "#### جميع الأسواق المؤهّلة",
        "method_title"   : "## 📖  المنهجية",
        "method_sub"     : "*التوثيق الكامل لمصادر البيانات والأساليب التحليلية وبنية المنصة*",
        "method_ds"      : "### مصدر البيانات",
        "method_modules" : "### خمس وحدات تحليلية",
        "method_limits"  : "### القيود والملاحظات",
        "method_tech"    : "### مجموعة التقنيات",
    },
}

def TP(key, lang=None):
    """Page-level translation helper"""
    if lang is None:
        lang = st.session_state.get("lang", "en")
    val = TRANS_PAGES.get(lang, TRANS_PAGES["en"]).get(key)
    if val is None:
        val = TRANS_PAGES["en"].get(key, key)
    return val




COLORS = {
    "Viable coastal & admin markets"  : "#2E7D32",
    "Stressed interior markets"       : "#E65100",
    "Fragmented major urban centers"  : "#C62828",
}
CUTOFF       = pd.Timestamp("2021-06-01")
TRAIN_CUTOFF = pd.Timestamp("2020-06-01")  # train/test split point

# Clean display names — remove underscores and standardize
NAME_MAP = {
    "City_Damascus" : "Rural Damascus",
    "Dayr_Az_Zor"   : "Deir ez-Zor",
    "Al_Qunaytirah" : "Al-Qunaytirah",
    "As_Suweida"    : "As-Sweida",
    "Hassakeh"      : "Al-Hasakeh",
    "Dara"          : "Dar'a",
    "Idleb"         : "Idlib",
}

def clean_name(name):
    return NAME_MAP.get(str(name), str(name))

def clean_col(df, col="adm1_name"):
    if col in df.columns:
        df = df.copy()
        df[col] = df[col].apply(clean_name)
    return df

# ── Home ──────────────────────────────────────────────────────────
def page_home(data):
    lang = st.session_state.get("lang", "en")
    role = st.session_state.get("user_role", "")
    if role == "Company":
        st.markdown(f"""
        <div style="background:#1F4E79; color:#BDD7EE; padding:8px 16px;
             border-radius:8px; font-size:0.82rem; margin-bottom:12px;">
            {T("company_msg", lang)}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<h1 class=\"main-title\">{T('home_title', lang)}</h1>",
                unsafe_allow_html=True)
    st.markdown(f"<p class=\"sub-title\">{T('home_sub', lang)}</p>",
                unsafe_allow_html=True)

    # KPI strip
    kpi_nums    = ["116,588","14","124","96","35"]
    kpi_labels  = T("kpi_labels", lang)
    kpis        = list(zip(kpi_nums, kpi_labels))
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
    st.markdown(f"""
    <div style="display:flex; justify-content:flex-end; margin-bottom:8px;">
        <span style="background:#1a2744; color:#90CAF9; font-size:0.75rem;
             padding:4px 14px; border-radius:999px; border:1px solid #2d4a7a;">
            {T("data_updated", lang)}
        </span>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(f"### {T('what_title', lang)}")
        st.markdown(f"""
        <div class="insight">{T("what_1", lang)}</div>
        <div class="insight">{T("what_2", lang)}</div>
        """, unsafe_allow_html=True)

        st.markdown(f"### {T('modules_title', lang)}")
        modules = T("modules_list", lang)
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
        st.markdown(f"### {T('findings_title', lang)}")
        findings = T("findings", lang)
        for icon, title, desc in findings:
            st.markdown(f"""
            <div class="finding">
                <b>{icon}  {title}</b><br>
                <span style="font-size:0.82rem;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### {T('quickview', lang)}")
    if not data["scores"].empty:
        sc = clean_col(data["scores"].sort_values("rank"))
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
    lang = st.session_state.get("lang","en")
    st.markdown(TP("profiles_title",lang))
    st.markdown(TP("profiles_sub",lang))

    if data["segments"].empty:
        st.error("Segments data not found in data/ folder.")
        return

    segs = clean_col(data["segments"])

    seg_info = {
        "Viable coastal & admin markets": {
            "icon": "🟢", "color": "#2E7D32",
            "desc": TP("seg_viable_desc", lang),
            "strategy": TP("seg_viable_strat", lang),
        },
        "Stressed interior markets": {
            "icon": "🟠", "color": "#E65100",
            "desc": TP("seg_stressed_desc", lang),
            "strategy": TP("seg_stressed_strat", lang),
        },
        "Fragmented major urban centers": {
            "icon": "🔴", "color": "#C62828",
            "desc": TP("seg_frag_desc", lang),
            "strategy": TP("seg_frag_strat", lang),
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
                st.markdown(f"**{TP('profiles_about',lang)}:** {info['desc']}")
                st.markdown(f"**{TP('profiles_strat',lang)}:** {info['strategy']}")
                st.markdown(f"**{TP('profiles_govs',lang)}:** {govs}")
            with c2:
                if not subset.empty:
                    avg_a = subset["avg_affordability"].mean()
                    avg_v = subset["volatility_index"].mean()
                    st.metric("Avg Affordability",
                              f"{avg_a:.3f}",
                              delta="Above threshold ✓" if avg_a >= 1.0 else "Below threshold")
                    st.metric("Avg Price Volatility", f"{avg_v:.1f}%")

    st.markdown("---")
    st.markdown(TP("profiles_seg",lang))

    segs_plot = segs.copy().dropna(subset=["volatility_index","avg_affordability"])
    segs_plot["segment_name"] = segs_plot["segment_name"].fillna("Stressed interior markets")

    scatter_title = (
        "خريطة الشرائح الاستهلاكية — كل فقاعة محافظة سورية" if lang=="ar"
        else "Consumer Segment Map — each bubble is one Syrian governorate"
    )
    vol_label = "مؤشر التذبذب (CoV %)" if lang=="ar" else "Price Volatility Index (CoV %)"
    aff_label = "متوسط مؤشر القدرة الشرائية" if lang=="ar" else "Average Affordability Index"

    # Build figure manually — avoids Plotly color groupby bug
    fig = go.Figure()
    for seg_name, color in COLORS.items():
        subset = segs_plot[segs_plot["segment_name"] == seg_name]
        if subset.empty:
            continue
        sizes = (subset["avg_basket_cost"].fillna(200000) / 10000).clip(8, 40).tolist()
        fig.add_trace(go.Scatter(
            x=subset["volatility_index"],
            y=subset["avg_affordability"],
            mode="markers+text",
            name=seg_name,
            text=subset["adm1_name"],
            textposition="top center",
            marker=dict(
                color=color,
                size=sizes,
                opacity=0.85,
                line=dict(color="white", width=1),
            ),
            hovertemplate=(
                "<b>%{text}</b><br>"
                f"{vol_label}: %{{x:.1f}}<br>"
                f"{aff_label}: %{{y:.3f}}"
                "<extra></extra>"
            ),
        ))

    fig.add_hline(
        y=1.0, line_dash="dash", line_color="gray",
        annotation_text="عتبة القدرة الشرائية (1.0)" if lang=="ar"
                        else "Affordability threshold (1.0)",
    )
    fig.update_layout(
        title=scatter_title,
        xaxis_title=vol_label,
        yaxis_title=aff_label,
        height=480,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title="الشريحة" if lang=="ar" else "Segment",
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Geographic Maps ───────────────────────────────────────────────
def page_geographic_maps(data):
    import requests, json
    lang = st.session_state.get("lang","en")
    st.markdown(TP("maps_title",lang))
    st.markdown(TP("maps_sub",lang))

    # ── Load GeoJSON (cached) ─────────────────────────────────────
    @st.cache_data(show_spinner=False)
    def get_geojson():
        try:
            api  = "https://www.geoboundaries.org/api/current/gbOpen/SYR/ADM1/"
            meta = requests.get(api, timeout=20).json()
            geo  = requests.get(meta["gjDownloadURL"], timeout=60).json()
            return geo
        except Exception:
            return None

    geo = get_geojson()

    if geo is None:
        st.error("Could not load Syria boundary data. Please check your internet connection.")
        return

    # ── Detect which Plotly map API is available ──────────────────
    import plotly
    plotly_version = tuple(int(x) for x in plotly.__version__.split(".")[:2])
    USE_NEW_API = plotly_version >= (5, 18)

    def make_map(df, color_col, color_scale, range_c,
                 hover_data, labels, colorbar=None):
        """Version-safe choropleth map creator"""
        common = dict(
            data_frame=df,
            geojson=geo,
            locations="adm1_name",
            featureidkey="properties.adm1_name",
            color=color_col,
            color_continuous_scale=color_scale,
            range_color=range_c,
            zoom=ZOOM,
            center=CENTER,
            opacity=0.85,
            hover_name="adm1_name",
            hover_data=hover_data,
            labels=labels,
        )
        try:
            if USE_NEW_API:
                fig = px.choropleth_map(**common, map_style=MAPBOX_STYLE)
            else:
                fig = px.choropleth_mapbox(**common, mapbox_style=MAPBOX_STYLE)
        except Exception:
            # Final fallback — try the other API
            try:
                fig = px.choropleth_map(**common, map_style=MAPBOX_STYLE)
            except Exception:
                fig = px.choropleth_mapbox(**common, mapbox_style=MAPBOX_STYLE)
        if colorbar:
            fig.update_coloraxes(colorbar=colorbar)
        fig.update_layout(height=HEIGHT, margin=dict(l=0,r=0,t=20,b=0))
        return fig

    # Name mapping: GeoJSON → our dataset
    NAME_GEO = {
        "Damascus"      : "Damascus",
        "Aleppo"        : "Aleppo",
        "Rural Damascus": "City_Damascus",
        "Homs"          : "Homs",
        "Hama"          : "Hama",
        "Lattakia"      : "Lattakia",
        "Idleb"         : "Idleb",
        "Al-Hasakeh"    : "Hassakeh",
        "Deir-ez-Zor"   : "Dayr_Az_Zor",
        "Tartous"       : "Tartous",
        "Ar-Raqqa"      : "Raqqa",
        "Dar'a"        : "Dara",
        "As-Sweida"     : "As_Suweida",
        "Quneitra"      : "Al_Qunaytirah",
    }
    for f in geo["features"]:
        orig = f["properties"]["shapeName"]
        f["properties"]["adm1_name"] = NAME_GEO.get(orig, orig)

    segs = data["segments"].copy() if not data["segments"].empty else pd.DataFrame()
    if segs.empty:
        st.error("Segment data not loaded.")
        return

    # Segment color codes
    seg_codes = {
        "Viable coastal & admin markets" : 2,
        "Stressed interior markets"      : 1,
        "Fragmented major urban centers" : 0,
    }
    segs["seg_code"] = segs["segment_name"].map(seg_codes).fillna(1)

    MAPBOX_STYLE  = "carto-positron"
    CENTER        = {"lat": 35.0, "lon": 38.5}
    ZOOM          = 5.2
    HEIGHT        = 540

    tab1, tab2, tab3 = st.tabs(TP("maps_tabs", lang))

    # ── Tab 1: Consumer Segments ──────────────────────────────────
    with tab1:
        if lang == "ar":
            st.markdown("""
            <div class="insight">
                🟢 <b>أخضر</b> = الأسواق الساحلية الجديدة — طرطوس، اللاذقية، ريف دمشق<br>
                🟠 <b>برتقالي</b> = الأسواق الداخلية المتأزمة — 9 محافظات<br>
                🔴 <b>أحمر</b> = المراكز الحضرية الكبرى المجزأة — دمشق، حلب
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight">
                🟢 <b>Green</b> = Viable coastal markets — Tartous, Lattakia, City Damascus<br>
                🟠 <b>Orange</b> = Stressed interior markets — 9 governorates<br>
                🔴 <b>Red</b> = Fragmented urban centers — Damascus, Aleppo
            </div>""", unsafe_allow_html=True)

        segs_plot = segs.copy()
        segs_plot["seg_label"] = segs_plot["segment_name"]
        fig1 = make_map(
            df=segs_plot,
            color_col="seg_code",
            color_scale=[
                [0.00,"#C62828"],[0.33,"#C62828"],
                [0.34,"#E65100"],[0.66,"#E65100"],
                [0.67,"#2E7D32"],[1.00,"#2E7D32"],
            ],
            range_c=[0,2],
            hover_data={
                "seg_label"        : True,
                "avg_affordability": ":.3f",
                "volatility_index" : ":.1f",
                "seg_code"         : False,
                "adm1_name"        : False,
            },
            labels={
                "seg_label"        : "Segment",
                "avg_affordability": "Affordability",
                "volatility_index" : "Volatility %",
            },
        )
        fig1.update_coloraxes(showscale=False)
        st.plotly_chart(fig1, use_container_width=True)

    # ── Tab 2: Affordability Heatmap ──────────────────────────────
    with tab2:
        if lang == "ar":
            st.markdown("""
            <div class="insight">
                التدرج اللوني: أحمر داكن (انعدام أمن غذائي حاد) ← أصفر (قرب العتبة) ← أخضر (فوق 1.0)
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight">
                Color scale: deep red (severe food insecurity) → yellow (near threshold) → green (above 1.0).<br>
                Values above 1.0 mean households can afford the basic food basket.
            </div>""", unsafe_allow_html=True)

        max_a = 1.4
        fig2 = make_map(
            df=segs,
            color_col="avg_affordability",
            color_scale=[
                [0.00,       "#C62828"],
                [0.35/max_a, "#EF5350"],
                [0.60/max_a, "#FFA726"],
                [0.85/max_a, "#FFEE58"],
                [1.00/max_a, "#A5D6A7"],
                [1.00,       "#2E7D32"],
            ],
            range_c=[0, max_a],
            hover_data={
                "avg_affordability": ":.3f",
                "volatility_index"  : ":.1f",
                "segment_name"      : True,
                "adm1_name"         : False,
            },
            labels={
                "avg_affordability": "Affordability Index",
                "volatility_index"  : "Volatility %",
                "segment_name"      : "Segment",
            },
            colorbar=dict(
                title="Affordability<br>Index",
                tickvals=[0,0.5,1.0,1.4],
                ticktext=["0.0","0.5","1.0 ← threshold","1.4"],
                len=0.6,
            ),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 3: Price Volatility Risk ──────────────────────────────
    with tab3:
        if lang == "ar":
            st.markdown("""
            <div class="insight">
                أحمر داكن = أسعار غير مستقرة = مخاطر تشغيلية أعلى للشركات.<br>
                دمشق (95% CoV) وحلب (72% CoV) أكثر الأسواق تذبذباً.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight">
                Darker red = more unstable prices = higher business operating risk.<br>
                Damascus (95% CoV) and Aleppo (72% CoV) are the most volatile markets.
            </div>""", unsafe_allow_html=True)

        if not data["volatility"].empty:
            vol_data = data["volatility"].copy()
            vol_data.columns = ["adm1_name","regional_volatility_index"]
            map_vol = segs[["adm1_name"]].merge(vol_data, on="adm1_name", how="left")
        else:
            map_vol = segs[["adm1_name","volatility_index"]].copy()
            map_vol.columns = ["adm1_name","regional_volatility_index"]

        fig3 = make_map(
            df=map_vol,
            color_col="regional_volatility_index",
            color_scale="Reds",
            range_c=[40,100],
            hover_data={
                "regional_volatility_index": ":.1f",
                "adm1_name": False,
            },
            labels={"regional_volatility_index": "Volatility Index (%)"},
            colorbar=dict(
                title="Volatility<br>Index (%)",
                tickvals=[40,60,80,100],
                len=0.6,
            ),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── Summary table ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown(TP("maps_summary",lang))
    if not data["segments"].empty:
        disp = clean_col(data["segments"])[[
            "adm1_name","segment_name","avg_affordability",
            "volatility_index","avg_basket_cost"
        ]].copy()
        disp.columns = ["Governorate","Segment","Avg Affordability",
                        "Volatility (%)","Avg Basket Cost (SYP)"]
        disp["Avg Affordability"]     = disp["Avg Affordability"].round(3)
        disp["Volatility (%)"]        = disp["Volatility (%)"].round(1)
        disp["Avg Basket Cost (SYP)"] = disp["Avg Basket Cost (SYP)"].apply(
            lambda x: f"{x:,.0f}"
        )
        st.dataframe(
            disp.sort_values("Avg Affordability", ascending=False),
            use_container_width=True, hide_index=True
        )

# ── Price Intelligence ────────────────────────────────────────────
def page_price_intelligence(data):
    lang = st.session_state.get("lang","en")
    st.markdown(TP("price_title",lang))
    st.markdown(TP("price_sub",lang))

    tab1, tab2, tab3 = st.tabs(TP("price_tabs",lang))

    # ── Tab 1 ─────────────────────────────────────────────────────
    with tab1:
        if data["income_share"].empty:
            st.info("income_share data not found.")
        else:
            df = data["income_share"].head(15).copy()
            df = df.dropna(subset=["avg_share","min_share","max_share"])
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
            wtp = clean_col(data["wtp"])
            c1, c2 = st.columns(2)
            with c1:
                gov = st.selectbox(TP("price_wtp_gov",lang),
                                   sorted(wtp["adm1_name"].unique()), key="wtp_gov")
            with c2:
                com = st.selectbox(TP("price_wtp_com",lang),
                                   sorted(wtp["commodity"].unique()), key="wtp_com")

            row = wtp[(wtp["adm1_name"]==gov) & (wtp["commodity"]==com)]
            if not row.empty:
                r = row.iloc[0]
                ca, cb, cc = st.columns(3)
                ca.metric(TP("price_wtp_inc",lang), f"{r['monthly_income']:,.0f}")
                cb.metric(TP("price_wtp_bud",lang), f"{r['max_budget_syp']:,.0f}")
                cc.metric(TP("price_wtp_ceil",lang), f"{r['wtp_ceiling_syp']:,.1f} SYP")

                st.markdown(f"""
                <div class="finding">
                    A household in <b>{gov}</b> can pay up to
                    <b>{r['wtp_ceiling_syp']:,.1f} SYP</b> per unit of
                    <b>{com.replace(" - Retail","")}</b>
                    before that product consumes more than 20% of their monthly income
                    ({r['monthly_income']:,.0f} SYP/month).
                </div>
                """, unsafe_allow_html=True)

            st.markdown(TP("price_wtp_all",lang))
            wtp_com = wtp[wtp["commodity"]==com].sort_values(
                "wtp_ceiling_syp", ascending=False
            ).copy()

            # Merge segment names safely
            if not data["scores"].empty:
                wtp_com = wtp_com.merge(
                    data["scores"][["adm1_name","segment_name"]],
                    on="adm1_name", how="left"
                )
                # Critical: fill NaN to prevent Plotly groupby crash
                wtp_com["segment_name"] = wtp_com["segment_name"].fillna(
                    "Stressed interior markets"
                )
                use_color = "segment_name"
            else:
                use_color = None

            wtp_com = wtp_com.dropna(subset=["adm1_name","wtp_ceiling_syp"])

            if not wtp_com.empty:
                wtp_title = (
                    f"سقف الاستعداد للدفع — {com.replace(' - Retail','')}"
                    if lang == "ar" else
                    f"WTP Ceiling — {com.replace(' - Retail','')}"
                )
                # Assign colors per row — avoids Plotly color groupby bug
                bar_colors = [
                    COLORS.get(s, "#2E75B6")
                    for s in wtp_com.get("segment_name",
                        ["Stressed interior markets"]*len(wtp_com))
                ]
                fig2 = go.Figure(go.Bar(
                    x=wtp_com["adm1_name"],
                    y=wtp_com["wtp_ceiling_syp"],
                    marker_color=bar_colors,
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        + ("السعر الأقصى: %{y:,.0f} ل.س" if lang=="ar"
                           else "Max Price: %{y:,.0f} SYP")
                        + "<extra></extra>"
                    ),
                ))
                fig2.update_layout(
                    title=wtp_title,
                    xaxis_title="المحافظة" if lang=="ar" else "Governorate",
                    yaxis_title="السعر الأقصى (ل.س)" if lang=="ar" else "Max Price (SYP)",
                    xaxis_tickangle=-45,
                    height=380,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
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
    lang = st.session_state.get("lang","en")
    st.markdown(TP("forecast_title",lang))
    st.markdown(TP("forecast_sub",lang))

    tab1, tab2, tab3 = st.tabs(TP("forecast_tabs",lang))

    def forecast_chart(fc, title, y_label, color, threshold=None):
        if fc.empty:
            st.info("Forecast data not found.")
            return

        # Split: training = up to Jun 2020, test = Jul 2020 to Jun 2021
        train = fc[fc["ds"] <= TRAIN_CUTOFF].copy()
        test  = fc[(fc["ds"] > TRAIN_CUTOFF) & (fc["ds"] <= CUTOFF)].copy()

        if lang == "ar":
            lbl_train = "بيانات التدريب (ملاءمة النموذج)"
            lbl_ci    = "فترة ثقة 80% (مجموعة الاختبار)"
            lbl_pred  = "متوقّع — مجموعة الاختبار"
            lbl_split = "بداية مجموعة الاختبار"
            lbl_end   = "نهاية البيانات"
        else:
            lbl_train = "Training data (model fit)"
            lbl_ci    = "80% confidence interval (test set)"
            lbl_pred  = "Predicted — test set"
            lbl_split = "Test set begins"
            lbl_end   = "End of data"

        figfc = go.Figure()

        # Confidence band — test period only
        if not test.empty:
            try:
                r, g, b = px.colors.hex_to_rgb(color)
                band_color = f"rgba({r},{g},{b},40)"
            except Exception:
                band_color = "rgba(200,100,50,40)"
            figfc.add_trace(go.Scatter(
                x=pd.concat([test["ds"], test["ds"][::-1]]),
                y=pd.concat([test["yhat_upper"], test["yhat_lower"][::-1]]),
                fill="toself", fillcolor=band_color,
                line=dict(color="rgba(0,0,0,0)"), name=lbl_ci,
            ))

        # Training line
        if not train.empty:
            figfc.add_trace(go.Scatter(
                x=train["ds"], y=train["yhat"], mode="lines",
                name=lbl_train, line=dict(color="#1F4E79", width=2),
            ))

        # Predicted line — test period
        if not test.empty:
            figfc.add_trace(go.Scatter(
                x=test["ds"], y=test["yhat"],
                mode="lines+markers",
                name=lbl_pred,
                line=dict(color=color, width=2.5, dash="dash"),
                marker=dict(size=6),
            ))

        # Affordability threshold
        if threshold is not None:
            figfc.add_shape(type="line", x0=0, x1=1, xref="paper",
                            y0=threshold, y1=threshold,
                            line=dict(dash="dash", color="green", width=1.5))
            figfc.add_annotation(x=0.01, xref="paper", y=threshold,
                                 text=f"Threshold ({threshold})",
                                 showarrow=False, xanchor="left",
                                 yanchor="bottom",
                                 font=dict(color="green", size=11))

        # Train/test split marker
        figfc.add_shape(type="line",
                        x0=str(TRAIN_CUTOFF)[:10], x1=str(TRAIN_CUTOFF)[:10],
                        y0=0, y1=1, yref="paper",
                        line=dict(dash="dot", color="gray", width=1.5))
        figfc.add_annotation(x=str(TRAIN_CUTOFF)[:10], y=0.96, yref="paper",
                             text=lbl_split, showarrow=False,
                             xanchor="left", font=dict(color="gray", size=11))

        # End of data marker
        figfc.add_shape(type="line",
                        x0="2021-06-01", x1="2021-06-01",
                        y0=0, y1=1, yref="paper",
                        line=dict(dash="dot", color="#2E7D32", width=1.5))
        figfc.add_annotation(x="2021-06-01", y=0.88, yref="paper",
                             text=lbl_end, showarrow=False,
                             xanchor="left", font=dict(color="#2E7D32", size=11))

        figfc.update_layout(
            title=title, xaxis_title="Date", yaxis_title=y_label,
            height=480,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(x=0.01, y=0.99),
        )
        st.plotly_chart(figfc, use_container_width=True)

        # Forecast table — test period only
        if not test.empty:
            tbl = test[["ds","yhat","yhat_lower","yhat_upper"]].copy()
            tbl.columns = ["Month","Forecast","Lower Bound","Upper Bound"]
            tbl["Month"] = tbl["Month"].dt.strftime("%B %Y")
            for c in ["Forecast","Lower Bound","Upper Bound"]:
                tbl[c] = tbl[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(tbl, use_container_width=True, hide_index=True)
