import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Tamsa Sales", page_icon=":bar_chart", layout='wide')
st.title(":bar_chart: Dashboard TAMSA")
col1, col2 = st.columns(2)

@st.cache_data
def load(file):
  return pd.read_excel(file, sheet_name="Emitidos_2023").copy()

df = load('./tamsa2.xlsx')

df["FechaEmision"] = pd.to_datetime(df["FechaEmision"])
df["Mes"] = df["FechaEmision"].dt.month
df["Month"] = df["FechaEmision"].dt.strftime('%b')
df["year"] = df["FechaEmision"].dt.year

# st.sidebar.header("Escoge el filtro")
# rfcReceptor = st.sidebar.multiselect("Elige la empresa", df["RfcReceptor"].unique() )

# if not rfcReceptor:
#   df2 = df.copy()
# else:
#   df2 = df[df["RfcReceptor"].isin(rfcReceptor)]

# df2

rfcReceptor_df = df.sort_values("Total")


rfcReceptor_df = rfcReceptor_df.groupby(by=["RfcReceptor"]).agg({'NombreRazonSocialReceptor':'first', 'Total':'sum'}).reset_index()
rfcReceptor_df = rfcReceptor_df.sort_values("Total", ascending=False)


salesByMonth = df.groupby(by=["Mes","Month"])['Total'].sum().reset_index()


st.subheader("Ventas Mensuales por empresa")
empresas = st.selectbox("Elige la empresa", df["NombreRazonSocialReceptor"].unique())

empresas = df[df["NombreRazonSocialReceptor"] == empresas]["RfcReceptor"].iloc[0]


if not empresas:
  df3 = df
else:
  df3 = df[(df["RfcReceptor"] == empresas) & (df["year"] == 2023)]
  df3 = df3.groupby(by=["Mes","Month"])['Total'].sum().reset_index()
  totalAnual = df3['Total'].sum()

  totalAnual = totalAnual
with st.container():
  title = "Venta anual" + ' ' + "${:,.2f}".format(totalAnual) 
  fig = px.line(df3, x="Month", y="Total", text=['${:,.2f}'.format(x) for x in df3["Total"]], template="seaborn", title=title)
  
  st.plotly_chart(fig, use_container_width=True )


st.subheader("Ventas Mensuales TAMSA")
fig = px.line(salesByMonth, x="Month", y="Total", text=['${:,.2f}'.format(x) for x in salesByMonth["Total"] ], template="seaborn" )
st.plotly_chart(fig, use_container_width=True, height = 200)







with col1:
  st.subheader("Tabla Venta total por empresa 2023")
  rfcReceptor_df
with col2:
  st.subheader("Top 10 2023")
  fig = px.bar(rfcReceptor_df.head(10), x="Total", y="NombreRazonSocialReceptor", orientation="h",text=['${:,.2f}'.format(x) for x in rfcReceptor_df.head(10)["Total"]], template="seaborn")
  st.plotly_chart(fig,use_container_width=True, height = 200)



