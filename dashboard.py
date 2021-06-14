import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import numpy as np

#Intestazione Pagina
st.title('Predict Dashboard')

st.write('Previsione dei trend')

df = pd.read_csv('output_data/09_zz_finish.csv', sep='\t')

df = df.replace(np.nan, 'Unknown')
df2 = df.append(df.sum(numeric_only=True), ignore_index=True)
df2 = df2.tail(1)
df2['Week'].fillna('Generale', inplace=True)

df2


