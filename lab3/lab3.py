import streamlit as st
import pandas as pd
import os
import nbformat

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, '../lab2/lab2.ipynb')
with open(path) as w:
    nb = nbformat.read(w, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        exec(cell.source)

df = concatDf
provinces = ["Вінницька область", "Волинська область", "Дніпропетровська область", "Донецька область", "Житомирська область", "Закарпатська область", "Запорізька область", "Івано-Франківська область", "Київська область", "Кіровоградська область", "Луганська область", "Львівська область", "Миколаївська область", "Одеська область", "Полтавська область", "Рівенська область", "Сумська область", "Тернопільська область", "Харківська область", "Херсонська область", "Хмельницька область", "Черкаська область", "Чернівецька область", "Чернігівська область", "Республіка Крим", "м. Київ", "м. Севастополь"]
Df_values = df.columns.tolist()[4:7]

st.set_page_config(layout="wide")

if "selected_area" not in st.session_state:
    st.session_state.selected_area = Df_values[0]
if "selected_province" not in st.session_state:
    st.session_state.selected_province = provinces[0]
if "week_range" not in st.session_state:
    st.session_state.week_range = (1, 52)
if "year_range" not in st.session_state:
    st.session_state.year_range = (2020, 2024)
if "sort_order" not in st.session_state:
    st.session_state.sort_order = "жодного"

col1, col2 = st.columns([2, 1])
with col2: 
    st.title('Lab 3')

    if st.button("Скинути фільтри"):
        st.session_state.selected_area = Df_values[0]
        st.session_state.selected_province = provinces[0]
        st.session_state.week_range = (1, 52)
        st.session_state.year_range = (2020, 2024)
        st.session_state.sort_order = "жодного"

    selected_area = st.selectbox(
    "Оберіть область даних",
    options = Df_values,
    index = Df_values.index(st.session_state.selected_area),
    key = "selected_area"
    )

    selected_province = st.selectbox(
        "Оберіть регіон",
       options = provinces,
        index = provinces.index(st.session_state.selected_province),
       key = "selected_province"
    )
    selected_index = provinces.index(st.session_state.selected_province) + 1 

    week_range = st.slider(
        "Виберіть інтервал тижнів", 1, 52,
        key = "week_range"
    )

    year_range = st.slider(
        "Виберіть інтервал років", 1982, 2024,
        key = "year_range"
    )

filtered_df = df[(df["week"] >= week_range[0]) &
                (df["week"] <= week_range[1]) &
                (df["year"] >= year_range[0]) &
                (df["year"] <= year_range[1])]

filtered_province_df = filtered_df[filtered_df["provinceID"] == selected_index]

with col1:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння даних"])
    with tab1:
        st.title("Таблиця відфільтрованих даних")

        sort_order = st.radio(
        "Оберіть сортування",
        options=["жодного", "за зростанням", "за спаданням"],
        key="sort_order"
        )

        if sort_order == "за зростанням":
            filtered_province_df = filtered_province_df.sort_values(selected_area, ascending=True)
        elif sort_order == "за спаданням":
            filtered_province_df = filtered_province_df.sort_values(selected_area, ascending=False)
        else:
            filtered_province_df = filtered_province_df.sort_values(["provinceID", "year", "week"]) 
        
        st.write(filtered_province_df[['year', 'week', selected_area, 'provinceID']])

    with tab2:
        st.title("Графік відфільтрованих даних для " + selected_province)

        chart_data = filtered_province_df.pivot(index="week", columns="year", values=selected_area)
        st.line_chart(chart_data, x_label="Тиждень", y_label=selected_area)


    with tab3:
        st.title("Графік порівняння даних для " + selected_area)

        province_averages = []
        province_colors = []

        for i in range(1, 28):
            province_data = filtered_df[filtered_df["provinceID"] == i][selected_area]
            province_average = province_data.mean()
            if i == selected_index:
                province_color = "#FF0000"
            else:
                province_color = "#0000FF"
            province_averages.append(province_average)
            province_colors.append(province_color)
        compare_data = pd.DataFrame({
            "provinces": provinces,
            "avg": province_averages,
            "color": province_colors
        })
        st.write(compare_data)
        st.bar_chart(compare_data, 
                    x="provinces", 
                    y_label="Регіони", 
                    y="avg", 
                    x_label=f"Середнє значення {selected_area}", 
                    color="color", 
                    horizontal=True
        )
        