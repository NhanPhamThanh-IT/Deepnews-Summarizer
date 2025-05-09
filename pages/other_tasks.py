import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Other Tasks", page_icon="🛠️", layout="wide")

def display_other_tasks():
    st.header("Other Tasks")
    st.write("This page provides additional tools and functionalities.")

    # Hiển thị URL từ trang Scraper nếu có
    if 'shared_url' in st.session_state:
        st.markdown(f"**URL from Scraper**: {st.session_state.shared_url}")
    
    # Task 1: Text input and display
    st.subheader("Text Input")
    user_input = st.text_input("Enter some text:", placeholder="Type something...")
    if user_input:
        st.success(f"You entered: {user_input}")
    
    # Task 2: Simple calculator
    st.subheader("Simple Calculator")
    num1 = st.number_input("Enter first number:", value=0.0, step=0.1)
    num2 = st.number_input("Enter second number:", value=0.0, step=0.1)
    operation = st.selectbox("Select operation:", ["Add", "Subtract", "Multiply", "Divide"])
    
    if st.button("Calculate", key="calc_button"):
        if operation == "Add":
            result = num1 + num2
            st.success(f"Result: {num1} + {num2} = {result}")
        elif operation == "Subtract":
            result = num1 - num2
            st.success(f"Result: {num1} - {num2} = {result}")
        elif operation == "Multiply":
            result = num1 * num2
            st.success(f"Result: {num1} * {num2} = {result}")
        elif operation == "Divide":
            if num2 != 0:
                result = num1 / num2
                st.success(f"Result: {num1} / {num2} = {result}")
            else:
                st.error("Error: Division by zero is not allowed.")

def main():
    display_other_tasks()

if __name__ == "__main__":
    main()