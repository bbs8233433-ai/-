import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 頁面配置與防自動翻譯設定
st.set_page_config(page_title="成本估價系統", layout="wide")
st.markdown('<div translate="no">', unsafe_allow_html=True)

st.title("🧮 自動化成本估價系統")

DB_FILE = "database.csv"

# 初始化資料庫
if not os.path.exists(DB_FILE):
    initial_data = [
        ["BHA32C20", "士林回路保護器2P20A 380V/6KA", "2P-20A", "只", 226, "三雨水電材料有限公司"],
        ["BHA32C05", "士林回路保護器2P5A 380V/6KA", "2P-5A", "只", 249, "三雨水電材料有限公司"],
        ["BHA32C63", "士林回路保護器2P63A 380V/6KA", "2P-63A", "只", 314, "三雨水電材料有限公司"],
        ["BHA33C10", "士林回路保護器3P10A 380V/6KA", "3P-10A", "只", 345, "三雨水電材料有限公司"],
        ["BHA33C16", "士林回路保護器3P16A 380V/6KA", "3P-16A", "只", 345, "三雨水電材料有限公司"],
        ["BHA33C50", "士林回路保護器3P50A 380V/6KA", "3P-50A", "只", 488, "三雨水電材料有限公司"],
        ["B1Z-10MR", "永宏PLC-10點(價格暫定)", "PLC", "只", 2000, "巨曜"],
        ["FBS-24MAR2-AC", "永宏PLC-24點", "PLC", "只", 3410, "巨曜"],
        ["H3M-B 220V 3S-30M", "士研多段式限時繼電器 220V", "士研電機/限時繼電器", "只", 250, "三雨水電材料有限公司"],
        ["JJB1-303015-1.0ST", "白鐵明箱300*300*150 厚1.0 ST底", "白鐵箱", "只", 1300, "三雨水電材料有限公司"],
        ["JJB1-363615-1.0ST訂", "白鐵明箱360*360*150 厚1.0 ST底", "白鐵箱", "只", 2200, "三雨水電材料有限公司"],
        ["CU-10/4P 220V4大A", "東元電熱專用接觸器220V4大A 25A", "東元電機/電磁接觸器", "只", 210, "三雨水電材料有限公司"],
        ["TN2BHR-1B", "天德連續按鈕-紅-1B", "急停扭", "只", 100, "三雨水電材料有限公司"],
        ["YW1B-V4E01R", "和泉連鎖押扣-1B-紅", "急停扭", "只", 120, "三雨水電材料有限公司"],
        ["TN2-EBS", "連瑣式窄版護座-黃色", "急停防護蓋", "只", 70, "三雨水電材料有限公司"],
        ["LSED-M3YN", "和泉LED 燈泡 AC/DC230/240 黃", "指示燈", "只", 42, "三雨水電材料有限公司"],
        ["YW1P-2EQ0Y", "和泉22半球形指示燈座無燈泡 黃", "指示燈座", "只", 36, "三雨水電材料有限公司"],
        ["YW1B-M1E01R", "和泉平頭押扣-1B-紅", "按鈕(紅)", "只", 55, "三雨水電材料有限公司"],
        ["YW1B-M1E10G", "和泉平頭押扣-1A-綠", "按鈕(綠)", "只", 55, "三雨水電材料有限公司"],
        ["TN2-B1", "單孔開關盒", "按鈕盒", "只", 78, "三雨水電材料有限公司"],
        ["JJA1-242415-1.2T", "鐵明箱240*240*150 厚1.2mm 鐵底", "烤漆箱", "只", 650, "三雨水電材料有限公司"],
        ["JJA1-363615-1.2T", "鐵明箱360*360*150 厚1.2mm 鐵底", "烤漆箱", "只", 700, "三雨水電材料有限公司"],
        ["JJA1-454517-1.2T", "鐵明箱450*450*180 厚1.2mm 鐵底", "烤漆箱", "只", 1000, "三雨水電材料有限公司"],
        ["JJA1-604517-1.2T", "鐵明箱600*450*170 厚1.2mm 鐵底", "烤漆箱", "只", 1600, "三雨水電材料有限公司"],
        ["JJA1-705016-1.2T", "鐵明箱700*500*160 厚1.2mm 鐵底", "烤漆箱", "只", 3100, "三雨水電材料有限公司"],
        ["QCE-3P50A", "東元無熔絲3P50A", "無熔絲開關", "只", 334, "三雨水電材料有限公司"],
        ["MW-HDR-30-24 1.5A", "明緯軌道式電源供應器 30w 24V", "電源供應器 30w", "只", 350, "三雨水電材料有限公司"],
        ["LED-S9-220-Y", "卡式燈泡LED AC/220V", "燈泡 220V", "只", 35, "三雨水電材料有限公司"],
        ["TN2SS4B-1AA", "天德選擇三段 1A-0-1A黑", "選擇開關", "只", 96, "三雨水電材料有限公司"],
        ["YW1S-2E10", "和泉選擇開關二段 1A", "選擇開關", "只", 57, "三雨水電材料有限公司"],
        ["RJ2S-CL A220", "和泉薄型繼電器 2P AC220V", "繼電器 220V", "只", 90, "三雨水電材料有限公司"],
        ["RJ2S-CL D24", "和泉薄型繼電器 2P DC24V", "繼電器 24V", "只", 90, "三雨水電材料有限公司"],
        ["SJ2S-05BS", "和泉薄型繼電器座 2P", "繼電器座", "只", 50, "三雨水電材料有限公司"],
        ["EP", "變壓器1Φ5A 380V 轉 220V", "變壓器", "台", 1995, "利能電機"]
    ]
    df_init = pd.DataFrame(initial_data, columns=["物品編號", "品名", "類別", "單位", "單價", "主要供應商"])
    df_init.to_csv(DB_FILE, index=False, encoding="utf-8-sig")

df_database = pd.read_csv(DB_FILE)

# 側邊欄：主資料庫管理
st.sidebar.header("⚙️ 主資料庫維護")
db_option = st.sidebar.radio("選擇操作", ["查看/編輯資料庫", "新增品項"])

if db_option == "查看/編輯資料庫":
    st.sidebar.subheader("當前品項資料庫")
    edited_db = st.sidebar.data_editor(df_database, num_rows="dynamic", key="db_editor")
    if not edited_db.equals(df_database):
        edited_db.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
        st.sidebar.success("資料庫修改已同步儲存！")
        st.rerun()

elif db_option == "新增品項":
    st.sidebar.subheader("新增品項至資料庫")
    with st.sidebar.form("add_item_form"):
        code = st.text_input("物品編號")
        name = st.text_input("品名")
        category = st.text_input("品牌/類別")
        unit = st.text_input("單位", value="只")
        price = st.number_input("標準單價 (NT$)", min_value=0, value=None, placeholder="請輸入單價")
        supplier = st.text_input("主要供應商")
        submit = st.form_submit_button("新增品項")
        
        if submit and name:
            actual_price = price if price is not None else 0
            new_row = pd.DataFrame([{
                "物品編號": code, "品名": name, "類別": category,
                "單位": unit, "單價": actual_price, "主要供應商": supplier
            }])
            updated_db = pd.concat([df_database, new_row], ignore_index=True)
            updated_db.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
            st.sidebar.success(f"已成功新增並永久儲存：{name}")
            st.rerun()

# 主要功能區域：成本估價表單
st.header("📋 報價估價單製作")

company_name = st.text_input("公司名稱：", value="")

if 'cart' not in st.session_state:
    st.session_state.cart = []

st.subheader("1. 勾選新增報價項目")

item_options = list(df_database["品名"].unique())

# 直接建立多選下拉選單（透過 key 控制狀態）
selected_items = st.multiselect("請勾選或搜尋要新增的品名（可多選）：", options=item_options, key="item_selector")

if st.button("➕ 將勾選項目加入報價單"):
    if selected_items:
        added_count = 0
        for item in selected_items:
            db_match = df_database[df_database["品名"] == item].iloc[0]
            existing_names = [cart_item["品名"] for cart_item in st.session_state.cart]
            if item not in existing_names:
                st.session_state.cart.append({
                    "品名": item,
                    "物品編號": db_match["物品編號"],
                    "品牌/類別": db_match["類別"],
                    "單位": db_match["單位"],
                    "數量": 1,
                    "標準單價 (NT$)": int(db_match["單價"]),
                    "小計金額 (NT$)": int(db_match["單價"]),
                    "備註說明": ""
                })
                added_count += 1
        
        # 加入後自動依「物品編號」排序
        if len(st.session_state.cart) > 0:
            cart_tmp = pd.DataFrame(st.session_state.cart)
            cart_tmp = cart_tmp.sort_values(by="物品編號", ascending=True)
            st.session_state.cart = cart_tmp.to_dict('records')
        
        st.success(f"成功加入 {added_count} 個新品項並完成排序！")
        
        # 關鍵：直接從 session_state 中刪除該選單的暫存記憶，強制下次渲染時為空
        if "item_selector" in st.session_state:
            del st.session_state["item_selector"]
            
        st.rerun()
    else:
        st.warning("請先勾選至少一個品名！")

st.subheader("2. 估價單明細")
if len(st.session_state.cart) > 0:
    cart_df = pd.DataFrame(st.session_state.cart)
    cart_df = cart_df.sort_values(by="物品編號", ascending=True)
    
    edited_cart = st.data_editor(
        cart_df,
        column_config={
            "數量": st.column_config.NumberColumn("數量", min_value=1, step=1, required=True),
            "小計金額 (NT$)": st.column_config.NumberColumn("小計金額 (NT$)", disabled=True),
        },
        disabled=["品名", "物品編號", "品牌/類別", "單位", "標準單價 (NT$)"],
        num_rows="dynamic",
        key="cart_editor"
    )
    
    edited_cart["數量"] = pd.to_numeric(edited_cart["數量"], errors='coerce').fillna(1).astype(int)
    edited_cart["標準單價 (NT$)"] = pd.to_numeric(edited_cart["標準單價 (NT$)"], errors='coerce').fillna(0).astype(int)
    edited_cart["小計金額 (NT$)"] = edited_cart["數量"] * edited_cart["標準單價 (NT$)"]
    
    edited_cart = edited_cart.sort_values(by="物品編號", ascending=True)
    
    updated_cart_list = edited_cart.to_dict('records')
    if updated_cart_list != st.session_state.cart:
        st.session_state.cart = updated_cart_list
        st.rerun()
    
    total_amount = edited_cart["小計金額 (NT$)"].sum()
    item_count = len(edited_cart)

    col_a, col_b = st.columns(2)
    col_a.metric("填報品項筆數", f"{item_count} 筆")
    col_b.metric("報價總金額 (NT$)", f"${total_amount:,.0f}")

    col_dl1, col_dl2 = st.columns(2)
    if col_dl1.button("🗑️ 清空報價單"):
        st.session_state.cart = []
        st.rerun()
        
    today_str = datetime.now().strftime("%Y%m%d")
    name_suffix = company_name if company_name else "估價單"
    export_filename = f"{today_str}-{name_suffix}_成本.csv"

    export_df = edited_cart.copy()
    total_row = pd.DataFrame([{
        "品名": "總計",
        "物品編號": "",
        "品牌/類別": "",
        "單位": "",
        "數量": "",
        "標準單價 (NT$)": "",
        "小計金額 (NT$)": total_amount,
        "備註說明": ""
    }])
    export_df = pd.concat([export_df, total_row], ignore_index=True)

    csv_data = export_df.to_csv(index=False).encode('utf-8-sig')
    col_dl2.download_button(
        label="📥 下載報價單 (CSV)",
        data=csv_data,
        file_name=export_filename,
        mime="text/csv"
    )
else:
    st.info("目前報價單為空，請從上方勾選品名並點擊加入。")
