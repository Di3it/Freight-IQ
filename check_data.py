import pandas as pd

print('=== BDI ===')
bdi = pd.read_csv('data/baltic_dry_index.csv')
print(bdi.columns.tolist())
print(bdi.head())

print('=== India Ports ===')
india = pd.read_excel('data/port_data_india.xlsx')
print(india.columns.tolist())
print(india.head())

print('=== Origin Ports ===')
origin = pd.read_excel('data/port_data_origin.xlsx')
print(origin.columns.tolist())
print(origin.head())