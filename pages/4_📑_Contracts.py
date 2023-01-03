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
st.set_page_config(page_title='Deployed Contracts - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('📑 Deployed Contracts')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
# @st.cache(ttl=600)
def get_data(query):
    if query == 'Contracts Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/6eb672c4-e52a-43c1-822f-a1e43cb52b10/data/latest')
    elif query == 'Contracts Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/cd150022-71ff-4d0b-8a79-53d1de1ec0b2/data/latest')
    return None

contracts_overview = get_data('Contracts Overview')
contracts_daily = get_data('Contracts Daily')

# Content
st.subheader('Overview')

st.metric(label='**Total Deployed Contracts**', value=str(contracts_overview['Contracts'].map('{:,.0f}'.format).values[0]))

fig = px.area(contracts_daily, x='Date', y='Contracts', title='Deployed Contracts Over Time')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Contracts')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)