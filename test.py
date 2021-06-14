
import pandas as pd
import numpy as np

#Intestazione Pagina

df = pd.read_csv('output_data/09_zz_finish.csv', sep='\t')

df = df.replace(np.nan, 'Unknown')
df2 = df.append(df.sum(numeric_only=True), ignore_index=True)
df2 = df2.tail(1)
df2['Week'].fillna('Generale', inplace=True)
df2 = df2.drop(['Week'], axis=1)


df2.reset_index(drop=True, inplace=True)
df2.insert(0, 'predict', 'predict')
print(df2)
df2.set_index('predict', inplace = True)
df2.index.name = None

print(df2)


df2_transposed = df2.T

print(df2_transposed)
# '''
# dict = {1018: 'Predict'}
# for col in df2_transposed.columns:
#     print(col)
#     print(type(col))
# df2_transposed.rename(columns=dict, inplace=True)
# '''

# #df2_transposed = df2_transposed.rename(columns={df2_transposed.columns[1]: 'new'})

# print(df2_transposed.columns.values[0])
# print(type(df2_transposed.columns.values[0]))
# df2_transposed.columns.values[0] = "b"


# print(df2_transposed)