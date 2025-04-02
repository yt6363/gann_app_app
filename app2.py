import streamlit as st

from date_sum_calculator import date_sum_calculator
from stock_price_calculators import stock_price_at_degree, degrees_from_stock_price
from events_workshops import events_workshops
from blog import blog
from planetary_ingress_date_generator import planetary_ingress_date_generator
from combined_page import combined_numerology_and_dob_analyzer
from orbital_and_gravitational_plotter import orbital_and_gravitational_plotter

# ---------------------------------------------------------------------
# 1) DUMMY USER DATABASE + MEMBERSHIP LOGIC
# ---------------------------------------------------------------------
# In production, store these in a real DB with hashed passwords
DUMMY_USERS_DB = {
    "alice@example.com": {
        "password": "password123",
        "user_name": "Alice",
        "subscription_plan": "PRO",  # or "PRO"
    },
    "bob@example.com": {
        "password": "p@ssw0rd",
        "user_name": "Bob",
        "subscription_plan": "FREE",
    },
}

def is_logged_in():
    """Check if user is logged in based on session state."""
    return st.session_state.get("logged_in", False) and "user_email" in st.session_state

def get_current_user():
    """Return current user data from DUMMY_USERS_DB, or {} if not logged in."""
    if not is_logged_in():
        return {}
    return DUMMY_USERS_DB.get(st.session_state["user_email"], {})

def get_user_name():
    return get_current_user().get("user_name", "User")

def get_user_subscription_plan():
    return get_current_user().get("subscription_plan", "FREE")

def is_subscriber():
    """Check if user subscription_plan == 'PRO'."""
    return (get_user_subscription_plan() == "PRO")

# Mock function to "verify" a Gumroad license key
def verify_gumroad_license(license_key):
    """
    In a real app, you'd call:
    requests.post("https://api.gumroad.com/v2/licenses/verify", data={...})
    For demo, we'll assume any license_key length >5 is valid and belongs to 'alice@example.com'
    """
    if license_key and len(license_key) > 5:
        return {
            "success": True,
            "purchase_email": "alice@example.com",  # or the email from Gumroad
            "subscription_active": True,
        }
    else:
        return {
            "success": False,
            "purchase_email": None,
            "subscription_active": False,
        }

# ---------------------------------------------------------------------
# 2) LOGIN, LOGOUT, AND SUBSCRIPTION PAGES
# ---------------------------------------------------------------------
def show_login_page():
    st.title("Login / Sign Up")
    st.write("Enter your email and password to log in. (Demo: alice@example.com / password123)")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in DUMMY_USERS_DB and DUMMY_USERS_DB[email]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email
            st.success("Logged in successfully as {}".format(DUMMY_USERS_DB[email]["user_name"]))
        else:
            st.error("Invalid email or password")

    if st.button("Cancel"):
        st.session_state["show_login"] = False

def manage_subscription_page():
    st.title("Manage Subscription (Gumroad)")

    if not is_logged_in():
        st.warning("You need to be logged in to manage subscriptions.")
        return

    user_plan = get_user_subscription_plan()
    st.write(f"**Current subscription plan:** {user_plan}")

    st.markdown("Enter your Gumroad license key below if you purchased PRO membership:")
    license_key = st.text_input("Gumroad License Key")

    if st.button("Activate License"):
        result = verify_gumroad_license(license_key)
        if result["success"]:
            purchase_email = result["purchase_email"]
            # Check if purchase_email matches the currently logged-in user
            if purchase_email == st.session_state["user_email"] and result["subscription_active"]:
                DUMMY_USERS_DB[purchase_email]["subscription_plan"] = "PRO"
                st.success("License verified! You are now a PRO member.")
            else:
                st.error("License verification failed or email mismatch.")
        else:
            st.error("Invalid license key or verification failed.")

def show_logout_button():
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_email"] = None
        st.sidebar.success("Logged out successfully.")
        st.stop()

# ---------------------------------------------------------------------
# 3) ORIGINAL APP CODE (WITH A FEW LINES ADDED FOR LOGIN/MEMBERSHIP)
# ---------------------------------------------------------------------
def original_app():
    # ------------- Your original styling --------------
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            font-size: 3em;
            margin-bottom: 0.1em;
            padding-bottom: 0.5em;
        }
        .bio {
            text-align: center;
            margin-top: 0.1em;
            margin-bottom: 0.1em;
        }
        .css-1aumxhk {
            display: none;
        }
        .sidebar-content .css-1aumxhk {
            font-size: 1em;
        }
        .bio-details {
            font-size: 1em;
            margin-bottom: 0.1em;
        }
        .bio-details a {
            font-size: 1em;
            margin-bottom: 0.1em;
        }
        .post {
            margin-top: 4em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

    # Custom CSS to increase font size of the sidebar navigation label
    st.sidebar.markdown(
        """
        <style>
        .css-1d391kg, .css-1d391kg span {
            font-size: 4em !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ----------- OUR NEW NAV OPTIONS -----------
    # We'll insert 2 new items for login and subscription
    # Everything else remains the same
    nav_options = [
        "Home",
        "Numerology & DOB Analyzer",
        "Planetary Ingress Dates",
        "Orbital & Gravitational Plotter",
        "Sum of Date Calculator",
        "Stock Price by Degree",  
        "Degrees from Stock Price",
        "Events & Workshops",
        "Resource Blog",
        "Login / Sign Up",          # <-- newly added
        "Manage Subscription",      # <-- newly added
    ]

    # Define all sidebar options directly with radio buttons
    app_selection = st.sidebar.radio(
        "Navigation",
        nav_options,
        index=0,
        key="app_selection",
    )

    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # If user is logged in, show a logout button and display user info
    if is_logged_in():
        show_logout_button()
        st.sidebar.write(f"**Logged in as:** {get_user_name()}")
        st.sidebar.write(f"**Plan:** {get_user_subscription_plan()}")

    # ------------- NAVIGATION LOGIC --------------
    if app_selection == "Home":
        # Keep Home public
        st.markdown('<div class="title">YASH NENI</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="bio">
            Time Student, Trader, Astrology and Numerology Enthusiast. Count your blessings only intend to put my thoughts and analysis, always trade at your own risk.
            <br><br>
            <span class="bio-details">
            Location: USA, NYC | 
            Email: <a href="mailto:yashnam15@gmail.com">yashnam15@gmail.com</a> | 
            <a href="https://x.com/YashNeni" target="_blank">X Profile</a>
            </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.components.v1.html(
            """
            <div class="twitter-container">
                <blockquote class="twitter-tweet">
                    <p lang="en" dir="ltr">
                        Either jan-feb 2025 or July 2025 <br>A good major top coming 
                        <a href="https://t.co/yiJPSA5YcJ">https://t.co/yiJPSA5YcJ</a> 
                        <a href="https://t.co/5y8xsI5t91">pic.twitter.com/5y8xsI5t91</a>
                    </p>
                    &mdash; Yash Neni (@YashNeni) 
                    <a href="https://twitter.com/YashNeni/status/1811999115384906052?ref_src=twsrc%5Etfw">July 13, 2024</a>
                </blockquote>
                <blockquote class="twitter-tweet">
                    <p lang="en" dir="ltr">You knew it before it happened, 9:47 exact top and 500 points clean swipe<br> 
                    <a href="https://twitter.com/hashtag/banknifty?src=hash&amp;ref_src=twsrc%5Etfw">#banknifty</a> 
                    <a href="https://twitter.com/hashtag/gann?src=hash&amp;ref_src=twsrc%5Etfw">#gann</a> 
                    <a href="https://twitter.com/hashtag/astro?src=hash&amp;ref_src=twsrc%5Etfw">#astro</a> 
                    <a href="https://twitter.com/hashtag/StockMarket?src=hash&amp;ref_src=twsrc%5Etfw">#StockMarket</a> 
                    <br><br>Like and retweet if it was helpful 
                    <a href="https://t.co/xnRfORVMAf">https://t.co/xnRfORVMAf</a> 
                    <a href="https://t.co/5O2TTs4GVh">pic.twitter.com/5O2TTs4GVh</a></p>
                    &mdash; Yash Neni (@YashNeni) 
                    <a href="https://twitter.com/YashNeni/status/1811618635275772359?ref_src=twsrc%5Etfw">July 12, 2024</a>
                </blockquote>
                <blockquote class="twitter-tweet">
                    <p lang="en" dir="ltr">Do I need to explain? <br>Exact 4:30 low and we are up 2600$ (4.4%) <br><br>Be Fearful When Others Are Greedy And Greedy When Others Are Fearful<br><br>I Didn’t anticipate this big move either. I am out of this trade, manage your risk from here on. 
                    <a href="https://twitter.com/hashtag/btc?src=hash&amp;ref_src=twsrc%5Etfw">#btc</a> 
                    <a href="https://twitter.com/hashtag/BITCOIN?src=hash&amp;ref_src=twsrc%5Etfw">#BITCOIN</a> 
                    <a href="https://twitter.com/hashtag/crypto_trading?src=hash&amp;ref_src=twsrc%5Etfw">#crypto_trading</a>
                    <a href="https://twitter.com/hashtag/astro?src=hash&amp;ref_src=twsrc%5Etfw">#astro</a> 
                    <a href="https://twitter.com/hashtag/gann?src=hash&amp;ref_src=twsrc%5Etfw">#gann</a> 
                    <a href="https://t.co/258hsXeDz2">https://t.co/258hsXeDz2</a> 
                    <a href="https://t.co/Vaghltel0w">pic.twitter.com/Vaghltel0w</a></p>
                    &mdash; Yash Neni (@YashNeni) 
                    <a href="https://twitter.com/YashNeni/status/1805448233969188904?ref_src=twsrc%5Etfw">June 25, 2024</a>
                </blockquote>
                <blockquote class="twitter-tweet"><p lang="en" dir="ltr">There is one day I am sure in next week, it can be a negative day <br><br>15 likes and 6 retweets <br><br>I will share it on my timeline. <a href="https://twitter.com/hashtag/Nifty?src=hash&amp;ref_src=twsrc%5Etfw">#Nifty</a> <a href="https://twitter.com/hashtag/gann?src=hash&amp;ref_src=twsrc%5Etfw">#gann</a> <a href="https://twitter.com/hashtag/markets?src=hash&amp;ref_src=twsrc%5Etfw">#markets</a> <a href="https://twitter.com/hashtag/StockMarket?src=hash&amp;ref_src=twsrc%5Etfw">#StockMarket</a></p>&mdash; Yashwanth Tatineni (@Yashneni) <a href="https://twitter.com/Yashneni/status/1811243048841380253?ref_src=twsrc%5Etfw">July 11, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
               <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Said it 9 days ago, Friday it is and there will be no support, we were ready for Friday from last week<br><br>We are 💲🧲 and 🥰🧲<br><br> <a href="https://twitter.com/hashtag/Nifty?src=hash&amp;ref_src=twsrc%5Etfw">#Nifty</a> <a href="https://twitter.com/hashtag/StockMarket?src=hash&amp;ref_src=twsrc%5Etfw">#StockMarket</a> <a href="https://twitter.com/hashtag/astro?src=hash&amp;ref_src=twsrc%5Etfw">#astro</a> <a href="https://twitter.com/hashtag/trading?src=hash&amp;ref_src=twsrc%5Etfw">#trading</a> <a href="https://t.co/WCtRTemEq2">https://t.co/WCtRTemEq2</a> <a href="https://t.co/tp0KIdRUN0">pic.twitter.com/tp0KIdRUN0</a></p>&mdash; Yashwanth Tatineni (@Yashneni) <a href="https://twitter.com/Yashneni/status/1814238227844251917?ref_src=twsrc%5Etfw">July 19, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
                <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Banknifty exact top at 11:38 and turned negative as predicted <a href="https://twitter.com/hashtag/Nifty?src=hash&amp;ref_src=twsrc%5Etfw">#Nifty</a> <a href="https://twitter.com/hashtag/astro?src=hash&amp;ref_src=twsrc%5Etfw">#astro</a> <a href="https://twitter.com/hashtag/thank?src=hash&amp;ref_src=twsrc%5Etfw">#thank</a> <a href="https://twitter.com/hashtag/you?src=hash&amp;ref_src=twsrc%5Etfw">#you</a> <a href="https://t.co/MEKEcES1bx">https://t.co/MEKEcES1bx</a> <a href="https://t.co/ulgGeOyait">pic.twitter.com/ulgGeOyait</a></p>&mdash; Yashwanth Tatineni (@Yashneni) <a href="https://twitter.com/Yashneni/status/1818172879894110566?ref_src=twsrc%5Etfw">July 30, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                <blockquote class="twitter-tweet"><p lang="qme" dir="ltr">🙏🏻✨🧿 <a href="https://t.co/wuo9N97t6g">https://t.co/wuo9N97t6g</a> <a href="https://t.co/clvYvH9SuK">pic.twitter.com/clvYvH9SuK</a></p>&mdash; Yashwanth Tatineni (@Yashneni) <a href="https://twitter.com/Yashneni/status/1818154311701963147?ref_src=twsrc%5Etfw">July 30, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                <blockquote class="twitter-tweet"><p lang="en" dir="ltr">As said 10:45 exact low and one way upside<br>clearly told both side but more towards positive side <a href="https://twitter.com/hashtag/nifty50?src=hash&amp;ref_src=twsrc%5Etfw">#nifty50</a> <a href="https://twitter.com/hashtag/banknifty?src=hash&amp;ref_src=twsrc%5Etfw">#banknifty</a> <a href="https://twitter.com/hashtag/StockMarket?src=hash&amp;ref_src=twsrc%5Etfw">#StockMarket</a> <a href="https://twitter.com/hashtag/astrology?src=hash&amp;ref_src=twsrc%5Etfw">#astrology</a> <a href="https://t.co/mL68GwIhVm">https://t.co/mL68GwIhVm</a> <a href="https://t.co/c7XAaJkCVe">pic.twitter.com/c7XAaJkCVe</a></p>&mdash; Yashwanth Tatineni (@Yashneni) <a href="https://twitter.com/Yashneni/status/1817808197270306990?ref_src=twsrc%5Etfw">July 29, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Universe is aligned for us to get rewarded both emotionally and financially 🙏🏻🧿 <br><br>Exact low 10:27 am <a href="https://twitter.com/hashtag/Nifty?src=hash&amp;ref_src=twsrc%5Etfw">#Nifty</a> <a href="https://twitter.com/hashtag/banknifty?src=hash&amp;ref_src=twsrc%5Etfw">#banknifty</a> <a href="https://twitter.com/hashtag/gann?src=hash&amp;ref_src=twsrc%5Etfw">#gann</a> <a href="https://twitter.com/hashtag/stock?src=hash&amp;ref_src=twsrc%5Etfw">#stock</a> <br><br>Like and retweet will be helpful 🙏🏻🧿 <a href="https://t.co/aIsXCoZsuq">https://t.co/aIsXCoZsuq</a> <a href="https://t.co/cV49lHXkWY">pic.twitter.com/cV49lHXkWY</a></p>&mdash; Yashwanth Tatineni (@Yashneni) <a href="https://twitter.com/Yashneni/status/1816369731110162765?ref_src=twsrc%5Etfw">July 25, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            </div>
            """,
            height=1800,
            scrolling=True,
        )

    elif app_selection == "Sum of Date Calculator":
        # Example gating: must be logged in, but plan doesn't matter
        if not is_logged_in():
            st.warning("Please log in to access Sum of Date Calculator.")
            st.stop()
        date_sum_calculator()

    elif app_selection == "Stock Price by Degree":
        # Example gating: must be PRO subscriber
        if not is_logged_in():
            st.warning("Please log in first.")
            st.stop()
        if not is_subscriber():
            st.error("This page requires a PRO subscription. Go to 'Manage Subscription' to upgrade.")
            st.stop()
        stock_price_at_degree()

    elif app_selection == "Degrees from Stock Price":
        # Suppose you allow any logged-in user
        if not is_logged_in():
            st.warning("Please log in first.")
            st.stop()
        degrees_from_stock_price()

    elif app_selection == "Events & Workshops":
        # Must be logged in
        if not is_logged_in():
            st.warning("Please log in first.")
            st.stop()
        events_workshops()

    elif app_selection == "Resource Blog":
        # Suppose you keep it public
        blog()

    elif app_selection == "Planetary Ingress Dates":
        if not is_logged_in():
            st.warning("Please log in first.")
            st.stop()
        planetary_ingress_date_generator()

    elif app_selection == "Numerology & DOB Analyzer":
        if not is_logged_in():
            st.warning("Please log in to access.")
            st.stop()
        combined_numerology_and_dob_analyzer()

    elif app_selection == "Orbital & Gravitational Plotter":
        if not is_logged_in():
            st.warning("Please log in to access.")
            st.stop()
        orbital_and_gravitational_plotter()

    elif app_selection == "Login / Sign Up":
        # Show login page if user not logged in
        if is_logged_in():
            st.info("You are already logged in.")
        else:
            show_login_page()

    elif app_selection == "Manage Subscription":
        manage_subscription_page()

# ---------------------------------------------------------------------
# 4) MAIN WRAPPER
# ---------------------------------------------------------------------
def main():
    # Initialize session variables if not present
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None
    if "show_login" not in st.session_state:
        st.session_state["show_login"] = False

    # Run the original app with membership changes
    original_app()

if __name__ == "__main__":
    main()
