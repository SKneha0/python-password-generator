import streamlit as st
import random
import string
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SecurePass Generator",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded"
)


def local_css():
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .password-display {
        background-color: #ffffff;
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 20px;
        text-align: center;
        margin-bottom: 20px;
        position: relative;
    }
    .password-display.dark {
        background-color: #2b2b2b;
        border: 1px solid #444444;
        color: #ffffff;
    }
    .strength-meter {
        height: 10px;
        border-radius: 5px;
        margin-top: 10px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .very-weak {
        background: linear-gradient(90deg, #ff4e50 0%, #ff4e50 100%);
    }
    .weak {
        background: linear-gradient(90deg, #ff4e50 0%, #f9d423 100%);
    }
    .medium {
        background: linear-gradient(90deg, #f9d423 0%, #f9d423 100%);
    }
    .strong {
        background: linear-gradient(90deg, #f9d423 0%, #00b09b 100%);
    }
    .very-strong {
        background: linear-gradient(90deg, #00b09b 0%, #00b09b 100%);
    }
    .dark-mode {
        background-color: #121212;
        color: #ffffff;
    }
    .light-mode {
        background-color: #f8f9fa;
        color: #000000;
    }
    .history-item {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .history-item.dark {
        background-color: #2b2b2b;
    }
    .history-item.light {
        background-color: #ffffff;
        border: 1px solid #d3d3d3;
    }
    .password-text {
        font-family: 'Courier New', monospace;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        max-width: 70%;
    }
    .timestamp {
        font-size: 12px;
        color: #888888;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'password_history' not in st.session_state:
    st.session_state.password_history = []
    
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
    
if 'current_password' not in st.session_state:
    st.session_state.current_password = ""
    
if 'copy_success' not in st.session_state:
    st.session_state.copy_success = False

# Function to generate password
def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special):
    # Ensure at least one character type is selected
    if not any([use_uppercase, use_lowercase, use_digits, use_special]):
        st.error("Please select at least one character type.")
        return ""
    
    # Define character sets
    chars = ""
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation
    
    # Generate password
    password = ''.join(random.choice(chars) for _ in range(length))
    
    # Ensure the password contains at least one of each selected character type
    while use_uppercase and not any(c.isupper() for c in password) or \
          use_lowercase and not any(c.islower() for c in password) or \
          use_digits and not any(c.isdigit() for c in password) or \
          use_special and not any(c in string.punctuation for c in password):
        password = ''.join(random.choice(chars) for _ in range(length))
    
    return password

# Function to calculate password strength
def calculate_strength(password):
    score = 0
    
    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    
    # Character variety checks
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    
    # Classify strength
    if score == 0:
        return "very-weak", "Very Weak"
    elif score <= 2:
        return "weak", "Weak"
    elif score <= 4:
        return "medium", "Medium"
    elif score <= 5:
        return "strong", "Strong"
    else:
        return "very-strong", "Very Strong"

# Function to add password to history
def add_to_history(password):
    if password and password not in [item["password"] for item in st.session_state.password_history]:
        st.session_state.password_history.insert(0, {
            "password": password,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "strength": calculate_strength(password)[1]
        })
        # Keep only the last 10 passwords
        if len(st.session_state.password_history) > 10:
            st.session_state.password_history.pop()

# Function to toggle theme
def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# Apply CSS
local_css()

# Main app
def main():
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # Theme toggle
        theme_col1, theme_col2 = st.columns([3, 1])
        with theme_col1:
            st.write("Theme:")
        with theme_col2:
            if st.button("🌓" if st.session_state.theme == "light" else "☀️"):
                toggle_theme()
        
        # Password settings
        st.subheader("Password Options")
        
        length = st.slider("Password Length", min_value=4, max_value=32, value=16, step=1)
        
        use_uppercase = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
        use_lowercase = st.checkbox("Include Lowercase Letters (a-z)", value=True)
        use_digits = st.checkbox("Include Numbers (0-9)", value=True)
        use_special = st.checkbox("Include Special Characters (!@#$)", value=True)
        
        # Generate button
        if st.button("🔄 Generate Password", key="generate"):
            password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
            if password:
                st.session_state.current_password = password
                add_to_history(password)
        
        # About section
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **SecurePass Generator** is a tool for creating strong, 
        random passwords to enhance your online security.
      
        """)

    # Main content
    st.title("🔐 SecurePass Generator")
    
    # Display header
    st.markdown("### Generate strong, secure passwords instantly")
    st.markdown("""
    Use this tool to create random passwords that are difficult to crack.
    Customize your password with various options and copy it with one click.
    """)
    
    # Password display
    st.markdown("### Your Password")
    
    # Password box
    password_class = "password-display dark" if st.session_state.theme == "dark" else "password-display"
    
    if st.session_state.current_password:
        # Calculate password strength
        strength_class, strength_text = calculate_strength(st.session_state.current_password)
        
        # Display password
        st.code(st.session_state.current_password, language=None)
        
        # Strength meter
        st.markdown(f"**Password Strength:** {strength_text}")
        st.markdown(f'<div class="strength-meter {strength_class}"></div>', unsafe_allow_html=True)
        
        # Copy instructions
        st.info("To copy: Select the password above and press Ctrl+C (or Cmd+C on Mac)")
        
    else:
        st.info("Click 'Generate Password' to create a new password")
    
    # Password history
    st.markdown("### Password History")
    
    if st.session_state.password_history:
        for i, item in enumerate(st.session_state.password_history):
            item_class = "history-item dark" if st.session_state.theme == "dark" else "history-item light"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(item['password'])
                st.caption(f"{item['timestamp']} • Strength: {item['strength']}")
            with col2:
                if st.button("Use", key=f"use_{i}"):
                    st.session_state.current_password = item["password"]
                    st.rerun()
    else:
        st.info("No password history yet. Generate your first password!")
    
    # Tips for secure passwords
    with st.expander("Tips for Secure Passwords"):
        st.markdown("""
        ### Password Security Tips
        
        1. **Use long passwords** - Aim for at least 12 characters
        2. **Mix character types** - Include uppercase, lowercase, numbers, and symbols
        3. **Avoid personal information** - Don't use names, birthdays, or common words
        4. **Use different passwords** for different accounts
        5. **Consider a password manager** to store your complex passwords securely
        """)

# Run the app
if __name__ == "__main__":
    main()