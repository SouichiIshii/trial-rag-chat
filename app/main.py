import streamlit as st
import requests

def main():
    # ページ設定
    st.set_page_config(page_title="AI Chat", layout="wide")

    # ページ選択
    page = st.sidebar.selectbox("ページを選択", ["AIとチャットする", "資料登録", "資料確認"], index=0)

    # ページへの遷移
    if page == "AIとチャットする":
        ai_chat_page()
    elif page == "資料登録":
        document_registration_page()
    elif page == "資料確認":
        document_review_page()

def ai_chat_page():
    st.title("AIとチャットする")

    # ユーザ入力用のテキストボックス
    user_question = st.text_input("質問を入力してください。")

    if st.button("送信"):
        # ここでチャットロジックを実装
        st.write(f"ユーザー: {user_question}")

        # 仮の回答
        st.write(f"AI: 何かお手伝いできることはありますか？")

def document_registration_page():
    st.title("資料登録")

    target_file = st.file_uploader("PDFファイルを選択してください。", type=["pdf"])
    if target_file is not None:
        files = {
            "file": (target_file.name, target_file, "application/pdf")
        }
        if st.button("選択したファイルを登録する"):
            response = requests.post(
                url="http://localhost:8000/upload/",
                files=files
            )
            if response.status_code == 200:
                st.success(f"{target_file.name}の登録完了")
            else:
                st.error("登録失敗")

def document_review_page():
    st.title("資料確認")


if __name__ == "__main__":
    main()