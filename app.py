import streamlit as st
import openai
import os

# 讀取環境變數中的 API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="設計對焦助手", layout="centered")
st.title("🎨 設計對焦助手")
st.markdown("用 AI 協助你快速聚焦設計起手與語氣風格")

# 使用者輸入區
with st.form("design_form"):
    topic = st.text_area("📝 請描述你的設計需求", placeholder="例如：我要設計一個信用卡推薦頁面")
    tone_options = ["專業", "親民", "活潑", "科技感", "文青", "極簡", "幽默"]
    tone = st.multiselect("🗣️ 選擇語氣風格（可複選）", tone_options, default=["專業", "親民"])
    submitted = st.form_submit_button("✨ 產生建議")

if submitted and topic:
    with st.spinner("AI 正在思考..."):
        prompt = f"""
你是一位資深金融業 UX 設計師，擅長設計頁面架構與撰寫文案。

請根據以下設計需求與指定語氣，產出以下內容：
1. 建議的頁面結構（3-5 個區塊，並簡述用途）
2. 每一區塊的標題與內文範例，語氣需符合指定風格
3. 每個段落請標註其語氣（例如：[專業]、[親民]）

【設計需求】：{topic}
【語氣風格】：{"、".join(tone)}

請用條列方式清楚呈現，語言使用繁體中文。
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1200
            )
            output = response["choices"][0]["message"]["content"]
            st.markdown("### 📋 AI 建議如下：")
            st.markdown(output)

        except Exception as e:
            st.error(f"⚠️ 發生錯誤：{str(e)}")
else:
    st.info("請先輸入設計需求並按下『產生建議』")
