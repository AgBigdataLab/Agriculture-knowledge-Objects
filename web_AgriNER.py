import streamlit as st
from openai import OpenAI
import json
st.set_page_config(page_title="农业领域知识对象识别",layout="wide")

def get_response(prompt):
    client = OpenAI(api_key="0", base_url="http://0.0.0.0:8011/v1")
    instruction = """Extract named entities from the given sentence based on the following entity types:["Grain and Oil Crops", "Fruits and Vegetables", "Edible Fungi", "Flowers", "Medicinal Plants", "Livestock and Poultry", "Aquatic Animals", "Tea", "Agricultural Enterprises", "Agronomic Techniques", "Developmental Stages", "Gas", "Fertilizer", "Soil Type", "Feed Additives", "Forage", "Livestock and Poultry Diseases", "Pests and Diseases", "Infected Crop Parts", "Pesticide", "Veterinary Drug", "Agricultural Control", "Physical Control", "Biological Control", "Chemical Control"]. \
Respond in the following JSON format.
Text:
"""
    messages = [
        {"role": "system", "content": "You are an excellent linguist in the domain of Agricultural domain."},
        {"role": "user", "content": instruction+prompt}
    ]
    
    result = client.chat.completions.create(
        messages=messages, 
        model="/home/zhaochenyun/zcy/0_Model/Llama3.1-8B-Instruct",
        temperature = 0.1,
        n=1,
        max_tokens=1024,
        response_format={"type": "json_object"},
    )
    
    return result.choices[0].message.content

# 设置按钮和输入框样式
st.markdown(
    """
    <style>
        .stTextArea textarea {
            font-size: 18px;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 10px;
        }
        /* Button Styling */
        .stButton button {
            font-size: 16px;
            padding: 10px 25px;
            background-color: #2a6b29;
            color: white;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.1s ease-in-out;
        }

        /* Button Hover */
        .stButton button:hover {
            background-color: #4CAF50;
        }

        /* Button Active (on click) */
        .stButton button:active {
            transform: scale(0.98);
            background-color: #3e8e41;
        }

        /* Button Focus Effect */
        .stButton button:focus {
            outline: none;
            box-shadow: 0 0 5px 3px rgba(72, 128, 30, 0.5);
        }
    </style>
    """, unsafe_allow_html=True
)
st.markdown("<h2 style='text-align: center'>农业领域知识对象识别</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
# Sidebar setup
with st.sidebar:
    # 添加小标题
    st.markdown("<h2 style='text-align: center;'>关于本工具</h2>", unsafe_allow_html=True)
    st.write("""
    本工具利用先进的自然语言处理技术，旨在帮助用户自动识别**农业领域知识对象**。通过输入农业领域的科技文献片段，系统能够快速识别并提取出与该文本相关的农业知识对象，包括但不限于作物类型、农业技术、病虫害防治、畜牧水产等信息。
    """)
    # Creating an expander for the knowledge object types list
    with st.expander("点击展开查看知识对象类型", expanded=False):
        st.markdown("""
        <ul style="list-style-type: none; padding-left: 0;">
            <li>Grain and Oil Crops</li>
            <li>Fruits and Vegetables</li>
            <li>Edible Fungi</li>
            <li>Flowers</li>
            <li>Medicinal Plants</li>
            <li>Tea</li>
            <li>Livestock and Poultry</li>
            <li>Aquatic Animals</li>
            <li>Agricultural Enterprises</li>
            <li>Feed Additives</li>
            <li>Forage</li>
            <li>Agronomic Techniques</li>
            <li>Developmental Stages</li>
            <li>Gas</li>
            <li>Fertilizer</li>
            <li>Soil Type</li>
            <li>Livestock and Poultry Diseases</li>
            <li>Pests and Diseases</li>
            <li>Infected Crop Parts</li>
            <li>Pesticide</li>
            <li>Veterinary Drug</li>
            <li>Agricultural Control</li>
            <li>Physical Control</li>
            <li>Biological Control</li>
            <li>Chemical Control</li>
        </ul>
        """, unsafe_allow_html=True)
        
    # 使用步骤
    st.markdown("""
    **📌 使用步骤**
    1. 在下方文本框输入农业科技文献片段。
    2. 点击“开始识别”按钮进行识别。
    3. 查看识别结果，获取相关农业知识对象信息。
    """)

input_text = st.text_area("请输入农业领域科技文献文本片段", value=st.session_state.get("input_text", ""), height=255)
# Display word & character count
word_count = len(input_text.split()) 
char_count = len(input_text)  
st.markdown(f"<div class='info-box'>📊 字数: <b>{word_count}</b> 个单词 | 字符数: <b>{char_count}</b> 个字符</div>", unsafe_allow_html=True)

# --- Button for Recognition ---
if st.button("🔍 开始识别"):
    if input_text.strip():
        with st.spinner("识别中，请稍候..."):
            response = get_response(input_text)

        st.subheader("识别结果")
        # st.markdown("<hr>", unsafe_allow_html=True)  # Divider

        # Formatting the output for readability
        try:
            response_json = json.loads(response)
            formatted_output = ""
            for key, values in response_json.items():
                formatted_output += f"<div style='font-size: 20px; font-weight: bold; color: #2c6e49;'>{key}:</div>"
                for value in values:
                    formatted_output += f"<div style='padding-left: 20px; font-size: 16px; color: #555;'>- {value}</div>"
                formatted_output += "<br>"

            st.markdown(formatted_output, unsafe_allow_html=True)
        except json.JSONDecodeError:
            st.error("解析返回的JSON失败，请检查数据格式！")
    else:
        st.warning("⚠ 请输入有效的文本！")