import streamlit as st
from src.bootstrap import uicapabilities


async def analysis_script():
    content = st.session_state['script_content']
    pass


async def send_prompts(prompts):
    pass


async def characters_analyze():
    # Thực thi xong thì gán giá trị luôn vào section state
    prompt = st.session_state['characters_extract_prompt']
    model = st.session_state['characters_model']
    content = st.session_state.get('script_content', None)

    chars = uicapabilities.extract_chars(
        prompt=prompt,
        content=content,
        model=model,
    )
    st.session_state['chars'] = chars
    return chars


async def shots_analyze(model, prompt, content):
    pass
