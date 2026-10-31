
import streamlit as st
from database import register_user, authenticate_user


def render_auth_page():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a, #1e1b4b);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='text-align:center;color:#38BDF8;'>"
        "CareerMate-AI 🚀</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#CBD5E1;'>"
        "Your AI-powered career companion</p>",
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Welcome Back!")

        with st.form("login_form"):
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input(
                "Password", type="password", key="login_password"
            )
            login_submit = st.form_submit_button(
                "Login", use_container_width=True
            )

        if login_submit:
            if not login_email.strip() or not login_password:
                st.error("Please enter both email and password.")
            else:
                success, message, user = authenticate_user(
                    login_email, login_password
                )

                if success and user:
                    st.session_state.is_authenticated = True
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.user_id = user["id"]
                    st.session_state.username = user.get("name", "Student User")
                    st.session_state.profile = user
                    st.session_state.active_page = "Dashboard"

                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(message)

    with register_tab:
        st.subheader("Create Your Account")

        with st.form("register_form"):
            name = st.text_input("Full Name", key="register_name")
            email = st.text_input("Email Address", key="register_email")
            password = st.text_input(
                "Create Password",
                type="password",
                key="register_password",
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="confirm_password",
            )
            education = st.selectbox(
                "Education",
                ["B.Tech", "B.E.", "B.Sc.", "M.Tech", "Other"],
            )
            branch = st.text_input(
                "Branch / Specialization",
                value="Computer Science & Engineering",
            )
            graduation_year = st.selectbox(
                "Graduation Year",
                ["2026", "2027", "2028", "2029", "2030", "Other"],
            )
            interests = st.text_input(
                "Career Interests",
                value="Artificial Intelligence, Web Development",
            )

            register_submit = st.form_submit_button(
                "Create Account", use_container_width=True
            )

        if register_submit:
            if not name.strip() or not email.strip() or not password:
                st.error("Please fill in your name, email, and password.")
            elif "@" not in email or "." not in email.rsplit("@", 1)[-1]:
                st.error("Please enter a valid email address.")
            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message, user = register_user(
                    name=name,
                    email=email,
                    password=password,
                    education=education,
                    branch=branch,
                    graduation_year=graduation_year,
                    interests=interests,
                )

                if success and user:
                    st.success(
                        "Account created successfully! Please use the Login tab to sign in."
                    )
                else:
                    st.error(message)

    st.markdown("---")
    st.caption("Developed by Upputuri Srilakshmihari")
