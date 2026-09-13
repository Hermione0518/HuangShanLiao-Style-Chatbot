import uuid
import streamlit as st

from config import TOP_K, MAX_HISTORY, LLM_PROVIDER
from database import init_db, save_message, get_history, save_feedback
from persona import load_persona
from rag import retrieve, format_context, build_index
from safety import is_high_risk, safety_response
from llm import generate

st.set_page_config(
    page_title="黃山料風格對話機器人",
    page_icon="📖",
    layout="centered"
)

init_db()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = get_history(
        st.session_state.session_id,
        MAX_HISTORY
    )

if "last_pair" not in st.session_state:
    st.session_state.last_pair = None

st.title("📖 黃山料風格對話機器人")
st.caption("受公開作品與資料啟發的風格化對話系統，不代表作者本人。")

with st.sidebar:
    st.header("設定")
    st.write(f"LLM：`{LLM_PROVIDER}`")

    top_k = st.slider("檢索資料數", 1, 10, TOP_K)

    if st.button("重新建立知識庫索引"):
        with st.spinner("建立 TF-IDF index..."):
            build_index()
        st.success("索引完成。")

    if st.button("清除目前對話"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.last_pair = None
        st.rerun()

    st.divider()
    st.markdown(
        "### 專案原則\n"
        "- 不冒充真人\n"
        "- 不複製書籍全文\n"
        "- 優先使用知識庫\n"
        "- 找不到資料時不亂編"
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("想聊聊什麼？")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    save_message(st.session_state.session_id, "user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    if is_high_risk(prompt):
        answer = safety_response()
        sources = []
    else:
        results = retrieve(prompt, top_k)
        context = format_context(results)
        persona = load_persona()

        recent = get_history(
            st.session_state.session_id,
            MAX_HISTORY
        )

        system = f"""
{persona}

你正在進行一個「風格化」對話，不是本人身分模擬。

以下是檢索到的知識庫內容：
{context}

回答規則：
- 不要說「根據資料庫所以……」這種機械式句子，除非使用者問資料來源。
- 不要捏造書中沒有的情節。
- 不要逐字複製受版權保護的長段落。
- 如果資料庫不足，說明不足。
- 先理解使用者真正想問的是什麼。
- 如果只是需要陪伴，可以自然回答，不必強行引用作品。
"""

        messages = recent[-MAX_HISTORY:]
        try:
            answer = generate(system, messages)
        except Exception as e:
            answer = (
                f"目前模型連線失敗：`{e}`\n\n"
                "請檢查 `.env` 的 API 設定，或切換成 Ollama。"
            )

        sources = results

    with st.chat_message("assistant"):
        st.markdown(answer)

        if sources:
            with st.expander("📚 參考資料"):
                for r in sources:
                    st.markdown(
                        f"**{r['source']}**  · 相似度 `{r['score']}`"
                    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    save_message(st.session_state.session_id, "assistant", answer)

    st.session_state.last_pair = {
        "user": prompt,
        "assistant": answer
    }

if st.session_state.last_pair:
    st.divider()
    st.subheader("這次回答有幫助嗎？")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 有幫助"):
            p = st.session_state.last_pair
            save_feedback(
                st.session_state.session_id,
                p["user"], p["assistant"], 1, ""
            )
            st.success("已記錄。")

    with col2:
        if st.button("👎 不太像"):
            st.session_state.show_correction = True

    if st.session_state.get("show_correction"):
        correction = st.text_area(
            "哪裡需要改？",
            placeholder="例如：太正式、太雞湯、沒有直接回答問題……"
        )
        if st.button("送出修正"):
            p = st.session_state.last_pair
            save_feedback(
                st.session_state.session_id,
                p["user"], p["assistant"], 0, correction
            )
            st.session_state.show_correction = False
            st.success("已記錄修正。")
