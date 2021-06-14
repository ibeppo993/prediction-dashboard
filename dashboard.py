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
df_trend = pd.read_csv('output_data/09_zz_finish.csv', sep='\t')
df_trend = df_trend.replace(np.nan, 'Unknown')
df_trend = df_trend.append(df_trend.sum(numeric_only=True), ignore_index=True)
df_trend = df_trend.tail(1)
df_trend['Week'].fillna('Generale', inplace=True)
df_trend = df_trend.drop(['Week'], axis=1)

df_trend.reset_index(drop=True, inplace=True)
df_trend.insert(0, 'trend', 'trend')
df_trend.set_index('trend', inplace = True)
df_trend.index.name = None

df_trend = df_trend.T

df_trend
st.write('Trend')
st.line_chart(df_trend)


#Grafico con Predict
df_predict = pd.read_csv('output_data/11_zz_finish.csv', sep='\t', decimal=',')
df_predict = df_predict.replace(np.nan, 'Unknown')
df_predict = df_predict.append(df_predict.sum(numeric_only=True), ignore_index=True)
df_predict = df_predict.tail(1)
df_predict['Week'].fillna('Generale', inplace=True)
df_predict = df_predict.drop(['Week'], axis=1)

df_predict.reset_index(drop=True, inplace=True)
df_predict.insert(0, 'predict', 'predict')
df_predict.set_index('predict', inplace = True)
df_predict.index.name = None

df_predict = df_predict.T

df_predict
st.write('Predict')
st.line_chart(df_predict)


#Grafico Comparazione Trend e Predict
df_result = pd.concat([df_predict, df_trend], axis=1, join="inner")

df_result
st.write('Comparazione')
st.line_chart(df_result)


