import streamlit as st

st.set_page_config(page_title="Concrete Mix Calculator", page_icon="🧱")

st.title("🧱 Concrete Mix Calculator with Cost")

# Mix ratios dictionary
ratios = {
    15: (1, 2, 4),
    20: (1, 1.5, 3),
    25: (1, 1, 2),
    30: (1, 0.75, 1.5),
    35: (1, 0.67, 1.33),
    40: (1, 0.5, 1)
}

# Default rates
cement_rate = 320.0
sand_rate = 60.0
agg_rate = 50.0

# -------- Private Cost Editor --------
st.sidebar.title("🔒 Admin Settings (Private)")
password = st.sidebar.text_input("Enter Password", type="password")

# Use st.secrets for deployment (set in Streamlit Cloud -> Secrets)
APP_PASSWORD = st.secrets.get("APP_PASSWORD", "mypassword")

if password == APP_PASSWORD:
    st.sidebar.success("✅ Admin Access Granted")
    cement_rate = st.sidebar.number_input("Cement per bag", value=cement_rate, step=10.0)
    sand_rate = st.sidebar.number_input("Sand per cft", value=sand_rate, step=1.0)
    agg_rate = st.sidebar.number_input("Aggregate per cft", value=agg_rate, step=1.0)
else:
    st.sidebar.info("Enter password to edit material costs (default rates will be used).")

# -------- Public Calculator --------
grade = st.selectbox("Select Concrete Grade", [15, 20, 25, 30, 35, 40])
volume = st.number_input("Enter Volume of Concrete (m³)", min_value=0.1, step=0.1)

if st.button("🔍 Calculate Mix"):
    c, s, a = ratios[grade]
    total = c + s + a

    # Dry volume = 1.54 * wet volume
    volume_cement = (c / total) * 1.54 * volume
    volume_sand = (s / total) * 1.54 * volume
    volume_agg = (a / total) * 1.54 * volume

    # Quantities
    cement_bags = (volume_cement * 1440) / 50
    sand_cft = volume_sand * 35.31
    agg_cft = volume_agg * 35.31

    # Costs
    cement_cost = cement_bags * cement_rate
    sand_cost = sand_cft * sand_rate
    agg_cost = agg_cft * agg_rate
    total_cost = cement_cost + sand_cost + agg_cost

    # Results
    st.subheader(f"Concrete Mix for **M{grade}** ({volume} m³)")
    st.metric("Cement", f"{cement_bags:.2f} bags", f"Rs. {cement_cost:,.2f}")
    st.metric("Sand", f"{sand_cft:.2f} cft", f"Rs. {sand_cost:,.2f}")
    st.metric("Aggregates", f"{agg_cft:.2f} cft", f"Rs. {agg_cost:,.2f}")
    st.success(f"👉 **Total Material Cost = Rs. {total_cost:,.2f}**")
