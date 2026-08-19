import streamlit as st
import numpy as np
import pandas as pd

class StreamlitHelper:
    def __init__(self):
        pass

    def get_columns(self, *names):
        len_args = len(names)
        columns = st.columns(len_args)
        for name, col in zip(names, columns):
            with col:
                # do something
                pass



def run():
    st.set_page_config(
        page_title="My App",
        layout="wide")
    st.header("Sử dụng `st.columns`")


    col1, col2, col3 = st.columns(3) # Chia thành 3 cột bằng nhau

    with col1:
        st.subheader("Cột 1")
        st.write("Nội dung trong cột đầu tiên.")
        st.button("Nút ở cột 1")

    with col2:
        st.subheader("Cột 2")
        st.write("Nội dung ở giữa.")
        st.checkbox("Tùy chọn ở cột 2")

    with col3:
        st.subheader("Cột 3")
        st.write("Nội dung ở cột cuối cùng.")
        st.slider("Thanh trượt ở cột 3", 0, 100, 50)

    # Bạn cũng có thể chỉ định tỷ lệ của các cột
    col_a, col_b = st.columns([2, 1]) # Cột A rộng gấp đôi cột B

    with col_a:
        st.write("Cột A (rộng hơn)")
        st.line_chart(np.random.randn(10, 2))

    with col_b:
        st.write("Cột B (hẹp hơn)")
        st.dataframe(pd.DataFrame({'data': [1, 2, 3]}))

    st.header("Sử dụng `st.tabs`")

    tab1, tab2, tab3 = st.tabs(["Dữ liệu", "Biểu đồ", "Cài đặt"])

    with tab1:
        st.subheader("Tab Dữ liệu")
        st.write("Hiển thị bảng dữ liệu mẫu.")
        st.dataframe(pd.DataFrame({'A': [10, 20, 30], 'B': [1, 2, 3]}))

    with tab2:
        st.subheader("Tab Biểu đồ")
        st.write("Hiển thị biểu đồ đường ngẫu nhiên.")
        st.line_chart(np.random.randn(20, 3))

    with tab3:
        st.subheader("Tab Cài đặt")
        st.write("Các tùy chọn cấu hình cho ứng dụng.")
        st.selectbox("Chọn tùy chọn:", ["Option 1", "Option 2", "Option 3"])



    st.sidebar.title("Thanh Bên (Sidebar)")
    st.sidebar.write("Đây là nơi bạn có thể đặt các bộ lọc hoặc tùy chọn.")

    # Widget trong sidebar
    selected_option = st.sidebar.selectbox(
        "Chọn một danh mục:",
        ["Phân tích", "Báo cáo", "Giới thiệu"]
    )

    st.sidebar.slider("Phạm vi dữ liệu:", 0, 100, (25, 75))

    st.header(f"Nội dung chính cho: {selected_option}")

    if selected_option == "Phân tích":
        st.write("Hiển thị các công cụ phân tích dữ liệu.")
    elif selected_option == "Báo cáo":
        st.write("Hiển thị các báo cáo tổng hợp.")
    else:
        st.write("Thông tin giới thiệu về ứng dụng.")