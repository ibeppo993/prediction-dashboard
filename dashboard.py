import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
#from scipy.stats import linregress
from datetime import datetime
import base64 as b64


def _max_width_():
    max_width_str = f"max-width: 1500px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True, 
    )
_max_width_()

#Intestazione Pagina
st.title('Predict Dashboard')

#H1
#st.write('Previsione dei trend')

#Grafico con Trend
df_trend_g = pd.read_csv('output_data/09_zz_finish.csv', sep='\t')
df_trend_g = df_trend_g.replace(np.nan, 'Unknown')
df_trend_g = df_trend_g.append(df_trend_g.sum(numeric_only=True), ignore_index=True)
df_trend_g = df_trend_g.tail(1)
df_trend_g['Week'].fillna('Generale', inplace=True)
df_trend_g = df_trend_g.drop(['Week'], axis=1)

df_trend_g.reset_index(drop=True, inplace=True)
df_trend_g.insert(0, 'trend', 'trend')
df_trend_g.set_index('trend', inplace = True)
df_trend_g.index.name = None

df_trend_g = df_trend_g.T

#df_trend_g
df_trend_g_chart = df_trend_g.copy()
#st.write('Trend')

df_trend_g_chart.reset_index(inplace=True)
df_trend_g_chart['index'] = df_trend_g_chart['index'].astype('datetime64[ns]')
#df_trend_g_chart
chart_trend = alt.Chart(df_trend_g_chart).mark_line().encode(
    x=alt.X('index'),
    y=alt.Y('trend')
).properties(title="Trend Forecast")

#st.altair_chart(chart_trend, use_container_width=True)
#st.line_chart(df_trend_g)

#
#
#Grafico con Predict
df_predict_g = pd.read_csv('output_data/11_zz_finish.csv', sep='\t', decimal=',')
df_predict_g = df_predict_g.replace(np.nan, 'Unknown')
df_predict_g = df_predict_g.append(df_predict_g.sum(numeric_only=True), ignore_index=True)
df_predict_g = df_predict_g.tail(1)
df_predict_g['Week'].fillna('Generale', inplace=True)
df_predict_g = df_predict_g.drop(['Week'], axis=1)

df_predict_g.reset_index(drop=True, inplace=True)
df_predict_g.insert(0, 'predict', 'predict')
df_predict_g.set_index('predict', inplace = True)
df_predict_g.index.name = None

df_predict_g = df_predict_g.T

#df_predict_g = df_predict_g.reset_index()

#df_predict_g
#st.write('Predict')

df_predict_g_chart = df_predict_g.copy()

df_predict_g_chart.reset_index(inplace=True)
df_predict_g_chart['index'] = df_predict_g_chart['index'].astype('datetime64[ns]')
#df_predict_g_chart

chart_prophet = alt.Chart(df_predict_g_chart).mark_line().encode(
    x=alt.X('index'),
    y=alt.Y('predict')
).properties(title="Trend Forecast")
#st.altair_chart(chart_prophet, use_container_width=True)


#
#
#Grafico Comparazione Trend e Predict
#st.write('Forecast')
#df_result_g = pd.concat([df_predict_g_chart, df_trend_g_chart], axis=1, join="inner")

#df_result_g
st.write('Comparazione')
#st.line_chart(df_result_g)


full_df = pd.merge(df_predict_g_chart, df_trend_g_chart, left_on='index', right_on='index', how='left')
a = alt.Chart(full_df).mark_area(opacity=0.8, color='blue').encode(x='index', y='trend')
b = alt.Chart(full_df).mark_area(opacity=0.6, color='orange').encode(x='index', y='predict')
c = alt.layer(a, b).properties(title="Forecast and Trend Comparison")
st.altair_chart(c, use_container_width=True)

st.write('---------------------------------------------------')


df_complete = pd.read_csv('output_data/14_for_streamlit.csv', sep='\t', decimal=',')

#st.write('df_complete')
index = df_complete.index
number_of_rows = len(index)
number_of_rows
#df_complete
st.dataframe(df_complete)

def get_table_download_link_csv(df_complete):
    #csv = df.to_csv(index=False)
    csv = df_complete.to_csv().encode()
    #b64 = base64.b64encode(csv.encode()).decode() 
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download csv file</a>'
    return href

st.markdown(get_table_download_link_csv(df_complete), unsafe_allow_html=True)
# add_selectbox = st.sidebar.selectbox(
#     'Filtro per keyword',
#     (list_keywords)
# )