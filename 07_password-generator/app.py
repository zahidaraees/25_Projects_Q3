import streamlit as st
import random
import string
import io

# Function to generate one password with enforced character types and exclusion of similar chars
def generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_similar):
    if exclude_similar:
        upper_chars = ''.join(c for c in string.ascii_uppercase if c not in "O")
        lower_chars = ''.join(c for c in string.ascii_lowercase if c not in "ilo")
        digits = ''.join(c for c in string.digits if c not in "01")
    else:
        upper_chars = string.ascii_uppercase
        lower_chars = string.ascii_lowercase
        digits = string.digits

    symbols = string.punctuation

    character_pool = ""
    required_chars = []

    if use_upper:
        character_pool += upper_chars
        required_chars.append(random.choice(upper_chars))
    if use_lower:
        character_pool += lower_chars
        required_chars.append(random.choice(lower_chars))
    if use_digits:
        character_pool += digits
        required_chars.append(random.choice(digits))
    if use_symbols:
        character_pool += symbols
        required_chars.append(random.choice(symbols))

    if not character_pool:
        return "Please select at least one character set!", 0

    remaining_length = length - len(required_chars)
    if remaining_length < 0:
        return "Password length too short for selected options!", 0

    random_chars = [random.choice(character_pool) for _ in range(remaining_length)]
    full_password = required_chars + random_chars
    random.shuffle(full_password)
    password = ''.join(full_password)

    strength_score = calculate_strength(length, use_upper, use_lower, use_digits, use_symbols)
    return password, strength_score

# Calculate password strength
def calculate_strength(length, upper, lower, digits, symbols):
    score = 0
    if length >= 12:
        score += 1
    if upper:
        score += 1
    if lower:
        score += 1
    if digits:
        score += 1
    if symbols:
        score += 1
    return score

# Strength label
def strength_label(score):
    if score <= 2:
        return "Weak", "red"
    elif score == 3:
        return "Moderate", "orange"
    else:
        return "Strong", "green"

# Streamlit UI
st.title("🔐 Advanced Password Generator")

st.sidebar.header("Password Settings")
num_passwords = st.sidebar.number_input("Number of passwords to generate", min_value=1, max_value=100, value=1)
min_length = st.sidebar.slider("Minimum length", min_value=4, max_value=50, value=12)
max_length = st.sidebar.slider("Maximum length", min_value=min_length, max_value=100, value=16)

use_upper = st.sidebar.checkbox("Include uppercase letters", value=True)
use_lower = st.sidebar.checkbox("Include lowercase letters", value=True)
use_digits = st.sidebar.checkbox("Include digits", value=True)
use_symbols = st.sidebar.checkbox("Include symbols", value=True)

exclude_similar = st.sidebar.checkbox("Exclude similar characters (1, l, I, 0, O)", value=False)

if st.button("Generate Passwords"):
    results = []
    for _ in range(num_passwords):
        random_length = random.randint(min_length, max_length)
        password, score = generate_password(
            random_length,
            use_upper,
            use_lower,
            use_digits,
            use_symbols,
            exclude_similar
        )
        label, color = strength_label(score)
        results.append((password, label, color))

    for i, (pwd, label, color) in enumerate(results, 1):
        st.markdown(f"**Password {i}:** `{pwd}`")
        st.markdown(f"<span style='color:{color}; font-weight:bold;'>Strength: {label}</span><hr>", unsafe_allow_html=True)

    all_passwords = '\n'.join(pwd for pwd, _, _ in results)
    st.download_button(
        label="📥 Download All Passwords",
        data=all_passwords,
        file_name="passwords.txt",
        mime="text/plain"
    )
