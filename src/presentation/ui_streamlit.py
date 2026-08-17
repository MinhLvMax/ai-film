import pandas as pd
from io import BytesIO
from datetime import datetime
import streamlit as st
from src.bootstrap import build_gen_prompts, build_send_prompts
import traceback


def run():
    if "prompts" not in st.session_state:
        st.session_state["prompts"] = []
    content = st.text_area("Nhập 1 đoạn content", height=150)

    if st.button("Tạo prompt"):
        try:
            with st.spinner("Đang tạo prompt..."):
                prompts = build_gen_prompts().gen_prompt_from_a_segment(content)

                st.session_state["prompts"] = prompts
        except Exception as e:
            st.error(e)
            st.code(traceback.format_exc())

    if st.session_state["prompts"]:
        for prompt in st.session_state["prompts"]:
            st.write(prompt)

        # tạo excel
        df = pd.DataFrame(st.session_state["prompts"])
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Prompts")

        file_name = datetime.now().strftime("prompts_%Y%m%d_%H%M%S.xlsx")

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "Lưu prompts ra Excel",
                data=output.getvalue(),
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with col2:
            if st.button("Gen toàn bộ"):
                try:
                    build_send_prompts(st.session_state["prompts"])
                    st.success("Đã gửi prompts")
                except Exception as e:
                    st.error(e)
                    st.code(traceback.format_exc())
