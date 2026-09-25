import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Product Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CONFIGURATION
# ============================================================

FLASK_API_URL = st.secrets["FLASK_API_URL"]
GUEST_TOKEN_API = st.secrets["GUEST_TOKEN_API"]
SUPERSET_URL = st.secrets["SUPERSET_URL"]

SUPERSET_DASHBOARD_UUID = st.secrets["SUPERSET_DASHBOARD_UUID"]

# ============================================================
# PAGE CSS
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-left: 2.1rem !important;
            padding-right: 2.1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
        }

        .stApp {
            background: #f4f7fb;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        #MainMenu,
        footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        /* Hide Streamlit Deploy button */
        [data-testid="stDeployButton"] {
            display: none !important;
        }

        /* Hide Streamlit toolbar */
        [data-testid="stToolbar"] {
            visibility: hidden !important;
        }

        .dashboard-title {
            color: #173b70;
            font-size: 25px;
            font-weight: 800;
            margin-top: 4px;
            margin-bottom: 18px;
        }

        .dashboard-shell {
            width: 100%;
            background: white;
            border: 1px solid #e4e9f0;
            border-radius: 16px;
            padding: 6px;
            box-sizing: border-box;
            box-shadow: 0 7px 22px rgba(40,60,90,.07);
            overflow: hidden;
        }

        .section-gap {
            height: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div style="
        min-height:245px;
        padding:28px 44px 38px 44px;
        margin:0 0 36px 0;
        border-radius:0 0 26px 26px;
        background:linear-gradient(110deg,#172f68 0%,#164276 48%,#197a82 100%);
        box-shadow:0 18px 38px rgba(30,55,90,.18);
        color:white;
        box-sizing:border-box;
        font-family:Arial,sans-serif;
    ">
        <div style="
            font-size:15px;
            font-weight:700;
            letter-spacing:1.7px;
            text-transform:uppercase;
            opacity:.72;
            margin-bottom:42px;
        ">
            LIVE ANALYTICS PLATFORM
        </div>

        <div style="
            font-size:36px;
            line-height:1.15;
            font-weight:800;
            margin-bottom:13px;
        ">
            Product Performance Analytics
        </div>

        <div style="
            font-size:17px;
            line-height:1.5;
            opacity:.9;
            margin-bottom:25px;
        ">
            Product performance insights.
        </div>

        <div style="
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:9px 16px;
            border-radius:24px;
            background:rgba(255,255,255,.13);
            font-size:14px;
            font-weight:600;
        ">
            <span style="
                width:8px;
                height:8px;
                border-radius:50%;
                background:#d9f99d;
                display:inline-block;
            "></span>
            Live data
        </div>
    </div>
    """
)

# ============================================================
# API DATA
# ============================================================

@st.cache_data(ttl=60)
def get_categories():
    response = requests.get(
        f"{FLASK_API_URL}/api/product-performance/categories",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=60)
def get_top_products():
    response = requests.get(
        f"{FLASK_API_URL}/api/product-performance/top-selling-products",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=60)
def get_returns():
    response = requests.get(
        f"{FLASK_API_URL}/api/product-performance/returns",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


categories = []
top_products = []
returns = []
api_data_error = None

try:
    categories = get_categories()
    top_products = get_top_products()
    returns = get_returns()
except Exception as e:
    api_data_error = str(e)

# ============================================================
# DASHBOARD TITLE ONLY
# ============================================================

st.markdown(
    '<div class="dashboard-title">Analytics Dashboard</div>',
    unsafe_allow_html=True,
)

# ============================================================
# EMBEDDED SUPERSET DASHBOARD
# ============================================================

embed_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">

    <script src="https://unpkg.com/@superset-ui/embedded-sdk"></script>

    <style>
        * {{
            box-sizing: border-box;
        }}

        html,
        body {{
            margin: 0;
            padding: 0;
            width: 100%;
            min-width: 100%;
            height: 100%;
            background: white;
            overflow: hidden;
        }}

        #superset-container {{
            position: relative;
            width: 100% !important;
            min-width: 100% !important;
            max-width: none !important;
            height: 1320px;
            min-height: 1320px;
            background: white;
            overflow: hidden;
        }}

        #superset-container iframe {{
            display: block !important;
            width: 100% !important;
            min-width: 100% !important;
            max-width: none !important;
            height: 1320px !important;
            min-height: 1320px !important;
            border: 0 !important;
        }}

        #loading {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 100px;
            color: #607493;
            font-size: 17px;
        }}

        #error {{
            display: none;
            margin: 30px;
            padding: 22px;
            border-radius: 12px;
            background: #fff5f5;
            border: 1px solid #fecaca;
            color: #b91c1c;
            font-family: Arial, sans-serif;
            white-space: pre-wrap;
        }}
    </style>
</head>

<body>

    <div id="loading">
        Loading analytics dashboard...
    </div>

    <div id="error"></div>

    <div id="superset-container"></div>

    <script>
        const dashboardId = "{SUPERSET_DASHBOARD_UUID}";
        const supersetDomain = "{SUPERSET_URL}";
        const guestTokenUrl = "{GUEST_TOKEN_API}";

        async function fetchGuestToken() {{

            const response = await fetch(
                guestTokenUrl,
                {{
                    method: "GET",
                    headers: {{
                        "Accept": "application/json"
                    }}
                }}
            );

            if (!response.ok) {{
                const text = await response.text();

                throw new Error(
                    "Guest token request failed (" +
                    response.status +
                    "): " +
                    text
                );
            }}

            const data = await response.json();

            if (!data.token) {{
                throw new Error(
                    "Guest token was not returned by the service."
                );
            }}

            return data.token;
        }}

        function showError(error) {{

            document.getElementById(
                "loading"
            ).style.display = "none";

            const errorBox =
                document.getElementById("error");

            errorBox.style.display = "block";

            errorBox.textContent =
                "Dashboard unavailable\\n\\n" +
                error.message;
        }}

        async function loadDashboard() {{

            try {{

                if (
                    !window.supersetEmbeddedSdk ||
                    !window.supersetEmbeddedSdk.embedDashboard
                ) {{
                    throw new Error(
                        "Superset Embedded SDK could not be loaded."
                    );
                }}

                await window.supersetEmbeddedSdk.embedDashboard({{
                    id: dashboardId,
                    supersetDomain: supersetDomain,

                    mountPoint:
                        document.getElementById(
                            "superset-container"
                        ),

                    fetchGuestToken: fetchGuestToken,

                    dashboardUiConfig: {{
                        hideTitle: true,
                        hideTab: false,
                        hideChartControls: false,

                        filters: {{
                            visible: true,
                            expanded: false
                        }},

                        urlParams: {{
                            standalone: 3
                        }}
                    }}
                }});

                document.getElementById(
                    "loading"
                ).style.display = "none";

            }} catch (error) {{

                console.error(
                    "Superset embedding error:",
                    error
                );

                showError(error);
            }}
        }}

        loadDashboard();
    </script>

</body>
</html>
"""

st.markdown(
    '<div class="dashboard-shell">',
    unsafe_allow_html=True,
)

components.html(
    embed_html,
    height=1350,
    scrolling=False,
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)

# ============================================================
# OPTIONAL API RESULTS
# ============================================================

st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

with st.expander("View Analytics API Results", expanded=False):

    if api_data_error:
        st.warning(
            f"Unable to load analytics data: {api_data_error}"
        )

    tab1, tab2, tab3 = st.tabs(
        [
            "🏆 Top Selling Products",
            "↩️ Product Returns",
            "📦 Category Performance",
        ]
    )

    with tab1:
        if top_products:
            st.dataframe(
                pd.DataFrame(top_products),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No top-selling product data available.")

    with tab2:
        if returns:
            st.dataframe(
                pd.DataFrame(returns),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No return data available.")

    with tab3:
        if categories:
            st.dataframe(
                pd.DataFrame(categories),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No category data available.")

# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div style="
        text-align:center;
        color:#718096;
        font-size:13px;
        padding:25px 0 5px 0;
        font-family:Arial,sans-serif;
    ">
        Product Performance Analytics • Flask API • Apache Superset • Streamlit
    </div>
    """
)
