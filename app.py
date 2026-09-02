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
CUTOFF = pd.Timestamp("2021-06-01")

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
        st.markdown(TP("forecast_seg_note",lang))
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
    lang = st.session_state.get("lang","en")
    st.markdown(TP("ranking_title",lang))
    st.markdown(TP("ranking_sub",lang))

    if data["scores"].empty:
        st.error("Scoring data not found.")
        return

    sc = clean_col(data["scores"].sort_values("rank"))

    with st.expander(TP("ranking_how",lang)):
        if lang == "ar":
            dims = [
                ("القدرة الشرائية","30%"),
                ("استقرار الأسعار","25%"),
                ("إمكانية الوصول للأسعار","25%"),
                ("كثافة السوق","10%"),
                ("جودة الشريحة","10%"),
            ]
        else:
            dims = [
                ("Purchasing Power","30%"),
                ("Price Stability","25%"),
                ("Price Accessibility","25%"),
                ("Market Density","10%"),
                ("Segment Quality","10%"),
            ]
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
    tab1, tab2, tab3 = st.tabs(TP("ranking_tabs",lang))

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
        if lang == "ar":
            disp.columns = ["الترتيب","المحافظة","الشريحة","الدرجة",
                            "القدرة الشرائية","استقرار الأسعار","إمكانية الوصول"]
            num_cols = ["الدرجة","القدرة الشرائية","استقرار الأسعار","إمكانية الوصول"]
        else:
            disp.columns = ["Rank","Governorate","Segment","Score",
                            "Purchasing Power","Price Stability","Price Access"]
            num_cols = ["Score","Purchasing Power","Price Stability","Price Access"]
        for c in num_cols:
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
    lang = st.session_state.get("lang","en")
    st.markdown(TP("advisory_title",lang))
    st.markdown(TP("advisory_sub",lang))

    st.markdown("""
    <div class="insight">
        This tool combines all five analytical modules to generate a customised market entry
        recommendation specific to your product category and risk tolerance.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(TP("advisory_input",lang))
    # Bilingual product/risk/horizon options
    if lang == "ar":
        prod_opts  = [
            "المواد الغذائية الأساسية (دقيق، أرز، سكر، زيت)",
            "البروتين والطازج (بيض، ألبان، دجاج)",
            "المواد المنزلية (صابون، منظفات)",
            "العناية الشخصية (معجون أسنان، النظافة)",
        ]
        risk_opts   = ["منخفض جداً","منخفض","متوسط","مرتفع","مرتفع جداً"]
        horiz_opts  = [
            "فوري (0–3 أشهر)",
            "قصير المدى (3–6 أشهر)",
            "متوسط المدى (6–12 شهراً)",
            "طويل المدى (أكثر من 12 شهراً)",
        ]
        prod_lbl  = "فئة المنتج"
        risk_lbl  = "مستوى تحمّل المخاطر"
        horiz_lbl = "الجدول الزمني للدخول"
    else:
        prod_opts  = [
            "Staple Foods (flour, rice, sugar, oil)",
            "Fresh & Protein (eggs, dairy, chicken)",
            "Household Goods (soap, cleaning products)",
            "Personal Care (toothpaste, hygiene)",
        ]
        risk_opts   = ["Very Low","Low","Medium","High","Very High"]
        horiz_opts  = [
            "Immediate (0–3 months)",
            "Short-term (3–6 months)",
            "Medium-term (6–12 months)",
            "Long-term (12+ months)",
        ]
        prod_lbl  = "Product category"
        risk_lbl  = "Risk tolerance"
        horiz_lbl = "Entry timeline"

    # English risk options for scoring logic
    risk_en_options = ["Very Low","Low","Medium","High","Very High"]

    c1, c2, c3 = st.columns(3)
    with c1:
        product = st.selectbox(prod_lbl, prod_opts,
                               key=f"prod_{lang}")
    with c2:
        # Use language-specific key to avoid stale session state mismatch
        risk = st.select_slider(risk_lbl,
                                options=risk_opts,
                                value=risk_opts[2],
                                key=f"risk_{lang}")
        risk_idx = risk_opts.index(risk)
        risk_en  = risk_en_options[risk_idx]
    with c3:
        horizon = st.selectbox(horiz_lbl, horiz_opts,
                               key=f"horiz_{lang}")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(TP("advisory_btn",lang), type="primary", use_container_width=True):
        if data["scores"].empty:
            st.error("Scoring data unavailable.")
            return

        sc  = clean_col(data["scores"].sort_values("rank"))
        min_score = {"Very Low":75,"Low":65,"Medium":55,
                      "High":45,"Very High":30}.get(risk_en, 55)
        rec = sc[sc["composite_score"] >= min_score]

        st.markdown("---")
        st.markdown(f"""
        <div style="background:#1F4E79; color:white; padding:16px 20px;
             border-radius:10px; margin-bottom:16px;">
            <div style="font-size:0.82rem; color:#BDD7EE;">{TP("gen_report",lang)}</div>
            <div style="font-size:1.15rem; font-weight:600; margin-top:4px;">
                {product.split("(")[0].strip()} — Syria Market Entry Strategy
            </div>
            <div style="font-size:0.82rem; color:#BDD7EE; margin-top:8px;">
                {risk} · {horizon} · {TP("qualifying",lang)} (≥{min_score}): {len(rec)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not rec.empty:
            top = rec.iloc[0]
            st.markdown(f"""
            <div class="finding">
                <b>{TP("primary_rec",lang)}: {top["adm1_name"]}</b><br>
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
                    <b>{TP("secondary_rec",lang)}:</b> {others}
                </div>
                """, unsafe_allow_html=True)

        if lang == "ar":
            cat_insights = {
                "أساسية"    : "المواد الغذائية الأساسية تمثل أعلى عبء على الدخل. يستهلك الخبز والدقيق 15–40% من دخل الأسرة في معظم المناطق. رَكِّز على الحجم بدلاً من الهامش.",
                "بروتين"    : "المنتجات الطازجة تتطلب بنية تحتية للتبريد. تتميز المناطق الساحلية بأفضل لوجستيات. البيض ومنتجات الألبان الأكثر استقراراً في الطلب.",
                "منزلية"    : "بيانات الرصد محدودة ما بعد 2021. إشارة طلب قوية في الأسواق الساحلية. عبء حصة دخل أقل مقارنة بالغذاء.",
                "شخصية"     : "الرصد بدأ عام 2020. المغتربون العائدون في الأسواق الساحلية يمثلون أعلى شريحة قوة شرائية.",
            }
            icon_insight = "📦  ملاحظة الفئة"
        else:
            cat_insights = {
                "Staple"   : "Staple foods have the highest income share burden. Bread and flour consume 15–40% of household income. Prioritise volume over margin.",
                "Fresh"    : "Fresh products require cold chain infrastructure. Coastal regions offer the best logistics. Eggs and dairy show the most stable demand.",
                "Household": "Monitoring data is limited post-2021. Strong demand signal in coastal viable markets. Lower income share burden than food.",
                "Personal" : "Monitoring began 2020. Diaspora returnees in coastal markets represent the highest purchasing power segment.",
            }
            icon_insight = "📦  Category insight"

        for key, text in cat_insights.items():
            if key.lower() in product.lower():
                st.markdown(f"<div class='insight'><b>{icon_insight}:</b> {text}</div>",
                            unsafe_allow_html=True)

        if risk_en in ["Very Low","Low"]:
            st.markdown(f"""
            <div class="warning">{TP("low_risk_note",lang)}</div>
            """, unsafe_allow_html=True)

        st.markdown(TP("advisory_all",lang))
        disp = rec[["rank","adm1_name","segment_name","composite_score"]].copy()
        disp.columns = ["Rank","Governorate","Consumer Segment","Score"]
        disp["Score"] = disp["Score"].round(1)
        st.dataframe(disp, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

# ── Methodology ───────────────────────────────────────────────────
def page_methodology(data):
    lang = st.session_state.get("lang","en")
    st.markdown(TP("method_title",lang))
    st.markdown(TP("method_sub",lang))

    st.markdown(TP("method_ds",lang))
    st.markdown("""
    <div class="insight">
        <b>Primary dataset:</b> WFP (World Food Programme) Food Price Monitoring Database
        for Syria, accessed via the Humanitarian Data Exchange (HDX) platform.<br><br>
        WFP field monitors record retail prices of essential commodities in local markets
        across Syria every month. This is the most comprehensive, structured, and
        geographically complete source of consumer price data available for Syria.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (num, lbl) in zip([c1,c2,c3,c4], [
        ("116,588",              "Total observations"),
        ("Apr 2011 — Jun 2021",  "Temporal coverage"),
        ("14 gov. · 96 markets", "Geographic coverage"),
        ("80 commodities",       "Products tracked"),
    ]):
        with col:
            st.markdown(f"""
            <div style="background:#1F4E79; color:white; border-radius:10px;
                 padding:14px; text-align:center; margin-bottom:8px;">
                <div style="font-size:1rem; font-weight:700; color:#DEEAF1;">{num}</div>
                <div style="font-size:0.72rem; color:#BDD7EE; margin-top:4px;">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(TP("method_modules",lang))
    if lang == "ar":
        modules = [
            ("A", "تجميع المستهلكين",
             "K-Means (تعلم آلي غير خاضع للإشراف)",
             "يُجمّع 14 محافظة سورية في شرائح استهلاكية طبيعية بناءً على تذبذب الأسعار "
             "ومؤشر القدرة الشرائية وتكلفة السلة. تم تحديد K=3 بطريقة الكوع ومعامل Silhouette "
             "(أعلى قيمة 0.475).",
             "3 ملفات تعريفية مُسمّاة للشرائح مع التوزيع الجغرافي"),
            ("B", "خرائط الطلب الجغرافي",
             "Plotly Mapbox choropleth + GeoPandas + GeoJSON",
             "يربط الميزات التحليلية بملف الحدود الإدارية لسوريا (geoBoundaries ADM1). "
             "ثلاث خرائط: شرائح المستهلكين، تدرج القدرة الشرائية، ومؤشر مخاطر تذبذب الأسعار.",
             "3 خرائط سوريا تفاعلية — مرّر فوق أي محافظة للتفاصيل"),
            ("C", "تحليل حساسية الأسعار",
             "انحدار OLS + حساب حصة الدخل",
             "يحسب حصة الدخل (% من دخل الأسرة لكل سلعة) وسقف الاستعداد للدفع "
             "باستخدام كميات WFP وحجم أسرة متوسط 4.3 أشخاص. يُنمذج OLS العلاقة بين "
             "تغيرات الأسعار الشهرية وتغيرات مؤشر القدرة الشرائية.",
             "سقف الاستعداد للدفع لكل منتج لكل منطقة + مخطط فجوة الخبز"),
            ("D", "التنبؤ الزمني",
             "نموذج Prophet للسلاسل الزمنية (Facebook)",
             "Prophet مُدرَّب على 122 شهراً من البيانات. مُكوَّن بنمط موسمية ضربية "
             "لمعالجة النمو الأسي. نقاط التغيير الهيكلي مكتشفة تلقائياً. "
             "تم رصد الإشارة الموسمية لرمضان من بيانات الأسعار.",
             "توقعات 12 شهراً قادمة مع فترات ثقة 80%"),
            ("E", "تسجيل دخول السوق",
             "مصفوفة تسجيل مركّبة مرجّحة",
             "خمسة أبعاد مُعيَّرة 0–100 بالتطبيع min-max. "
             "الأوزان: القدرة الشرائية 30%، استقرار الأسعار 25%، إمكانية الوصول 25%، "
             "كثافة السوق 10%، جودة الشريحة 10%. تصنيف جميع المحافظات الـ14.",
             "تصنيف كامل للمحافظات مع تفاصيل الأبعاد"),
        ]
        meth_lbl = "الأسلوب"
        out_lbl  = "الناتج"
        desc_lbl = "الوصف"
        exp_prefix = "الوحدة"
    else:
        modules = [
            ("A", "Consumer Segmentation",
             "K-Means clustering (unsupervised machine learning)",
             "Groups Syria's 14 governorates into natural consumer segments based on "
             "price volatility, affordability index, and basket cost. Optimal K=3 determined "
             "using the Elbow method (inertia) and Silhouette coefficient (peak score 0.475).",
             "3 named consumer segment profiles with geographic distribution"),
            ("B", "Geographic Demand Mapping",
             "Plotly Mapbox choropleth + GeoPandas + GeoJSON",
             "Joins analytical features to Syria's administrative boundary shapefile "
             "(geoBoundaries ADM1). Three maps: consumer segments, affordability gradient, "
             "and price volatility risk index.",
             "3 interactive Syria maps — hover for governorate detail"),
            ("C", "Price Sensitivity Analysis",
             "OLS regression + income share computation",
             "Computes income share (% of household income per commodity) and "
             "willingness-to-pay ceilings using WFP Minimum Food Expenditure Basket quantities "
             "and average household size of 4.3 persons. OLS models the relationship between "
             "monthly price changes and affordability index changes.",
             "WTP thresholds per product per region + bread affordability gap chart"),
            ("D", "Temporal Forecasting",
             "Facebook Prophet time series model",
             "Prophet trained on 122 months of historical basket cost and affordability data. "
             "Configured with multiplicative seasonality to handle exponential price growth. "
             "Structural changepoints detected automatically. Seasonal Ramadan signal detected "
             "from price data without explicit calendar input.",
             "12-month forward projections with 80% confidence intervals"),
            ("E", "Market Entry Scoring",
             "Weighted composite scoring matrix",
             "Five dimensions normalized 0–100 using min-max normalization. "
             "Weights: Purchasing Power 30%, Price Stability 25%, Price Accessibility 25%, "
             "Market Density 10%, Segment Quality 10%. All 14 governorates ranked.",
             "Full governorate ranking with dimension-level score breakdown"),
        ]
        meth_lbl = "Method"
        out_lbl  = "Output"
        desc_lbl = "Description"
        exp_prefix = "Module"

    for letter, name, method, desc, output in modules:
        with st.expander(f"{exp_prefix} {letter} — {name}", expanded=False):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"**{meth_lbl}:** {method}")
                st.markdown(f"**{out_lbl}:** {output}")
            with c2:
                st.markdown(f"**{desc_lbl}:** {desc}")

    st.markdown(TP("method_limits",lang))
    if lang == "ar":
        st.markdown("""
        <div class="warning">
            <b>قطع البيانات:</b> تغطي بيانات WFP الفترة من أبريل 2011 إلى يونيو 2021.
            تلتقط هذه النافذة القوس الكامل لأزمة سوريا الاقتصادية —
            من الخط الأساسي قبل النزاع حتى انهيار التضخم المفرط 2020–2021.
        </div>
        <div class="warning">
            <b>ملاحظة تكلفة السلة:</b> قد تُبالغ تكلفة السلة المرجّحة بالكميات قليلاً
            في تقدير الإنفاق الفعلي للأسرة بسبب تضمين دقيق القمح والخبز معاً.
            يمثّل هذا تقديراً محافظاً للحد الأعلى متوافقاً مع سيناريوهات الأمن الغذائي الأسوأ.
        </div>
        <div class="insight">
            <b>دقة جغرافية:</b> جميع التحليلات على مستوى المحافظة (ADM1).
            لا يُرصد التباين داخل كل محافظة في هذا الإصدار. تحليل المدينة مخطط للإصدار v2.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning">
            <b>Data cutoff:</b> The WFP dataset covers April 2011 through June 2021.
            The 2011–2021 window captures the full arc of Syria's economic crisis —
            from the pre-conflict baseline through the 2020–2021 hyperinflationary collapse.
        </div>
        <div class="warning">
            <b>Basket cost note:</b> The quantity-weighted basket cost may slightly overestimate
            true household expenditure due to simultaneous inclusion of both wheat flour and bread.
            This represents a conservative upper-bound estimate consistent with food security
            worst-case scenarios.
        </div>
        <div class="insight">
            <b>Geographic granularity:</b> All analysis is at governorate level (ADM1).
            Sub-governorate variation within each region is not captured in this version.
            City-level analysis is planned for v2.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(TP("method_tech",lang))
    if lang == "ar":
        tech = [
            ("Python 3.12",     "لغة البرمجة الأساسية"),
            ("Pandas + NumPy",  "معالجة البيانات وهندسة الميزات"),
            ("Scikit-learn",    "K-Means والتطبيع بـ StandardScaler"),
            ("Statsmodels",     "تحليل الانحدار OLS"),
            ("Prophet",         "التنبؤ بالسلاسل الزمنية"),
            ("Plotly",          "الرسوم البيانية والخرائط التفاعلية"),
            ("GeoPandas",       "معالجة البيانات الجيومكانية"),
            ("Streamlit",       "إطار تطبيق الويب"),
            ("WFP / HDX",       "مصدر البيانات الأساسي (أسعار الغذاء الإنسانية)"),
            ("geoBoundaries",   "ملف حدود المحافظات السورية"),
        ]
    else:
        tech = [
            ("Python 3.12",     "Core programming language"),
            ("Pandas + NumPy",  "Data processing and feature engineering"),
            ("Scikit-learn",    "K-Means clustering and StandardScaler normalization"),
            ("Statsmodels",     "OLS regression analysis"),
            ("Prophet",         "Time series forecasting"),
            ("Plotly",          "Interactive charts and maps"),
            ("GeoPandas",       "Geospatial data processing"),
            ("Streamlit",       "Web application framework"),
            ("WFP / HDX",       "Primary data source (humanitarian food prices)"),
            ("geoBoundaries",   "Syria administrative boundary shapefile"),
        ]
    c1, c2 = st.columns(2)
    for i, (tool, desc) in enumerate(tech):
        with (c1 if i % 2 == 0 else c2):
            st.markdown(f"""
            <div style="display:flex; gap:10px; align-items:center; padding:7px 10px;
                 background:#F8F9FA; border-radius:6px; margin:3px 0;">
                <div style="font-weight:600; color:#1F4E79;
                     min-width:130px; font-size:0.85rem;">{tool}</div>
                <div style="color:#546E7A; font-size:0.82rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)



# ── Company Data Upload ───────────────────────────────────────────
def page_upload(data):
    lang = st.session_state.get("lang", "en")

    if lang == "ar":
        st.markdown("## 📤  تحليل بيانات الشركة")
        st.markdown("*ارفع ملف CSV ببيانات مبيعاتك — ستحلّله المنصة وتقارنه بالمعايير الوطنية السورية*")
    else:
        st.markdown("## 📤  Company Data Analysis")
        st.markdown("*Upload your sales CSV — the platform analyses it and benchmarks it against Syria national data*")

    # ── Template download ─────────────────────────────────────────
    template_csv = """date,governorate,product_name,category,quantity_sold,unit_price_syp,total_revenue_syp
2024-01-15,Tartous,Wheat Flour,Staple Foods,120,4500,540000
2024-01-15,Lattakia,Cooking Oil,Staple Foods,80,12000,960000
2024-01-20,Homs,Sugar,Staple Foods,200,3800,760000
2024-02-01,Damascus,Rice,Staple Foods,150,6500,975000
2024-02-10,Aleppo,Soap,Household Goods,90,2500,225000
"""

    if lang == "ar":
        st.markdown("### الخطوة 1 — تحميل القالب")
        st.markdown("""
        <div class="insight">
            يجب أن يحتوي ملفك على هذه الأعمدة: date, governorate, product_name,
            category, quantity_sold, unit_price_syp, total_revenue_syp
        </div>
        """, unsafe_allow_html=True)
        dl_label = "⬇️  تحميل قالب CSV"
    else:
        st.markdown("### Step 1 — Download the template")
        st.markdown("""
        <div class="insight">
            Your file must contain these columns: <b>date, governorate, product_name,
            category, quantity_sold, unit_price_syp, total_revenue_syp</b>
        </div>
        """, unsafe_allow_html=True)
        dl_label = "⬇️  Download CSV template"

    st.download_button(
        label=dl_label,
        data=template_csv,
        file_name="personamatch_template.csv",
        mime="text/csv",
    )

    st.markdown("---")

    # ── File upload ───────────────────────────────────────────────
    upload_label = "### الخطوة 2 — رفع بياناتك" if lang == "ar" else "### Step 2 — Upload your data"
    st.markdown(upload_label)

    uploader_text = "اختر ملف CSV" if lang == "ar" else "Choose a CSV file"
    uploaded_file = st.file_uploader(uploader_text, type=["csv"])

    if uploaded_file is None:
        if lang == "ar":
            st.info("لم يتم رفع أي ملف بعد. قم بتحميل القالب أعلاه، ثم أضف بياناتك وارفعه هنا.")
        else:
            st.info("No file uploaded yet. Download the template above, fill in your data, then upload it here.")
        return

    # ── Load and validate ─────────────────────────────────────────
    try:
        df_company = pd.read_csv(uploaded_file)
        df_company.columns = df_company.columns.str.strip().str.lower()
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return

    required_cols = ["date","governorate","product_name","category",
                     "quantity_sold","unit_price_syp","total_revenue_syp"]
    missing = [c for c in required_cols if c not in df_company.columns]

    if missing:
        if lang == "ar":
            st.error(f"الأعمدة المفقودة: {', '.join(missing)}")
        else:
            st.error(f"Missing columns: {', '.join(missing)}")
        st.markdown("**Your columns:** " + ", ".join(df_company.columns.tolist()))
        return

    # Parse dates
    df_company["date"] = pd.to_datetime(df_company["date"], errors="coerce")
    df_company["total_revenue_syp"] = pd.to_numeric(
        df_company["total_revenue_syp"], errors="coerce"
    ).fillna(0)
    df_company["quantity_sold"] = pd.to_numeric(
        df_company["quantity_sold"], errors="coerce"
    ).fillna(0)

    # ── Summary stats ─────────────────────────────────────────────
    if lang == "ar":
        st.markdown("### ✅  تم قبول الملف بنجاح")
    else:
        st.markdown("### ✅  File accepted successfully")

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (f"{len(df_company):,}",
         "سجلات مبيعات" if lang=="ar" else "Sales records"),
        (f"{df_company['governorate'].nunique()}",
         "محافظات" if lang=="ar" else "Governorates"),
        (f"{df_company['product_name'].nunique()}",
         "منتجات" if lang=="ar" else "Products"),
        (f"{df_company['total_revenue_syp'].sum()/1e6:.1f}M",
         "إجمالي الإيرادات (ل.س)" if lang=="ar" else "Total Revenue (SYP)"),
    ]
    for col, (num, lbl) in zip([c1,c2,c3,c4], stats):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-num">{num}</div>
                <div class="kpi-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Data preview ──────────────────────────────────────────────
    preview_lbl = "#### معاينة البيانات" if lang=="ar" else "#### Data preview"
    with st.expander(preview_lbl, expanded=False):
        st.dataframe(df_company.head(10), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Analysis tabs ─────────────────────────────────────────────
    if lang == "ar":
        tabs_lbl = ["📍 المبيعات حسب المحافظة","📦 المبيعات حسب الفئة",
                    "📈 الإيرادات عبر الزمن","🏆 أفضل المنتجات","🔍 مقارنة مرجعية"]
    else:
        tabs_lbl = ["📍 Sales by Region","📦 Sales by Category",
                    "📈 Revenue Over Time","🏆 Top Products","🔍 Benchmark Comparison"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs_lbl)

    # Tab 1 — Sales by region
    with tab1:
        rev_region = (
            df_company.groupby("governorate")["total_revenue_syp"]
            .sum().sort_values(ascending=False).reset_index()
        )
        fig1 = px.bar(
            rev_region,
            x="governorate", y="total_revenue_syp",
            color="total_revenue_syp",
            color_continuous_scale="Blues",
            title="Total Revenue by Governorate (SYP)" if lang=="en" else "إجمالي الإيرادات حسب المحافظة (ل.س)",
            labels={"total_revenue_syp": "Revenue (SYP)", "governorate": "Governorate"},
        )
        fig1.update_layout(xaxis_tickangle=-45, height=420,
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

        # Table
        rev_region["total_revenue_syp"] = rev_region["total_revenue_syp"].apply(
            lambda x: f"{x:,.0f}"
        )
        st.dataframe(rev_region, use_container_width=True, hide_index=True)

    # Tab 2 — Sales by category
    with tab2:
        rev_cat = (
            df_company.groupby("category")["total_revenue_syp"]
            .sum().reset_index()
        )
        fig2 = px.pie(
            rev_cat, values="total_revenue_syp", names="category",
            title="Revenue Share by Category" if lang=="en" else "حصة الإيرادات حسب الفئة",
            color_discrete_sequence=["#2E7D32","#E65100","#1F4E79","#C62828"],
        )
        fig2.update_layout(height=420)
        st.plotly_chart(fig2, use_container_width=True)

    # Tab 3 — Revenue over time
    with tab3:
        df_monthly = (
            df_company.dropna(subset=["date"])
            .groupby(df_company["date"].dt.to_period("M"))["total_revenue_syp"]
            .sum().reset_index()
        )
        df_monthly["date"] = df_monthly["date"].astype(str)

        fig3 = px.line(
            df_monthly, x="date", y="total_revenue_syp",
            title="Monthly Revenue Trend (SYP)" if lang=="en" else "اتجاه الإيرادات الشهرية (ل.س)",
            labels={"total_revenue_syp": "Revenue (SYP)", "date": "Month"},
            markers=True,
        )
        fig3.update_traces(line_color="#2E75B6", line_width=2.5)
        fig3.update_layout(height=420,
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True)

    # Tab 4 — Top products
    with tab4:
        top_products = (
            df_company.groupby("product_name")
            .agg(total_revenue=("total_revenue_syp","sum"),
                 total_qty=("quantity_sold","sum"))
            .sort_values("total_revenue", ascending=False)
            .head(10).reset_index()
        )

        fig4 = px.bar(
            top_products, x="total_revenue", y="product_name",
            orientation="h",
            title="Top 10 Products by Revenue" if lang=="en" else "أفضل 10 منتجات حسب الإيراد",
            labels={"total_revenue": "Revenue (SYP)", "product_name": "Product"},
            color="total_revenue", color_continuous_scale="Greens",
        )
        fig4.update_layout(yaxis=dict(autorange="reversed"), height=420,
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # Tab 5 — Benchmark comparison
    with tab5:
        if lang == "ar":
            st.markdown("#### مقارنة محافظاتك بالمعايير الوطنية")
            st.markdown("""
            <div class="insight">
                تقارن هذه الخريطة محافظاتك التشغيلية بتصنيف دخول السوق الوطني.
                المحافظات ذات الدرجات المرتفعة تمتلك أفضل الظروف التجارية.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("#### Your governorates vs national market entry benchmark")
            st.markdown("""
            <div class="insight">
                This chart compares your operating governorates against the national
                market entry ranking. Higher-scoring governorates have the best
                commercial conditions.
            </div>
            """, unsafe_allow_html=True)

        if not data["scores"].empty:
            company_govs = df_company["governorate"].unique().tolist()
            scores_bench = data["scores"].copy()
            scores_bench["your_market"] = scores_bench["adm1_name"].isin(company_govs)
            scores_bench["bar_color"] = scores_bench["your_market"].map(
                {True: "#2E7D32", False: "#CCCCCC"}
            )

            fig5 = go.Figure(go.Bar(
                x=scores_bench["composite_score"],
                y=scores_bench["adm1_name"],
                orientation="h",
                marker_color=scores_bench["bar_color"],
                text=scores_bench["composite_score"].round(1),
                textposition="outside",
            ))
            fig5.update_layout(
                title="🟢 Your markets  |  ⬜ Other governorates" if lang=="en"
                      else "🟢 أسواقك  |  ⬜ محافظات أخرى",
                xaxis=dict(title="Market Entry Score (0–100)", range=[0,115]),
                yaxis=dict(autorange="reversed"),
                height=540,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=80, t=50, b=30),
            )
            st.plotly_chart(fig5, use_container_width=True)

            # Show scores for company's governorates
            comp_scores = scores_bench[scores_bench["your_market"]][
                ["adm1_name","segment_name","composite_score",
                 "score_purchasing","score_stability"]
            ].copy()
            comp_scores.columns = [
                "Governorate","Segment","Score","Purchasing Power","Price Stability"
            ]
            for c in ["Score","Purchasing Power","Price Stability"]:
                comp_scores[c] = comp_scores[c].round(1)

            if not comp_scores.empty:
                if lang == "ar":
                    st.markdown("#### درجات محافظاتك")
                else:
                    st.markdown("#### Your governorates scores")
                st.dataframe(comp_scores, use_container_width=True, hide_index=True)

                # Key insight
                best = comp_scores.sort_values("Score", ascending=False).iloc[0]
                if lang == "ar":
                    st.markdown(f"""
                    <div class="finding">
                        <b>🏆 أفضل سوق لديك: {best["Governorate"]}</b>
                        بدرجة {best["Score"]}/100 — {best["Segment"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="finding">
                        <b>🏆 Your strongest market: {best["Governorate"]}</b>
                        with score {best["Score"]}/100 — {best["Segment"]}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                if lang == "ar":
                    st.warning("لم يتم مطابقة أي محافظة في ملفك مع البيانات المرجعية. تحقق من تهجئة أسماء المحافظات.")
                else:
                    st.warning("No governorates in your file matched the benchmark data. Check governorate name spelling.")


def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "lang" not in st.session_state:
        st.session_state["lang"] = "en"

    if not st.session_state["logged_in"]:
        login_page()
        return

    data = load_data()
    sidebar()

# ── Top navigation bar — always visible, never collapsible ────
    # Pages available per role
    role = st.session_state.get("user_role", "Analyst")

    ALL_PAGES = [
        ("Home",              "🏠 Home"),
        ("Consumer Profiles", "👤 Profiles"),
        ("Geographic Maps",   "🗺️ Maps"),
        ("Price Intelligence","💰 Prices"),
        ("Forecasting",       "📈 Forecast"),
        ("Market Entry",      "🏆 Ranking"),
        ("Decision Support",  "🎯 Advisory"),
        ("Upload",            "📤 Upload"),
        ("Methodology",       "📖 Method"),
    ]

    COMPANY_PAGES = [
        ("Home",              "🏠 Home"),
        ("Geographic Maps",   "🗺️ Maps"),
        ("Price Intelligence","💰 Prices"),
        ("Market Entry",      "🏆 Ranking"),
        ("Decision Support",  "🎯 Advisory"),
        ("Upload",            "📤 Upload"),
    ]

    page_list   = COMPANY_PAGES if role == "Company" else ALL_PAGES
    page_keys   = [p[0] for p in page_list]
    lang        = st.session_state.get("lang", "en")
    # Use translated navigation labels
    all_labels_translated   = TRANS.get(lang, TRANS["en"])["nav"]
    comp_labels_translated  = TRANS.get(lang, TRANS["en"])["nav_company"]
    page_labels = comp_labels_translated if role == "Company" else all_labels_translated

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    # If current page not available for this role, reset to Home
    if st.session_state["page"] not in page_keys:
        st.session_state["page"] = "Home"
    current_idx = page_keys.index(st.session_state["page"])

    st.markdown("""
    <div style="background:#1a2744; padding:6px 16px; margin:-1rem -1rem 1.5rem;
         border-bottom:1px solid #2d4a7a;">
    </div>
    """, unsafe_allow_html=True)

    nav_col, user_col = st.columns([5, 1])

    with nav_col:
        chosen = st.radio(
            "Navigate",
            page_labels,
            index=current_idx,
            horizontal=True,
            label_visibility="collapsed",
            key="top_nav"
        )

    with user_col:
        lang       = st.session_state.get("lang", "en")
        role       = st.session_state.get("user_role", "")
        user_name  = st.session_state.get("user_name", "")
        role_color = {
            "Admin"  : "#C62828",
            "Company": "#2E7D32",
            "Analyst": "#1F4E79",
        }.get(role, "#888888")

        # Language toggle
        btn_label = "🌐 العربية" if lang == "en" else "🌐 English"
        col_lang, col_out = st.columns(2)
        with col_lang:
            if st.button(btn_label, key="lang_toggle",
                         use_container_width=True):
                st.session_state["lang"] = "ar" if lang == "en" else "en"
                st.rerun()
        with col_out:
            signout_label = "🚪 خروج" if lang == "ar" else "🚪 Sign Out"
            if st.button(signout_label, key="signout_top",
                         use_container_width=True):
                for k in ["logged_in","username","user_name","user_role","page"]:
                    st.session_state.pop(k, None)
                st.rerun()

        st.markdown(
            f'''<div style="text-align:right; padding-top:2px;">
            <div style="font-size:0.70rem; color:#666;">{user_name}</div>
            <span style="background:{role_color}; color:white;
                 font-size:0.66rem; padding:2px 8px;
                 border-radius:999px; font-weight:500;">
                {role}
            </span></div>''',
            unsafe_allow_html=True,
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
    elif page == "Upload":            page_upload(data)
    elif page == "Methodology":       page_methodology(data)

if __name__ == "__main__":
    main()
