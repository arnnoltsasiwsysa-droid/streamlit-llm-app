from dotenv import load_dotenv
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .env を読み込む（OPENAI_API_KEY が必要）
load_dotenv()

st.set_page_config(page_title="LLMアプリ（簡単な専門家モード）")
# -----------------------------
# 概要と操作方法
# -----------------------------
st.title("LLMアプリ（簡単な専門家モード）")
st.write("""
このアプリでは、入力した質問に対して **LLM** が専門家になりきって答えます。  
下のラジオボタンで「料理の専門家」か「旅行ガイド」を選び、質問を入力してみましょう。

**使い方**
1. 専門家の種類を選びます。  
   - 料理の専門家  
   - 旅行ガイド  
2. 質問を入力します。  
   （例：「夕食に簡単なレシピを教えて」「京都でおすすめの観光地は？」）  
3. 「実行」ボタンを押すと、回答が表示されます。
""")

st.divider()

# 専門家選択（A/B）
role_choice = st.radio(
    "専門家の種類を選択してください。",
    options=["専門家A（料理の専門家）", "専門家B（旅行ガイド）"],
    horizontal=True
)

# 入力フォーム
user_input = st.text_input(
    label="質問を入力してください。",
    placeholder="例：夕食に簡単なレシピを教えて"
)

st.divider()

# LLM呼び出し関数
def get_llm_response(input_text: str, selected_role: str) -> str:
    # ★ langchain_openai.ChatOpenAI は model= を使います（model_name ではありません）
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    EXPERT_A_PROMPT = "あなたは『料理の専門家』です。わかりやすく、短くレシピや料理のアドバイスをしてください。"
    EXPERT_B_PROMPT = "あなたは『旅行ガイド』です。観光地や旅のヒントを、簡潔に楽しく教えてください。"

    system_prompt = EXPERT_A_PROMPT if "料理" in selected_role else EXPERT_B_PROMPT

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text),
    ]

    # ★ 呼び出しは llm.invoke(messages)
    result = llm.invoke(messages)
    return result.content

# 実行ボタン
if st.button("実行"):
    if not user_input.strip():
        st.error("質問を入力してから「実行」ボタンを押してください。")
    else:
        with st.spinner("LLMに問い合わせ中..."):
            try:
                answer = get_llm_response(user_input, role_choice)
                st.success("回答を取得しました。")
                st.write("##### 回答")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")