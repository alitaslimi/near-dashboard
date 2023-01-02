# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import PIL

# Global Variables
theme_plotly = None # None or streamlit
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Page Favicon
favicon = PIL.Image.open('favicon.png')

# Layout
st.set_page_config(page_title='NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('NEAR Mega Dashboard')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
# @st.cache(ttl=600)
def get_data(query):
    if query == 'Transfers Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/748dc207-2309-4afb-8b09-9e979aa6007f/data/latest')
    elif query == 'Transfers Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e4353f8e-2e61-486e-8d7f-d5bf05d9bfed/data/latest')
    elif query == 'Transfers Heatmap':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9135ad92-3e0c-4c07-9af8-905f204533eb/data/latest')
    elif query == 'Transfers Assets Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/c14f77c5-76be-4fc1-8e50-595462b36f64/data/latest')
    elif query == 'Transfers Assets Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/c1e767c2-3601-43e4-b159-f5fb8efbedfb/data/latest')
    return None

transfers_overview = get_data('Transfers Overview')
transfers_daily = get_data('Transfers Daily')
transfers_heatmap = get_data('Transfers Heatmap')
transfers_assets_overview = get_data('Transfers Assets Overview')
transfers_assets_daily = get_data('Transfers Assets Daily')

# Content
st.subheader('Overview')

fig = px.area(transfers_assets_daily.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='Asset', title='Daily Transferred Volume')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
fig.add_annotation(x='2022-05-12', y=35000000, text='Terra Collapse', showarrow=False, xanchor='left')
fig.add_shape(type='line', x0='2022-05-12', x1='2022-05-12', y0=0, y1=1, xref='x', yref='paper', line=dict(width=1, dash='dot'))
fig.add_annotation(x='2022-11-10', y=6000000, text='FTX Collapse', showarrow=False, xanchor='left')
fig.add_shape(type='line', x0='2022-11-10', x1='2022-11-10', y0=0, y1=1, xref='x', yref='paper', line=dict(width=1, dash='dot'))
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# Credits
c1, c2 = st.columns(2)
with c1:
    st.info('**Data Analyst: [@AliTslm](https://twitter.com/AliTslm)**', icon="💻")
with c2:
    st.info('**Data: [Flipside Crypto](https://flipsidecrypto.xyz/)**', icon="🧠")
