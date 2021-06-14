import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import numpy as np
import altair as alt


#Intestazione Pagina
st.title('Predict Dashboard')

#H1
st.write('Previsione dei trend')

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
#st.write('Trend')
#st.line_chart(df_trend_g)


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

#df_predict_g
#st.write('Predict')
#st.line_chart(df_predict_g)


#Grafico Comparazione Trend e Predict
df_result_g = pd.concat([df_predict_g, df_trend_g], axis=1, join="inner")

df_result_g
st.write('Comparazione')
st.line_chart(df_result_g)



df_keywords = pd.read_csv('output_data/11_zz_finish.csv', sep='\t', decimal=',')
#df_predict_d
list_keywords = df_keywords['Week'].tolist()
#list_keywords

df_tredline = pd.read_csv('output_data/11_zz_finish.csv', sep='\t', decimal=',')






df_ads = pd.read_csv('output_data/6_google_ads_export-Volume.csv', sep='\t', decimal=',')
df_ads.fillna(0)
#df_ads
df_search_console = pd.read_csv('output_data/12_search_console_data.csv', sep='\t', decimal=',')
#df_search_console



st.write('Aggregato Predict')

df_predict = pd.DataFrame(list_keywords, columns =['keywords'])
df_predict = pd.merge(df_predict, df_ads, left_on='keywords', right_on='Keywords', how ='inner')

#Join Google Ads
df_predict.drop('Keywords', axis=1, inplace=True)
df_predict.drop('Category', axis=1, inplace=True)
df_predict.drop('Monthly Searches', axis=1, inplace=True)

#Join Google Search Console
df_predict = pd.merge(df_predict, df_search_console, left_on='keywords', right_on='query', how ='inner')
df_predict.drop('query', axis=1, inplace=True)

df_predict = df_predict.fillna(0)
df_predict





#
#
#
#
# test
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

