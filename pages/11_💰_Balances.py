# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import PIL

# Global Variables
theme_plotly = None # None or streamlit

# Page Favicon
favicon = PIL.Image.open('favicon.png')

# Layout
st.set_page_config(page_title='Wallet Balances - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('💰 Wallet Balances')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
@st.cache(ttl=3600)
def get_data(query):
    if query == 'Wallet Balances Distribution':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/eee5e19b-2632-4fec-b337-e52d85509eb5/data/latest')
    elif query == 'Wallet Balances Addresses':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/efb88e24-abba-44e3-ac66-2dfeedb4813b/data/latest')
    return None

balances_distribution = get_data('Wallet Balances Distribution')
balances_addresses = get_data('Wallet Balances Addresses')

# Content
st.subheader('NEAR Distribution')

df = balances_distribution

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='Bucket', y='Balance', color='Bucket', title='Total NEAR Balance', log_y=True)
    fig.update_layout(showlegend=False, yaxis_title='Balance [NEAR]')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.bar(df, x='Bucket', y='Addresses', color='Bucket', title='Total Addresses', log_y=True)
    fig.update_layout(showlegend=False, yaxis_title='Address')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='Balance', names='Bucket', title='Share of Total NEAR Balance')
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.pie(df, values='Addresses', names='Bucket', title='Share of Total Addresses')
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Top Addresses')

df = balances_addresses
fig = px.bar(df, x='Address', y='Balance', color='Address', title='NEAR Balance of Top Addresses')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Balance [NEAR]', xaxis={'categoryorder':'total ascending'})
fig.update_xaxes(type='category')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = sp.make_subplots()
fig.add_trace(go.Bar(x=df['Address'], y=df['Inflows'], name='Inflows'))
fig.add_trace(go.Bar(x=df['Address'], y=df['Outflows'], name='Outflows'))
fig.update_layout(title_text='Volume of Inflows and Outflows to Top Addresses', yaxis_title='Volume [NEAR]')
fig.update_xaxes(title=None, categoryorder='total ascending')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)