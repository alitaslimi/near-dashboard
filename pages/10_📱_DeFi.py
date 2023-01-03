# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import PIL

# Global Variables
theme_plotly = None # None or streamlit
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Page Favicon
favicon = PIL.Image.open('favicon.png')

# Layout
st.set_page_config(page_title='DeFi - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('📱 DeFi')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
# @st.cache(ttl=600)
def get_data(query):
    if query == 'Burrow Netflow':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/215ed4b5-e745-42f9-be3c-87b724ffa22a/data/latest')
    elif query == 'Burrow Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/8eb9c5ea-e4bc-41cf-97c4-30e319ffc0cf/data/latest')
    return None

burrow_netflow = get_data('Burrow Netflow')
burrow_overview = get_data('Burrow Overview')

# Content
tab_burrow, tab_test = st.tabs(['**Burrow**', 'test'])

with tab_burrow:

    st.subheader('Overview')

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Inflow**', value=str(burrow_netflow['Inflow'].map('{:,.0f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Outflow**', value=str(burrow_netflow['Outflow'].map('{:,.0f}'.format).values[0]), help='USD')
    with c3:
        st.metric(label='**Netflow**', value=str(burrow_netflow['Netflow'].map('{:,.0f}'.format).values[0]), help='USD')

    st.subheader('Market Shares')
    
    df = burrow_overview
    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.pie(df, values='Volume', names='Action', title='Share of Total Transferred Volume')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.pie(df, values='Volume', names='Token', title='Share of Total Transferred Volume')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Transactions', names='Action', title='Share of Total Transactions')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.pie(df, values='Transactions', names='Token', title='Share of Total Transactions')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(df, values='Users', names='Action', title='Share of Total Users')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.pie(df, values='Users', names='Token', title='Share of Total Users')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)