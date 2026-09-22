import streamlit as st
import uuid 
from payment import SquarePaymentUI
from email_sender import EmailSender

st.set_page_config(page_title="Re-String Tennis Northern Beaches", layout="wide",page_icon='Logos.png')

string_options = {
    "-- Select --": 0,
    "Yonex Polytour Pro 1.25 - Purple - $30": 30,
    "Babolat RPM Blast 1.30 - Black - $30": 30,
    "Cheapest String - 1.30 - Black - $15": 15,
    "BYO String - $0": 0
}
payment_options = ["Card", "Cash"]
st.title("🎾 Northern Beaches Tennis Re-Stringing Services")

string = st.selectbox(label="String", options=string_options)
payment = st.selectbox(label="Payment Method", options=payment_options)
tension = st.number_input(label="Tension - Lbs", min_value=20, step=1, max_value=60, value=55)
delivery = st.selectbox(label="Delivery Method", options=["Drop off and Pickup - Address will be shared on email"])
receiver_email = st.text_input(label="Email Address")

# Initialize session state for persistence
if "proceed_to_payment" not in st.session_state:
    st.session_state.proceed_to_payment = False

# When the submit button is clicked, validate and lock the state to True
if st.button("Submit - Proceed to Payment"):
    if string == "-- Select --":
        st.warning("⚠️ Please select a valid string before proceeding.")
    elif not receiver_email.strip():
        st.warning("⚠️ Please enter your email address before proceeding.")
    else:
        st.session_state.proceed_to_payment = True

unique_id = str(uuid.uuid4())
amount = string_options[string] + 20
st.write(f"Total Amount: ${amount:.2f} AUD")
st.divider()

# Trigger payment module based on persistent session state instead of the raw button
if st.session_state.proceed_to_payment and string != "-- Select --" and receiver_email != "":
    if payment == "Card":
        # Render the payment UI module 
        SquarePaymentUI(
            amount=amount,
            currency="AUD", 
            description=f"Stringing service for {string} at {tension} lbs tension with delivery method: {delivery} for {receiver_email}."
        )
        # Check if payment outcome stored in session state is successful
        if st.session_state.get("outcome") == "ACCEPTED":
            email_sender = EmailSender()
            email_sender.send_email(receiver_email, string, tension, unique_id, amount)
            st.success(f"✅ Payment successful! An email will be sent to **{receiver_email}** with the payment receipt and instructions.")
            st.balloons()
            
    elif payment == "Cash":
        email_sender = EmailSender()
        email_sender.send_email(receiver_email, string, tension, unique_id, amount)
        st.success(f"✅ You have selected cash payment, an email will be sent to **{receiver_email}** with the payment instructions. The total amount to be paid is **${amount:.2f} AUD**.")
        st.balloons()
else:
    st.info("Please select a string, choose a payment method, provide your email address, and click submit to proceed.")
st.image("poweredbymatedata.png", width=400)