# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import PIL
import data

# Global Variables
theme_plotly = None # None or streamlit

# Page Favicon
favicon = PIL.Image.open('favicon.png')

# Layout
st.set_page_config(page_title='Lending - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('📒 Lending')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
burrow_netflow = data.get_data('Burrow Netflow')
burrow_overview = data.get_data('Burrow Overview')
burrow_daily = data.get_data('Burrow Daily')
burrow_liquidity_overview = data.get_data('Burrow Liquidity Overview')
burrow_liquidity_daily = data.get_data('Burrow Liquidity Daily')

st.subheader('Overview of Burrow')

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
    fig = px.pie(df, values='Volume', names='Action', title='Share of Total Volume')
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.pie(df, values='Volume', names='Token', title='Share of Total Volume')
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

st.subheader('Liquidity')

df = burrow_liquidity_overview
c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Token'], y=df['Inflow'], name='Inflow'))
    fig.add_trace(go.Bar(x=df['Token'], y=df['Outflow'], name='Outflow'))
    fig.update_layout(title_text='Volume of Inflow and Outflow of Each Token', yaxis_title='Volume [USD]')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.bar(df, x='Token', y='Netflow', color='Token', title='Liquidity of Each Token')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

df = burrow_overview
c1, c2, c3 = st.columns(3)
with c1:
    fig = px.bar(df, x='Token', y='Volume', color='Action', title='Total Volume')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.bar(df, x='Token', y='Transactions', color='Action', title='Total Transactions')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c3:
    fig = px.bar(df, x='Token', y='Users', color='Action', title='Total Users')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', xaxis={'categoryorder':'total ascending'})
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Activity Over Time')

interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='burrow_interval', horizontal=True)

if st.session_state.burrow_interval == 'Daily':
    actions_over_time = burrow_daily.groupby(['Date', 'Action']).agg('sum').reset_index()
    burrow_liquidity_over_time = burrow_liquidity_daily
elif st.session_state.burrow_interval == 'Weekly':
    actions_over_time = burrow_daily
    actions_over_time = actions_over_time.groupby([pd.Grouper(freq='W', key='Date'), 'Action']).agg('sum').reset_index()
    burrow_liquidity_over_time = burrow_liquidity_daily
    burrow_liquidity_over_time = burrow_liquidity_over_time.groupby([pd.Grouper(freq='W', key='Date'), 'Token']).agg('sum').reset_index()
elif st.session_state.burrow_interval == 'Monthly':
    actions_over_time = burrow_daily
    actions_over_time = actions_over_time.groupby([pd.Grouper(freq='MS', key='Date'), 'Action']).agg('sum').reset_index()
    burrow_liquidity_over_time = burrow_liquidity_daily
    burrow_liquidity_over_time = burrow_liquidity_over_time.groupby([pd.Grouper(freq='M', key='Date'), 'Token']).agg('sum').reset_index()

fig = px.line(burrow_liquidity_over_time, x='Date', y='Netflow', color='Token', custom_data=['Token'], title='Liquidity of Each Token Over Time')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(actions_over_time, x='Date', y='Volume', color='Action', custom_data=['Action'], title='Volume of Each Action Over Time')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(actions_over_time, x='Date', y='Transactions', color='Action', custom_data=['Action'], title='Transactions of Each Action Over Time')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(actions_over_time, x='Date', y='Users', color='Action', custom_data=['Action'], title='Users of Each Action Over Time')
fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)