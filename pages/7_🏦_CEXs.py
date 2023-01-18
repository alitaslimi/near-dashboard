# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import PIL

# Global Variables
theme_plotly = None # None or streamlit

# Page Favicon
favicon = PIL.Image.open('favicon.png')

# Layout
st.set_page_config(page_title='CEXs - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('🌍 CEXs')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
@st.cache(ttl=1000, allow_output_mutation=True)
def get_data(query):
    if query == 'CEXs Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/3c4330b0-36d2-4016-a092-1fb72b414f80/data/latest')
    elif query == 'CEXs Exchanges Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/ea5814fb-ba21-4b01-9e12-0d44f25980a8/data/latest')
    elif query == 'CEXs Exchanges Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/84fc0987-4902-4295-82de-dbdcf0703660/data/latest')
    return None

cexs_overview = get_data('CEXs Overview')
cexs_exchanges_overview = get_data('CEXs Exchanges Overview')
cexs_exchanges_daily = get_data('CEXs Exchanges Daily')

# Content
st.subheader('Overview')

c1, c2, c3 = st.columns(3)
with c1:
    fig = px.pie(cexs_overview, values='Volume', names='Flow', title='Share of Total Transferred Volume', hole=0.4)
    fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(cexs_overview, values='Transactions', names='Flow', title='Share of Total Transactions', hole=0.4)
    fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c3:
    fig = px.pie(cexs_overview, values='Users', names='Flow', title='Share of Total Users Interacting With CEX Addresses', hole=0.4)
    fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Market Shares')

c1, c2, c3 = st.columns(3)
df = cexs_exchanges_overview.query("Flow == 'Inflow'")
with c1:
    fig = px.pie(df, values='Volume', names='CEX', title='Share of Inflow Volume', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='Transactions', names='CEX', title='Share of Inflow Transactions', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c3:
    fig = px.pie(df, values='Users', names='CEX', title='Share of Asset Senders', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

df = cexs_exchanges_overview.query("Flow == 'Outflow'")
with c1:
    fig = px.pie(df, values='Volume', names='CEX', title='Share of Outflow Volume', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='Transactions', names='CEX', title='Share of Outflow Transactions', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c3:
    fig = px.pie(df, values='Users', names='CEX', title='Share of Asset Receivers', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Activity Over Time')

interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='cexs_interval', horizontal=True)

if st.session_state.cexs_interval == 'Daily':
    dfi = cexs_exchanges_daily.query("Flow == 'Inflow'")
    dfi = dfi.groupby(['Date', 'CEX']).agg({'Transactions': 'sum', 'Users': 'sum', 'Volume': 'sum'}).reset_index()
    dfo = cexs_exchanges_daily.query("Flow == 'Outflow'")
    dfo = dfo.groupby(['Date', 'CEX']).agg({'Transactions': 'sum', 'Users': 'sum', 'Volume': 'sum'}).reset_index()
elif st.session_state.cexs_interval == 'Weekly':
    dfi = cexs_exchanges_daily.query("Flow == 'Inflow'")
    dfi = dfi.groupby([pd.Grouper(freq='W', key='Date'), 'CEX']).agg({'Transactions': 'sum', 'Users': 'sum', 'Volume': 'sum'}).reset_index()
    dfo = cexs_exchanges_daily.query("Flow == 'Outflow'")
    dfo = dfo.groupby([pd.Grouper(freq='W', key='Date'), 'CEX']).agg({'Transactions': 'sum', 'Users': 'sum', 'Volume': 'sum'}).reset_index()
elif st.session_state.cexs_interval == 'Monthly':
    dfi = cexs_exchanges_daily.query("Flow == 'Inflow'")
    dfi = dfi.groupby([pd.Grouper(freq='MS', key='Date'), 'CEX']).agg({'Transactions': 'sum', 'Users': 'sum', 'Volume': 'sum'}).reset_index()
    dfo = cexs_exchanges_daily.query("Flow == 'Outflow'")
    dfo = dfo.groupby([pd.Grouper(freq='MS', key='Date'), 'CEX']).agg({'Transactions': 'sum', 'Users': 'sum', 'Volume': 'sum'}).reset_index()

c1, c2 = st.columns(2)
with c1:
    fig = px.line(dfi, x='Date', y='Volume', color='CEX', custom_data=['CEX'], title='Inflow Volume of CEXs Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.line(dfi, x='Date', y='Transactions', color='CEX', custom_data=['CEX'], title='Inflow Transactions of CEXs Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.line(dfi, x='Date', y='Users', color='CEX', custom_data=['CEX'], title='Asset Senders of CEXs Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Senders', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.line(dfo, x='Date', y='Volume', color='CEX', custom_data=['CEX'], title='Outflow Volume of CEXs Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.line(dfo, x='Date', y='Transactions', color='CEX', custom_data=['CEX'], title='Outflow Transactions of CEXs Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.line(dfo, x='Date', y='Users', color='CEX', custom_data=['CEX'], title='Asset Receivers of CEXs Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Receivers', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)