import streamlit_authenticator as stauth
import streamlit as st

import pandas as pd
import plotly.express as px

# st.set_page_config(page_title="Tuvansa Dashboard", page_icon=":bar_chart", layout='wide')

st.set_page_config(page_title="Tamsa Sales", page_icon=":bar_chart", layout='wide')

names = ['Roy Grinberg', 'Marcos Avalos', 'Alejandro Lozano']
usernames = ['rgrinberg', 'mavalos' , 'alozano']
passwords = ['$2b$12$aZkuuz.79QGY49OE1UJXr.0ARLtfaHLxTGfeeWSYIVzTiCD3JjFCq', '$2b$12$BBSQuSg95vfO/3iWKPFePuJBsjRESrlbWWklOLwaM9KerS7VNc3yW', '$2b$12$PSeEziaeEdjKTaud4yd.aunk5qnxsg9jBp9BLjnKnljiqgtY8BCzm']
authenticator = stauth.Authenticate(
  names, 
  usernames, 
  passwords,
  'streamlitCookieTamsa', 
  '18309138', 
  cookie_expiry_days=30
)

# Manejar el inicio de sesión
name, authentication_status, username = authenticator.login('Login', 'main')


if authentication_status:

  col3, col4 = st.columns(2)

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
  
  with st.sidebar:
    authenticator.logout('Logout', 'main')  
    st.write(f'Bienvenido {name}')
    st.write("Contenido protegido por autenticación")
    st.title(":bar_chart: Dashboard TAMSA")
    st.subheader("Ventas Mensuales por empresa")
    empresas = st.selectbox("Elige la empresa", df["NombreRazonSocialReceptor"].unique())
    selectedYear = st.selectbox('Elige un año', df["year"].dropna().unique())
    topValue = st.number_input("Escribe el valor del Top", value=10)



  salesByMonth = df.groupby(by=["Mes","Month"])['Total'].sum().reset_index()


  competidoresRfcList = ["EGU800818ST2","LAV751101B63","MIB820517DS8","MIC990201JR8","MIG000330RNA","MIM7207049C1","MIM9706191V8","PAC040303UY6","TMO831114QV9","TVN7407019H3","VIT841218650","TVN820506NT0"] 

  empresaName = empresas
  
  competidoresData = df[(df["RfcReceptor"].isin(competidoresRfcList)) & (df["year"] == selectedYear )].sort_values("RfcReceptor")

  
  competidoresData = competidoresData.groupby(by=["RfcReceptor"]).agg({'NombreRazonSocialReceptor':'first', 'Total':'sum'}).reset_index().sort_values("Total", ascending=False)
  
  # competidoresData
  
  # Crear la gráfica de barras
  fig = px.bar(competidoresData, x='NombreRazonSocialReceptor', y='Total', 
             title=f"Venta a competidores {selectedYear}",
             labels={'NombreRazonSocialReceptor': 'Nombre del Receptor', 'Total': 'Total ($)'},
             text_auto=True)
  
  st.plotly_chart(fig,use_container_width=True, height = 500 )
  

  empresas = df[(df["NombreRazonSocialReceptor"] == empresas) & (df["year"] == selectedYear)]["RfcReceptor"].iloc[0]

  # Top 2023
  st.subheader(f"Top 10 {selectedYear}")
  rfcReceptor_df = df.sort_values("Total")
  rfcReceptor_df = df[df['year'] == selectedYear]
  rfcReceptor_df = rfcReceptor_df.groupby(by=["RfcReceptor"]).agg({'NombreRazonSocialReceptor':'first', 'Total':'sum'}).reset_index()
  rfcReceptor_df = rfcReceptor_df.sort_values("Total", ascending=False)
  fig = px.bar(rfcReceptor_df.head(topValue), x="Total", y="NombreRazonSocialReceptor", orientation="h",text=['${:,.2f}'.format(x) for x in rfcReceptor_df.head(topValue)["Total"]], template="seaborn")
  st.plotly_chart(fig,use_container_width=True, height = 500)
  
  
  st.subheader(f"Tabla Venta total por empresa {selectedYear}")
  st.dataframe(rfcReceptor_df, use_container_width=True) 


  df3 = df[(df["RfcReceptor"] == empresas) & (df["year"] == selectedYear)]
  df3 = df3.groupby(by=["Mes","Month"])['Total'].sum().reset_index()
  totalAnual = df3['Total'].sum()
  totalAnual = totalAnual
  with st.container():
    # title = f"Venta anual tamsa a: {empresaName}" + ' ' + "${:,.2f}".format(totalAnual) 
    st.subheader(f"{selectedYear} Venta anual tamsa a: {empresaName}" + ' ' + "${:,.2f}".format(totalAnual) )
    fig = px.line(df3, x="Month", y="Total", text=['${:,.2f}'.format(x) for x in df3["Total"]], template="seaborn")

    st.plotly_chart(fig, use_container_width=True )

  st.subheader(f"{selectedYear} Ventas Mensuales TAMSA")
  fig = px.line(salesByMonth, x="Month", y="Total", text=['${:,.2f}'.format(x) for x in salesByMonth["Total"] ], template="seaborn" )
  st.plotly_chart(fig, use_container_width=True, height = 200)
elif authentication_status == False:
    st.error('Nombre de usuario o contraseña incorrectos')
elif authentication_status == None:
    st.warning('Por favor, ingresa tus credenciales')











