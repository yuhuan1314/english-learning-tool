import streamlit as st
import PyPDF2
from minimax_client import MiniMax
from io import BytesIO

# 页面配置
st.set_page_config(page_title="英语试卷二次开发", page_icon="📝", layout="wide")
st.title("📝 英语试卷二次开发")
st.caption("手机也能用 | 上传试卷PDF，自动生成三纽扣拆解+专项练习")

# 配置Minimax（替换成你自己的密钥）
YOUR_MINIMAX_API_KEY = "sk-cp-3yV1Tg4PVX98E-lu p5R4UShPvzzO0uZNBcXGj SYIJIIFD3fg40LneOSB9KGo TX4EkwYKyPZ9AapQwF991 5SVu65A9OMX5c7ViYo8iy7 pSHAiihLQ8xW73sw"
YOUR_MINIMAX_GROUP_ID = "2024308105302516508"
MINIMAX_MODEL_ID = "abab6.5-chat" # 官方标准模型名，不要乱改

# 初始化客户端
@st.cache_resource
def init_minimax():
    return MiniMax(api_key=MINIMAX_API_KEY)

minimax_client = init_minimax()

# 上传PDF
uploaded_file = st.file_uploader("上传英语试卷PDF", type="pdf")

# 核心处理逻辑
if uploaded_file is not None:
    with st.spinner("正在解析PDF..."):
        # 提取PDF文本
        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        paper_text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                paper_text += page_text
        st.success("PDF解析完成！正在生成练习...")

    # 生成练习
    with st.spinner("AI正在生成二次开发练习，请稍候..."):
        prompt = f"""
        你是高考英语试卷二次开发专家，严格遵循李力老师的【三纽扣还原法】，对上传的高考英语试卷进行二次开发。
        三纽扣还原法核心定义：
        1. ⚡引擎纽扣：句子核心谓语动词，排除非谓语干扰
        2. 🔗关节纽扣：句子连接词/引导词，拆解从句逻辑
        3. ⚓锚点纽扣：核心介词词块、固定搭配，高考高频考点

        请基于下面的试卷内容，生成对应的练习，结构清晰，分模块展示：
        1. 【核心长难句三纽扣拆解】：提取5句40词以上的长难句，每句都按三纽扣法拆解，标注考点
        2. 【高频词汇练习】：提取20个试卷高频核心词汇/短语，给出中文释义、考点、例句
        3. 【词性变形练习】：提取10个核心考点词汇，生成词性变形题，附答案
        4. 【短语翻译练习】：提取10个试卷高频短语，生成中英互译题，附答案
        5. 【语境填词练习】：基于试卷核心词汇，生成5道语境填空题，附答案
        6. 【微写作题目】：基于试卷话题，生成1道50词左右的高考适配微写作题，给情境和开头示例

        试卷原文内容：
        {paper_text}
        """
        response = minimax_client.chat.completions.create(
            model=MINIMAX_MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4096
        )
        result = response.choices[0].message.content

    # 展示结果
    st.markdown(result)

    # 下载功能
    st.download_button(
        label="📥 下载练习内容",
        data=result,
        file_name=f"{uploaded_file.name.split('.')[0]}_二次开发练习.txt",
        mime="text/plain"
    )
