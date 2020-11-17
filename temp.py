import pandas as pd 


df0 = pd.read_csv('data/preprocessed_data_update_0.csv')
print(1)
df1 = pd.read_csv('data/preprocessed_data_update_1.csv')
print(1)

df2 = pd.read_csv('data/preprocessed_data_update_2.csv')
print(1)

df3 = pd.read_csv('data/preprocessed_data_update_3.csv')
print(1)

df4 = pd.read_csv('data/preprocessed_data_update_4.csv')
print(1)

df5 = pd.read_csv('data/preprocessed_data_update_5.csv')
print(1)

df6 = pd.read_csv('data/preprocessed_data_update_6.csv')
print(1)



print(11111)




result = pd.merge(df0, df1, how='outer')

print(1)

result = pd.merge(result, df2, how='outer')

print(1)

result = pd.merge(result, df3, how='outer')

print(1)

result = pd.merge(result, df4, how='outer')

print(1)

result = pd.merge(result, df5, how='outer')
result = pd.merge(result, df6, how='outer')

print(111111)

result = pd.merge(result, pd.read_csv('data/preprocessed_data.csv'), how='outer')

print('hihi')
result.to_csv('data/preprocessed_data.csv')


