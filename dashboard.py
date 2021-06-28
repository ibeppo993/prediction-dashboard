import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from scipy.stats import linregress
from datetime import datetime

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



#
#
# Elenco date
last_trend_week = pd.read_csv('output_data/09_zz_finish.csv', sep='\t', decimal=',',  nrows=1).columns.tolist()
#last_trend_week
last_trend_week = last_trend_week[-1]
#st.write('last_trend_week')
#last_trend_week

last_predit_week = pd.read_csv('output_data/11_zz_finish.csv', sep='\t', decimal=',',  nrows=1).columns.tolist()
#last_predit_week
#st.write(type(last_predit_week))
last_predit_week = last_predit_week[-8:]
#st.write('last_predit_week')
#last_predit_week

#
#
#
#
# Creazione dataframe
df_keywords = pd.read_csv('output_data/11_zz_finish.csv', sep='\t', decimal=',')
list_keywords = df_keywords['Week'].tolist()
#st.write('list_keywords')
#list_keywords
df_complete = pd.DataFrame(list_keywords, columns =['keywords'])
#df_complete

df_trend = pd.read_csv('output_data/09_zz_finish.csv', sep='\t', decimal=',')
#st.write('df_trend')
#df_trend

df_trend_zero = pd.read_csv('output_data/09_zz_finish.csv', sep='\t', decimal=',')
#st.write('df_trend_zero')
df_trend_zero['Accuratezza'] = (df_trend_zero == 0).astype(int).sum(axis=1)
df_trend_zero = df_trend_zero[['Week','Accuratezza']]
#df_trend_zero


df_forecast = pd.read_csv('output_data/11_zz_finish.csv', sep='\t', decimal=',')
#st.write('df_forecast')
#df_forecast

df_forecast_1_100 = pd.read_csv('output_data/11_zz_finish_0_100.csv', sep='\t', decimal=',')
df_forecast_1_100['HighScore_predict'] = df_forecast_1_100[last_predit_week].max(axis=1)
#st.write('df_forecast_1_100')
#df_forecast_1_100
df_forecast_1_100_slope = df_forecast_1_100.copy()

df_ads = pd.read_csv('output_data/6_google_ads_export-Volume.csv', sep='\t', decimal=',')
df_ads.fillna(0)
#st.write('df_ads')
#df_ads

df_search_console = pd.read_csv('output_data/12_search_console_data.csv', sep='\t', decimal=',')
#st.write('df_search_console')
#df_search_console

#
#
#
# Composizione dataframe

#aggiunta accuratezza
df_complete = pd.merge(df_complete, df_trend_zero, left_on='keywords', right_on='Week', how ='inner')
df_complete.drop('Week', axis=1, inplace=True)


#aggiunta gads
df_complete = pd.merge(df_complete, df_ads, left_on='keywords', right_on='Keywords', how ='inner')
df_complete.drop(['Keywords','Category','Monthly Searches'], axis=1, inplace=True)

#aggiunta search console
df_complete = pd.merge(df_complete, df_search_console, left_on='keywords', right_on='query', how ='inner')
df_complete.drop('query', axis=1, inplace=True)


df_trend = df_trend.iloc[:, list(range(1)) + [-1]]
#df_trend
df_complete = pd.merge(df_complete, df_trend, left_on='keywords', right_on='Week', how ='inner')
df_complete.drop('Week', axis=1, inplace=True)

#df_forecast_1_100 = df_forecast_1_100.iloc[:, list(range(1)) + [-9,-8,-7,-6,-5,-4,-3,-2,-1]]
df_forecast_1_100 = df_forecast_1_100.iloc[:, list(range(1)) + [-1]]


#df_forecast_1_100
df_complete = pd.merge(df_complete, df_forecast_1_100, left_on='keywords', right_on='Week', how ='inner')
df_complete.drop('Week', axis=1, inplace=True)

df1 = pd.DataFrame()
empty_list = []
df1['keywords'] = empty_list
df1['slope_trendline'] = empty_list
for x in df_forecast_1_100_slope['Week']:
    #x
    new_df = df_forecast_1_100_slope.loc[df_forecast_1_100_slope['Week'] == x]
    new_df = pd.concat([new_df.iloc[:,0],new_df.iloc[:,-10:]],axis = 1)
    #new_df
    new_df = df_forecast_1_100_slope.loc[df_forecast_1_100_slope['Week'] == x]
    new_df = pd.concat([new_df.iloc[:,0],new_df.iloc[:,-10:]],axis = 1)
    #creazione x
    x_list = list(new_df.columns.values)
    x_list = x_list[1:]
    n_value = len(x_list)
    x_list = list(range(0, n_value))
    #creazione y
    y_list = new_df.values.tolist()
    y_list = [item for sublist in y_list for item in sublist]
    y_list = y_list[1:]
    #print(y_list)
    slope, intercept, r_value, p_value, std_err = linregress(x_list, y_list)
    #print(slope)
    #df_forecast_1_100_slope.loc[df_forecast_1_100_slope.Week == x, "slope_trendline"] = slope
    #print(df_tredline)
    dictionary = {'keywords': x, 'slope_trendline': slope}
    df1 = df1.append(dictionary, ignore_index=True)

df_complete = pd.merge(left=df_complete, right=df1, how='left', left_on='keywords', right_on='keywords')

df_complete.dropna()
df_complete = df_complete[(df_complete.HighScore_predict > 95) & (df_complete.Accuratezza < 15)]
df_complete.sort_values(by=['Search Volume'], inplace=True, ascending=False)
df_complete = df_complete.rename(columns={f'{last_trend_week}': 'Last_Trend'})

st.write('df_complete')
#df_complete
st.dataframe(df_complete)







# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     (list_keywords)
# )