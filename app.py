import streamlit as st
import pandas as pd
from datetime import datetime

# 頁面配置與防自動翻譯設定
st.set_page_config(page_title="成本估價系統", layout="wide")
st.markdown('<div translate="no">', unsafe_allow_html=True)

st.title("🧮 自動化成本估價系統")

# 初始化完整材料資料庫
if 'database' not in st.session_state:
    initial_db = [
        {"物品編號": "BHA32C20", "品名": "士林回路保護器2P20A 380V/6KA", "類別": "2P-20A", "單位": "只", "單價": 226, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "BHA32C05", "品名": "士林回路保護器2P5A 380V/6KA", "類別": "2P-5A", "單位": "只", "單價": 249, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "BHA32C63", "品名": "士林回路保護器2P63A 380V/6KA", "類別": "2P-63A", "單位": "只", "單價": 314, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "BHA33C10", "品名": "士林回路保護器3P10A 380V/6KA", "類別": "3P-10A", "單位": "只", "單價": 345, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "BHA33C16", "品名": "士林回路保護器3P16A 380V/6KA", "類別": "3P-16A", "單位": "只", "單價": 345, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "BHA33C50", "品名": "士林回路保護器3P50A 380V/6KA", "類別": "3P-50A", "單位": "只", "單價": 488, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "B1Z-10MR", "品名": "永宏PLC-10點(價格暫定)", "類別": "PLC", "單位": "只", "單價": 2000, "主要供應商": "巨曜"},
        {"物品編號": "FBS-24MAR2-AC", "品名": "永宏PLC-24點", "類別": "PLC", "單位": "只", "單價": 3410, "主要供應商": "巨曜"},
        {"物品編號": "H3M-B 220V 3S-30M", "品名": "士研多段式限時繼電器 220V", "類別": "士研電機/限時繼電器", "單位": "只", "單價": 250, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "JJB1-303015-1.0ST", "品名": "白鐵明箱300*300*150 厚1.0 ST底", "類別": "白鐵箱", "單位": "只", "單價": 1300, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "JJB1-363615-1.0ST訂", "品名": "白鐵明箱360*360*150 厚1.0 ST底", "類別": "白鐵箱", "單位": "只", "單價": 2200, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "CU-10/4P 220V4大A", "品名": "東元電熱專用接觸器220V4大A 25A", "類別": "東元電機/電磁接觸器", "單位": "只", "單價": 210, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "TN2BHR-1B", "品名": "天德連續按鈕-紅-1B", "類別": "急停扭", "單位": "只", "單價": 100, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "YW1B-V4E01R", "品名": "和泉連鎖押扣-1B-紅", "類別": "急停扭", "單位": "只", "單價": 120, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "TN2-EBS", "品名": "連瑣式窄版護座-黃色", "類別": "急停防護蓋", "單位": "只", "單價": 70, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "LSED-M3YN", "品名": "和泉LED 燈泡 AC/DC230/240 黃", "類別": "指示燈", "單位": "只", "單價": 42, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "YW1P-2EQ0Y", "品名": "和泉22半球形指示燈座無燈泡 黃", "類別": "指示燈座", "單位": "只", "單價": 36, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "YW1B-M1E01R", "品名": "和泉平頭押扣-1B-紅", "類別": "按鈕(紅)", "單位": "只", "單價": 55, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "YW1B-M1E10G", "品名": "和泉平頭押扣-1A-綠", "類別": "按鈕(綠)", "單位": "只", "單價": 55, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "TN2-B1", "品名": "單孔開關盒", "類別": "按鈕盒", "單位": "只", "單價": 78, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "JJA1-242415-1.2T", "品名": "鐵明箱240*240*150 厚1.2mm 鐵底", "類別": "烤漆箱", "單位": "只", "單價": 650, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "JJA1-363615-1.2T", "品名": "鐵明箱360*360*150 厚1.2mm 鐵底", "類別": "烤漆箱", "單位": "只", "單價": 700, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "JJA1-454517-1.2T", "品名": "鐵明箱450*450*180 厚1.2mm 鐵底", "類別": "烤漆箱", "單位": "只", "單價": 1000, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "JJA1-604517-1.2T", "品名": "鐵明箱600*450*170 厚1.2mm 鐵底", "類別": "烤漆箱", "單位": "只", "單價": 1600, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "JJA1-705016-1.2T", "品名": "鐵明箱700*500*160 厚1.2mm 鐵底", "類別": "烤漆箱", "單位": "只", "單價": 3100, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "QCE-3P50A", "品名": "東元無熔絲3P50A", "類別": "無熔絲開關", "單位": "只", "單價": 334, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "MW-HDR-30-24 1.5A", "品名": "明緯軌道式電源供應器 30w 24V", "類別": "電源供應器 30w", "單位": "只", "單價": 350, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "LED-S9-220-Y", "品名": "卡式燈泡LED AC/220V", "類別": "燈泡 220V", "單位": "只", "單價": 35, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "TN2SS4B-1AA", "品名": "天德選擇三段 1A-0-1A黑", "類別": "選擇開關", "單位": "只", "單價": 96, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "YW1S-2E10", "品名": "和泉選擇開關二段 1A", "類別": "選擇開關", "單位": "只", "單價": 57, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "RJ2S-CL A220", "品名": "和泉薄型繼電器 2P AC220V", "類別": "繼電器 220V", "單位": "只", "單價": 90, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "RJ2S-CL D24", "品名": "和泉薄型繼電器 2P DC24V", "類別": "繼電器 24V", "單位": "只", "單價": 90, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "SJ2S-05BS", "品名": "和泉薄型繼電器座 2P", "類別": "繼電器座", "單位": "只", "單價": 50, "主要供應商": "三雨水電材料有限公司"},
        {"物品編號": "EP", "品名": "變壓器1Φ5A 380V 轉 220V", "類別": "變壓器", "單位": "台", "單價": 1995, "主要供應商": "利能電機"}
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

# 公司名稱預設留白
company_name = st.text_input("公司名稱：", value="")

# 初始化報價單項目
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 新增報價明細區（多選勾選框）
st.subheader("1. 勾選新增報價項目")

item_options = list(st.session_state.database["品名"].unique())
selected_items = st.multiselect("請勾選或搜尋要新增的品名（可多選）：", options=item_options)

if st.button("➕ 將勾選項目加入報價單"):
    if selected_items:
        added_names = []
        for item in selected_items:
            db_match = st.session_state.database[st.session_state.database["品名"] == item].iloc[0]
            st.session_state.cart.append({
                "品名": item,
                "物品編號": db_match["物品編號"],
                "品牌/類別": db_match["類別"],
                "單位": db_match["單位"],
                "數量": 1,  # 預設數量為 1
                "標準單價 (NT$)": db_match["單價"],
                "小計金額 (NT$)": db_match["單價"],
                "備註說明": ""
            })
            added_names.append(item)
        st.success(f"已成功加入 {len(added_names)} 個品項！請至下方明細調整數量。")
    else:
        st.warning("請先勾選至少一個品名！")

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
        
    # 自動取得今天日期 YYYYMMDD 格式
    today_str = datetime.now().strftime("%Y%m%d")
    name_suffix = company_name if company_name else "估價單"
    export_filename = f"{today_str}-{name_suffix}_成本報價單.csv"

    csv_data = edited_cart.to_csv(index=False).encode('utf-8-sig')
    col_dl2.download_button(
        label="📥 下載報價單 (CSV)",
        data=csv_data,
        file_name=export_filename,
        mime="text/csv"
    )
else:
    st.info("目前報價單為空，請從上方勾選品名並點擊加入。")
