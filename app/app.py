import streamlit as st
import uuid
from payment import SquarePaymentUI
from email_sender import EmailSender

st.set_page_config(
    page_title="Re-String Tennis Northern Beaches",
    layout="centered",
    page_icon="profile.png",
)
import base64
from pathlib import Path

@st.cache_data
def img_to_base64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()

logo_b64 = img_to_base64("profile.png")

# ---------- Styling ----------
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {max-width: 820px; padding-top: 2rem;}

    .hero {
        background: linear-gradient(135deg, #0f5132 0%, #2e8b57 60%, #c6e03a 130%);
        color: white; padding: 2rem 2rem 1.6rem; border-radius: 18px;
        margin-bottom: 1.2rem; box-shadow: 0 8px 24px rgba(15,81,50,.25);
    }
    .hero h1 {margin: 0 0 .3rem; font-size: 2rem; color: white;}
    .hero p {margin: 0; font-size: 1.05rem; opacity: .95;}
    .hero-top {display: flex; align-items: center; gap: 1rem; margin-bottom: .6rem;}
    .hero-logo {
        width: 72px; height: 72px; border-radius: 50%; object-fit: cover;
        border: 3px solid rgba(255,255,255,.85);
        box-shadow: 0 4px 12px rgba(0,0,0,.25);
        flex-shrink: 0;
    }
    .hero-top h1 {margin: 0;}

    .badges {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: .6rem;
    margin-bottom: 1.2rem;
    }
    .badge {
        background: #f4f9f6; border: 1px solid #d5e8dd;
        border-radius: 12px; padding: .7rem .4rem; text-align: center; color: #1b4332;
        font-size: .8rem; line-height: 1.25;
    }
    .badge span {display: block; font-size: 1.4rem; margin-bottom: .2rem;}

    .summary {
        background: #f4f9f6; border: 1px solid #d5e8dd; border-radius: 12px;
        padding: 1rem 1.2rem; color: #1b4332;
    }
    .summary .row {display: flex; justify-content: space-between; padding: .15rem 0;}
    .summary .total {
        border-top: 1px dashed #9cc5ad; margin-top: .5rem; padding-top: .5rem;
        font-weight: 700; font-size: 1.15rem;
    }
    div.stButton > button {
        width: 100%; border-radius: 10px; padding: .7rem 1rem;
        font-weight: 600; font-size: 1.05rem;
    }
    .footer-note {text-align: center; color: #6b7c74; font-size: .85rem; margin-top: 1rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Data ----------
string_options = {
    "-- Select --": 0,
    "Yonex Polytour Pro 1.25 - Purple - $30": 30,
    "Babolat RPM Blast 1.30 - Black - $30": 30,
    "Cheapest String - 1.30 - Black - $15": 15,
    "BYO String - $0": 0,
}
payment_options = ["Card", "Cash"]
LABOUR = 20

# ---------- Session state ----------
if "proceed_to_payment" not in st.session_state:
    st.session_state.proceed_to_payment = False
if "unique_id" not in st.session_state:
    st.session_state.unique_id = str(uuid.uuid4())   # stable across reruns
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# ---------- Hero + trust ----------
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-top">
            <img class="hero-logo" src="data:image/png;base64,{logo_b64}" alt="Logo">
            <h1> Northern Beaches Re-Stringing</h1>
        </div>
        <p>Your racquet, strung with care by a local player who knows the game.
        Fresh strings, accurate tension, and a smooth, hassle-free booking.</p>
    </div>
    <div class="badges">
        <div class="badge"><span>🎯</span>Precise tension,<br>every time</div>
        <div class="badge"><span>⚡</span>Quick turnaround</div>
        <div class="badge"><span>🔒</span>Secure payments<br>via Square</div>
        <div class="badge"><span>💵</span>Pay by card<br>or cash on pickup</div>
        <div class="badge"><span>📧</span>Instant email<br>confirmation</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    "**You're in good hands.** Every racquet is strung on a quality machine, "
    "tension is double-checked before handover, and you'll get a receipt and clear "
    "drop-off/pick-up instructions straight to your inbox. If anything isn't right, "
    "just reply to your confirmation email and we'll sort it out."
)

# ---------- Form ----------
with st.container(border=True):
    st.subheader("1. Your racquet")
    string = st.selectbox("String", options=list(string_options))
    tension = st.number_input("Tension (lbs)", min_value=20, max_value=60, step=1, value=55)

    st.subheader("2. Your details")
    col1, col2 = st.columns(2)
    with col1:
        receiver_email = st.text_input("Email address", placeholder="you@example.com")
    with col2:
        payment = st.selectbox("Payment method",payment_options,help="Not comfortable paying online? No problem. Choose Cash and pay when you drop off or pick up.")
    delivery = st.selectbox(
        "Delivery method",
        ["Drop off and Pickup - Address will be shared on email"],
    )
if payment == "Card":
    st.caption("💵 Prefer not to pay online? Select **Cash** above and pay in person. No card needed.")
else:
    st.caption("💵 Cash selected. You'll pay when you drop off or pick up your racquet.")
amount = string_options[string] + LABOUR

# ---------- Price summary ----------
st.markdown(
    f"""
    <div class="summary">
        <div class="row"><span>String</span><span>${string_options[string]:.2f}</span></div>
        <div class="row"><span>Stringing service</span><span>${LABOUR:.2f}</span></div>
        <div class="row total"><span>Total</span><span>${amount:.2f} AUD</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

if st.button("Submit - Proceed to Payment", type="primary"):
    if string == "-- Select --":
        st.warning("⚠️ Please select a valid string before proceeding.")
    elif not receiver_email.strip():
        st.warning("⚠️ Please enter your email address before proceeding.")
    else:
        st.session_state.proceed_to_payment = True

st.divider()

# ---------- Payment flow ----------
unique_id = st.session_state.unique_id
ready = st.session_state.proceed_to_payment and string != "-- Select --" and receiver_email.strip() != ""

if ready:
    if payment == "Card":
        SquarePaymentUI(
            amount=amount,
            currency="AUD",
            description=f"Stringing service for {string} at {tension} lbs tension with delivery method: {delivery} for {receiver_email}.",
        )
        if st.session_state.get("outcome") == "ACCEPTED":
            if not st.session_state.email_sent:
                EmailSender().send_email(receiver_email, string, tension, unique_id, amount)
                st.session_state.email_sent = True
            st.success(
                f"✅ Payment successful! An email will be sent to **{receiver_email}** with the "
                "payment receipt and instructions. Please check your spam folder if you can't find it."
            )
            st.balloons()

    elif payment == "Cash":
        if not st.session_state.email_sent:
            EmailSender().send_email(receiver_email, string, tension, unique_id, amount)
            st.session_state.email_sent = True
        st.success(
            f"✅ You have selected cash payment. An email will be sent to **{receiver_email}** "
            f"with the payment instructions. The total to be paid is **${amount:.2f} AUD**."
        )
        st.balloons()
else:
    st.info("Select a string, choose a payment method, enter your email, then click submit to continue.")

# ---------- FAQ ----------
st.subheader("Good to know")
with st.expander("What tension should I choose?"):
    st.write("55 lbs is a solid all-round default. Lower tension gives more power and comfort; "
             "higher gives more control. Not sure? Stick with what you've used before.")
with st.expander("How does drop-off and pick-up work?"):
    st.write("After booking, you'll receive an email with the address and timing details.")
with st.expander("Is my payment secure?"):
    st.write("Yes. Card payments are processed by Square, and your card details are never stored on this site.")
with st.expander("Can I bring my own string?"):
    st.write("Absolutely, choose **BYO String** and you'll only pay the stringing service fee.")

# ---------- Footer ----------
st.write("")
_, mid, _ = st.columns([1, 2, 1])
with mid:
    st.image("poweredbymatedata.png", use_container_width=True)
st.markdown('<p class="footer-note">Locally run · Northern Beaches, Sydney</p>', unsafe_allow_html=True)