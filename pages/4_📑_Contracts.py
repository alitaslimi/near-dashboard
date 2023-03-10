# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import PIL
import data

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
contracts_overview = data.get_data('Contracts Overview')
contracts_daily = data.get_data('Contracts Daily')
contracts_interactions_overview = data.get_data('Contracts Interactions Overview')
contracts_interactions_daily = data.get_data('Contracts Interactions Daily')

# Content
st.subheader('Overview')

st.metric(label='**Total Deployed Contracts**', value=str(contracts_overview['Contracts'].map('{:,.0f}'.format).values[0]))

st.subheader('Interactions')

c1, c2 = st.columns(2)
with c1:
    df = contracts_interactions_overview.sort_values('Transactions', ascending=False).head(20)
    fig = px.bar(df, x='Contract', y='Transactions', color='Contract', title='Total Transactions of Top Contracts', log_y=True)
    fig.update_layout(showlegend=False, yaxis_title='Transactions')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    df = contracts_interactions_overview.sort_values('Users', ascending=False).head(20)
    fig = px.bar(df, x='Contract', y='Users', color='Contract', title='Total Users of Top Contracts', log_y=True)
    fig.update_layout(showlegend=False, yaxis_title='Users')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Activity Over Time')

interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='burrow_interval', horizontal=True)

if st.session_state.burrow_interval == 'Daily':
    contracts_over_time = contracts_daily
    df = contracts_interactions_daily
    df['RowNumber'] = df.groupby('Date')['Transactions'].rank(method='max', ascending=False)
    df.loc[df['RowNumber'] > 5, 'Contract'] = 'Other'
    df = df.groupby(['Date', 'Contract']).agg('sum').reset_index()
elif st.session_state.burrow_interval == 'Weekly':
    contracts_over_time = contracts_daily
    contracts_over_time = contracts_over_time.groupby([pd.Grouper(freq='W', key='Date')]).agg('sum').reset_index()
    df = contracts_interactions_daily
    df = df.groupby([pd.Grouper(freq='W', key='Date'), 'Contract']).agg('sum').reset_index()
    df['RowNumber'] = df.groupby('Date')['Transactions'].rank(method='max', ascending=False)
    df.loc[df['RowNumber'] > 5, 'Contract'] = 'Other'
    df = df.groupby(['Date', 'Contract']).agg('sum').reset_index()
elif st.session_state.burrow_interval == 'Monthly':
    contracts_over_time = contracts_daily
    contracts_over_time = contracts_over_time.groupby([pd.Grouper(freq='MS', key='Date')]).agg('sum').reset_index()
    df = contracts_interactions_daily
    df = df.groupby([pd.Grouper(freq='MS', key='Date'), 'Contract']).agg('sum').reset_index()
    df['RowNumber'] = df.groupby('Date')['Transactions'].rank(method='max', ascending=False)
    df.loc[df['RowNumber'] > 5, 'Contract'] = 'Other'
    df = df.groupby(['Date', 'Contract']).agg('sum').reset_index()

fig = px.area(contracts_over_time, x='Date', y='Contracts', title='Deployed Contracts Over Time')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Contracts')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df.sort_values(['Date', 'Transactions'], ascending=[True, False]), x='Date', y='Transactions', color='Contract', custom_data=['Contract'], title='Transactions Conducted on Top Contracts Over Time')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df.sort_values(['Date', 'Users'], ascending=[True, False]), x='Date', y='Users', color='Contract', custom_data=['Contract'], title='Users Interacting with Top Contracts Over Time')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)