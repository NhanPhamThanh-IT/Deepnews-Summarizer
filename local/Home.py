import streamlit as st

if __name__ == "__main__":
    st.set_page_config(page_title="Trang Chính", page_icon="🏠")

    st.title("🏠 Trang chính")
    st.write("Chào mừng đến với ứng dụng Streamlit! Dưới đây là hai chức năng chính:")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📰 Tin tức hàng ngày")
        st.write("📅 Tự động cập nhật các bản tin mới nhất mỗi ngày.")
        st.markdown("""
        **Tính năng:**
        - Tổng hợp từ nhiều nguồn đáng tin cậy
        - Hiển thị theo thứ tự thời gian
        - Giao diện đơn giản, dễ đọc
        """)
        if st.button("🔎 Vào Tin tức hàng ngày"):
            st.switch_page("pages/Daily_News.py")

    with col2:
        st.subheader("🔍 Tìm kiếm tùy chỉnh")
        st.write("🎯 Lọc và tìm kiếm tin tức theo ý bạn.")
        st.markdown("""
        **Tính năng:**
        - Nhập từ khóa để tìm tin liên quan
        - Chọn ngày, danh mục, nguồn
        - Giao diện tương tác
        """)
        if st.button("🔧 Vào Tìm kiếm tùy chỉnh"):
            st.switch_page("pages/Custom_Fetch.py")