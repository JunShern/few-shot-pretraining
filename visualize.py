import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

data_dir = "./output"
data_path = Path(data_dir) / "results.csv"

st.title('Scavenged Output')

# dtypes = [str, int, int, str]
df = pd.read_csv(str(data_path))
print(df)

df1 = df.select_dtypes(include=bool)
print(df1)

df2 = df1.apply(pd.value_counts).loc[True]
print(df2)

st.table(df2)
st.bar_chart(df2)

# df.dtypes
# st.write(df.dtypes)
# df.select_dtypes(bool)