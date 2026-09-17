Python
import streamlit as st
import pandas as pd

# 1. 透過 html 加入 translate="no"，阻止瀏覽器自動翻譯破壞 DOM 結構
st.set_page_config(page_title="成本估價系統", layout="wide")
st.markdown('<div translate="no">', unsafe_allow_html=True)

st.title("🧮 自動化成本估價系統")

# 初始化或載入預設資料庫
if 'database' not in st.session_state:
    initial_db = [
        {"物品編號": "JJB1-303015-1.0ST", "品名": "白鐵明箱300*300*150 厚1.0 ST底", "類別": "白鐵箱", "單位": "只", "單價": 1300, "主要供應商": "三雨水電"},
        {"物品編號": "BHA32C05", "品名": "士林回路保護器2P5A 380V/6KA", "類別": "2P-5A", "單位": "只", "單價": 249, "主要供應商": "三雨水電"},
        {"物品編號": "JJA1-242415-1.2T", "品名": "鐵明箱240*240*150 厚1.2mm 鐵底", "類別": "烤漆箱", "單位": "只", "單價": 650, "主要供應商": "三雨水電"},
        {"物品編號": "BHA33C50", "品名": "士林回路保護器3P50A 380V/6KA", "類別": "3P-50A", "單位": "只", "單價": 488, "主要供應商": "三雨水電"},
        {"物品編號": "B1Z-10MR", "品名": "永宏PLC-10點(價格暫定)", "類別": "PLC", "單位": "只", "單價": 2000, "主要供應商": "巨曜"}
    ]
    st.session_state.database = pd.DataFrame(initial_db)

# 側邊欄：主資料庫管理
st.sidebar.header("⚙️ 主資料庫維護")
db_option = st.sidebar.radio("選擇操作", ["查看/編輯資料庫", "新增品項"])

if db_option == "查看/編輯資料庫":
    st.sidebar.subheader("當前品項資料庫")
    edited_db = st.sidebar.data_editor(st.session_state.database, num_rows="dynamic")
    st.session_state.database = edited_db
elif db_option == "新增品項":
    st.sidebar.subheader("新增品項至資料庫")
    with st.sidebar.form("add_item_form"):
        code = st.text_input("物品編號")
        name = st.text_input("品名")
        category = st.text_input("品牌/類別")
        unit = st.text_input("單位", value="只")
        price = st.number_input("標準單價 (NT$)", min_value=0, value=0)
        supplier = st.text_input("主要供應商")
        submit = st.form_submit_button("新增品項")
        
        if submit and name:
            new_row = pd.DataFrame([{
                "物品編號": code, "品名": name, "類別": category,
                "單位": unit, "單價": price, "主要供應商": supplier
            }])
            st.session_state.database = pd.concat([st.session_state.database, new_row], ignore_index=True)
            st.sidebar.success(f"已新增品項：{name}")

# 主要功能區域：成本估價表單
st.header("📋 報價估價單製作")

company_name = st.text_input("公司名稱：", value="客戶公司")

# 初始化報價單項目
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 新增報價明細區
st.subheader("1. 新增報價項目")
col1, col2 = st.columns([3, 1])

item_list = ["(請選擇品名)"] + list(st.session_state.database["品名"].unique())
selected_item = col1.selectbox("選擇品名", options=item_list)
qty = col2.number_input("數量", min_value=1, value=1)

if st.button("➕ 加入報價單"):
    if selected_item != "(請選擇品名)":
        db_match = st.session_state.database[st.session_state.database["品名"] == selected_item].iloc[0]
        st.session_state.cart.append({
            "品名": selected_item,
            "物品編號": db_match["物品編號"],
            "品牌/類別": db_match["類別"],
            "單位": db_match["單位"],
            "數量": qty,
            "標準單價 (NT$)": db_match["單價"],
            "小計金額 (NT$)": qty * db_match["單價"],
            "備註說明": ""
        })
        st.success(f"已加入：{selected_item}")
    else:
        st.warning("請先選擇品名！")

# 顯示估價單結果
st.subheader("2. 估價單明細")
if len(st.session_state.cart) > 0:
    cart_df = pd.DataFrame(st.session_state.cart)
    
    edited_cart = st.data_editor(
        cart_df,
        column_config={
            "數量": st.column_config.NumberColumn(min_value=1),
            "小計金額 (NT$)": st.column_config.NumberColumn(disabled=True),
        },
        disabled=["品名", "物品編號", "品牌/類別", "單位", "標準單價 (NT$)"],
        num_rows="dynamic"
    )
    
    edited_cart["小計金額 (NT$)"] = edited_cart["數量"] * edited_cart["標準單價 (NT$)"]
    total_amount = edited_cart["小計金額 (NT$)"].sum()
    item_count = len(edited_cart)

    col_a, col_b = st.columns(2)
    col_a.metric("填報品項筆數", f"{item_count} 筆")
    col_b.metric("報價總金額 (NT$)", f"${total_amount:,.0f}")

    col_dl1, col_dl2 = st.columns(2)
    if col_dl1.button("🗑️ 清空報價單"):
        st.session_state.cart = []
        st.rerun()
        
    csv_data = edited_cart.to_csv(index=False).encode('utf-8-sig')
    col_dl2.download_button(
        label="📥 下載報價單 (CSV)",
        data=csv_data,
        file_name=f"{company_name}_成本報價單.csv",
        mime="text/csv"
    )
else:
    st.info("目前報價單為空，請從上方選擇品名並加入。")
