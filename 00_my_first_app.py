import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,  # システムメッセージ(ChatGPTの設定を決める指示)
    HumanMessage,  # 人間の質問
    AIMessage  # ChatGPTの返答
)

def main():
    # temperatureパラメータは、モデルが生成するテキストの"ランダム性"や"多様性"を制御
    llm = ChatOpenAI(temperature=0)  # ChatGPT APIを呼んでくれる機能

    st.set_page_config(
        page_title= "My Great ChatGPT",
        page_icon="🤗",
    )
    st.header("My Great ChatGPT 🤗")

    # チャット履歴の初期化
    # session_stateは、アプリケーションの状態を管理するための機能
    # LangChainにも会話の内容を記憶してくれるMemoryという機能がある
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    # ユーザーの入力を監視
    if user_input := st.chat_input("聞きたいことを入力してね！"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm(st.session_state.messages)
        # ChatGPT APIはステートレスなAPIのため、毎回、チャットの履歴を送信しないと適切な返答を得られない
        st.session_state.messages.append(AIMessage(content=response.content))

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else: # isinstance(message, SystemMessage)
            st.write(f"System message: {message.content}")

if __name__ == '__main__':
    main()
