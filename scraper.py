import os
from bs4 import BeautifulSoup
from vector_store import build_vector_db

os.makedirs("data", exist_ok=True)

def extract_clean_text_from_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.extract()
    blocks = []
    for p in soup.find_all(["p", "li"]):
        text = p.get_text().strip()
        if len(text) > 20:
            blocks.append(text)
    return "\n\n".join(blocks)


COMPANY_HTML_PAGES = {
    "amazon": """
    <html><body>
        <p>Password Reset: Go to Login & Security, click Edit next to Password, and enter the OTP sent to your mobile number.</p>
        <p>Return Policy: Most items can be returned within 7 to 10 days of delivery via Your Orders > Return or Replace Items.</p>
        <p>Refund Timeline: Refunds to UPI take 3 to 5 business days after the returned item is picked up.</p>
        <p>Prime Cancellation: Go to Your Prime Membership > Manage Membership > End Membership.</p>
    </body></html>
    """,
    "flipkart": """
    <html><body>
        <p>Track Order: Open the Flipkart app, go to My Orders, and select your item to see live courier tracking.</p>
        <p>Replacement Policy: Defective electronics are eligible for 7-day replacement with original box and invoice.</p>
        <p>SuperCoins: SuperCoins can be used at checkout and expire 1 year after being credited.</p>
        <p>Change Mobile Number: Go to Account Settings > Edit Profile and verify using OTP.</p>
    </body></html>
    """,
    "swiggy": """
    <html><body>
        <p>Order Cancellation: Cancel within 60 seconds of placing the order for a full refund. After 60 seconds, cancellation fees apply.</p>
        <p>Coupon Not Working: Check that your cart value meets the minimum requirement before taxes.</p>
        <p>Edit Address: Address can be changed from Track Order only if the new location is within the restaurant's delivery radius.</p>
    </body></html>
    """,
    "zomato": """
    <html><body>
        <p>Zomato Gold Benefits: Enjoy free delivery on eligible restaurants within 7 km and up to 40% extra dining-out discounts.</p>
        <p>Cancel Order: Orders can only be cancelled within 1 minute of placement before the restaurant accepts them.</p>
        <p>Refund Status: Approved refunds to UPI are processed instantly or within 24 to 48 hours.</p>
    </body></html>
    """,
    "uber": """
    <html><body>
        <p>Cancel Ride Fee: A cancellation fee applies if you cancel more than 2 minutes after a driver accepts your trip.</p>
        <p>Lost Item in Cab: Go to Your Trips, select the ride, tap Find Lost Item, and choose Contact Driver about a lost item.</p>
        <p>Change Payment Method: You can switch between Cash, UPI, and Card before the ride ends in the Uber app.</p>
    </body></html>
    """,
    "ola": """
    <html><body>
        <p>Ola Money Refund: Refunds credited to Ola Money wallet appear within 24 hours; bank refunds take 3 to 7 working days.</p>
        <p>Driver Verification OTP: Always share the 4-digit start code with your Ola driver only after boarding the cab.</p>
        <p>Download Ride Invoice: Go to Your Rides, select the completed trip, and tap Email Invoice.</p>
    </body></html>
    """,
    "paytm": """
    <html><body>
        <p>Pending UPI Payment: If money is deducted but payment shows pending, banks automatically settle or refund it within 48 hours (T+2 days).</p>
        <p>Reset UPI PIN: Go to UPI & Payment Settings, select your bank account, click Change/Reset UPI PIN, and enter debit card details or Aadhaar OTP.</p>
        <p>FASTag Balance: Paytm FASTag status and toll deductions can be viewed under Manage FASTag in the app.</p>
    </body></html>
    """,
    "phonepe": """
    <html><body>
        <p>Failed Transaction Refund: If money was debited for a failed UPI transaction, it is automatically refunded to your bank account within 3 to 5 days.</p>
        <p>Check Bank Balance: Tap Check Balance on the PhonePe home screen, select your linked bank, and enter your UPI PIN.</p>
        <p>Unlink Bank Account: Go to Profile > Payment Methods > Select Bank Account > Scroll down and tap Unlink Bank Account.</p>
    </body></html>
    """,
    "netflix": """
    <html><body>
        <p>Cancel Subscription: Go to Account, click Cancel Membership under Membership & Billing. Your access continues until the end of the billing cycle.</p>
        <p>Household Device Limit: To update your Netflix Household, open Netflix on your primary TV and select Confirm or Update Netflix Household.</p>
        <p>Reset Password: Visit netflix.com/loginhelp to receive a password reset link via email or SMS.</p>
    </body></html>
    """,
    "jio": """
    <html><body>
        <p>Check Data Balance: Open the MyJio app or dial 1299 from your Jio number to receive an SMS with your active plan and remaining daily data.</p>
        <p>Activate eSIM: Send SMS GETESIM <32-digit EID> <15-digit IMEI> to 199 from your Jio number and follow the email verification steps.</p>
        <p>5G Welcome Offer: Ensure 5G network mode is enabled in your phone settings and you have an active plan of Rs 239 or above.</p>
    </body></html>
    """
}

if __name__ == "__main__":
    for company, html_content in COMPANY_HTML_PAGES.items():
        clean_text = extract_clean_text_from_html(html_content)
        with open(f"data/{company}.txt", "w", encoding="utf-8") as file:
            file.write(clean_text)
        print(f"Saved FAQ file -> data/{company}.txt")

    # Automatically rebuild the Vector Database for all 10 companies!
    build_vector_db()
    print("\nAll 10 companies indexed into vector_db.json!")