import os
import requests
from bs4 import BeautifulSoup

# 1. Create a 'data' folder to store each company's help articles
os.makedirs("data", exist_ok=True)


# 2. Function that uses BeautifulSoup to clean HTML into plain readable rules
def extract_clean_text_from_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove unwanted website clutter like scripts or menus
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.extract()

    # Extract each paragraph or FAQ block cleanly
    blocks = []
    for p in soup.find_all(["p", "li"]):
        text = p.get_text().strip()
        if len(text) > 20:
            blocks.append(text)
    return "\n\n".join(blocks)


# 3. Sample HTML Help Center pages for Amazon, Swiggy, and Flipkart
COMPANY_HTML_PAGES = {
    "amazon": """
    <html><body>
        <p>Password Reset: To reset your Amazon password, go to Login & Security, click Edit next to Password, and enter the OTP sent to your mobile number.</p>
        <p>Return Policy: Most items purchased on Amazon can be returned within 7 to 10 days of delivery. Go to Your Orders, select Return or Replace Items, and choose a pickup slot.</p>
        <p>Refund Timeline: Once your returned item is picked up, refunds to UPI or original payment methods take 3 to 5 business days to reflect in your bank account.</p>
        <p>Prime Membership Cancellation: Go to Your Prime Membership, click Manage Membership, and select End Membership. Unused membership fees may be refunded.</p>
    </body></html>
    """,

    "swiggy": """
    <html><body>
        <p>Order Cancellation: You can cancel a Swiggy order within 60 seconds of placing it for a full refund. After 60 seconds, cancellation charges may apply if the restaurant has started preparing food.</p>
        <p>Coupon Not Working: Ensure your cart total meets the minimum order value before taxes and that the promo code has not expired.</p>
        <p>Edit Delivery Address: You can change your delivery address from the Track Order screen only if the restaurant is within the serviceable radius of the new address.</p>
        <p>Swiggy One Membership: Swiggy One provides free delivery on eligible restaurants above Rs 199 and extra discounts on Instamart orders.</p>
    </body></html>
    """,

    "flipkart": """
    <html><body>
        <p>Track Order: Open the Flipkart app, go to My Orders, and tap on your product to view real-time courier tracking updates.</p>
        <p>Replacement Policy: Electronics and appliances with manufacturing defects are eligible for a 7-day service center replacement. Keep the original invoice and box intact.</p>
        <p>SuperCoins Usage: Flipkart SuperCoins can be redeemed at checkout or used for rewards. SuperCoins expire 1 year after the month they are credited.</p>
        <p>Change Mobile Number: Go to Account Settings, click Edit Profile, enter your new mobile number, and verify both the old and new numbers using OTP.</p>
    </body></html>
    """
}

# 4. Run the scraper and save the cleaned text files into the 'data' folder
if __name__ == "__main__":
    for company, html_content in COMPANY_HTML_PAGES.items():
        clean_text = extract_clean_text_from_html(html_content)
        file_path = f"data/{company}.txt"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(clean_text)

        print(f"Saved clean FAQ file for {company.capitalize()} -> {file_path}")

    print("\nAll company knowledge files are ready!")