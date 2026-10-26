import streamlit as st
import urllib.parse


def show_escalation_card(company_name, contacts, customer_query):
    # Show a prominent alert banner
    st.error(
        f"⚠️ **Escalation Required:** This issue cannot be solved by automated FAQs and needs a human agent from **{company_name}**.")

    # Create a nice bordered card
    with st.container(border=True):
        st.subheader(f"🛡️ {company_name} Verified Human Support")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📞 Customer Care Number:**")
            st.code(contacts["phone"], language=None)

        with col2:
            st.markdown("**✉️ Official Support Email:**")
            st.code(contacts["email"], language=None)

        st.markdown("---")

        # Pre-fill the email subject and body with the customer's exact complaint
        subject = urllib.parse.quote(f"Urgent Support Escalation - {company_name}")
        body = urllib.parse.quote(
            f"Hello {company_name} Support Team,\n\n"
            f"I need urgent human assistance with the following issue:\n"
            f"\"{customer_query}\"\n\n"
            f"Please help resolve this as soon as possible.\nThank you."
        )
        mailto_url = f"mailto:{contacts['email']}?subject={subject}&body={body}"

        # Add two clickable action buttons side by side
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.link_button("✉️ One-Click Support Email", mailto_url, use_container_width=True)
        with btn_col2:
            st.link_button("🌐 Open Official Help Center", contacts["link"], use_container_width=True)