from io import BytesIO

    today_str = datetime.now().strftime("%Y%m%d")
    name_suffix = company_name if company_name else "估價單"
    export_filename = f"{today_str}-{name_suffix}_成本.xlsx"

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

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        export_df.to_excel(writer, index=False, sheet_name="成本估價明細")
    excel_data = excel_buffer.getvalue()

    col_dl2.download_button(
        label="📥 下載報價單 (Excel)",
        data=excel_data,
        file_name=export_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
