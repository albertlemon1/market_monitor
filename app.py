import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="WealthTech Light", layout="wide")

st.title("📊 WealthTech: Monitor de Mercado Light")

# Cargar datos
if os.path.exists('data/market_data.csv'):
    # Cargamos el CSV (el índice es la fecha 'Date')
    df = pd.read_csv('data/market_data.csv', index_col=0, parse_dates=True)
    # Aseguramos orden cronológico para cálculos correctos
    df = df.sort_index()
    
    # Selector de Ticker
    ticker_list = df.columns
    selected_ticker = st.selectbox("Selecciona una acción:", ticker_list)
    
    # --- NUEVA SECCIÓN: Indicador de Valor Actual ---
    # Obtenemos los datos del ticker seleccionado
    ticker_series = df[selected_ticker]
    
    # El valor actual es el último registro (iloc[-1])
    current_price = ticker_series.iloc[-1]
    last_date = ticker_series.index[-1].strftime('%Y-%m-%d')
    
    # Calculamos el cambio con respecto al día anterior (iloc[-2]) para el indicador delta
    if len(ticker_series) > 1:
        previous_price = ticker_series.iloc[-2]
        change = current_price - previous_price
        change_percent = (change / previous_price) * 100
    else:
        change = 0
        change_percent = 0

    # Mostramos la métrica destacada
    st.metric(
        label=f"Valor de Cierre Actual ({selected_ticker} al {last_date})",
        value=f"${current_price:.2f}",
        delta=f"{change:.2f} ({change_percent:.2f}%)"
    )
    # -------------------------------------------------
    
    # Layout de columnas (2/3 gráfica, 1/3 tabla)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Histórico de 1 año")
        fig = px.line(df, y=selected_ticker, template="plotly_dark")
        # Mejoramos el hover para mostrar precios bonitos
        fig.update_traces(mode="lines", hovertemplate='%{x}: $%{y:.2f}')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Últimos 10 días registrados")
        # Mostramos los últimos 10, ordenados descendente por fecha
        table_df = ticker_series.tail(10).sort_index(ascending=False).reset_index()
        # Damos formato de moneda a la tabla
        st.dataframe(
            table_df.style.format({'Date': '{:%Y-%m-%d}', selected_ticker: '${:.2f}'}),
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("Aún no hay datos disponibles. El pipeline debe ejecutarse primero.")
    st.info("Corre 'python update_data.py' en tu terminal.")