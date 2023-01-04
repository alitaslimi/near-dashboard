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
st.set_page_config(page_title='Bridges - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('🌈 Bridges')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
@st.cache(ttl=3600)
def get_data(query):
    if query == 'Bridges Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/4e31e12c-bf4e-40c7-b81b-68927d9d537a/data/latest')
    elif query == 'Bridges Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/fea096a4-db6d-48ec-abab-28966966137f/data/latest')
    elif query == 'Bridges Tokens Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/137df1be-0ba5-4cdb-9764-bb6935f73e27/data/latest')
    elif query == 'Bridges Tokens Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/85db43ba-7b4a-40c8-a805-2759be0b4623/data/latest')
    return None

bridges_overview = get_data('Bridges Overview')
bridges_daily = get_data('Bridges Daily')
bridges_tokens_overview = get_data('Bridges Tokens Overview')
bridges_tokens_daily = get_data('Bridges Tokens Daily')

# Content
tab_overview, tab_tokens = st.tabs(['**Overview**', '**Tokens**'])

with tab_overview:

    st.subheader('Overview of Rainbow Bridge')

    df = bridges_overview.sum().reset_index()
    print(df)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Total Bridged Volume**', value=str(df.loc[df['index'] == 'Volume', 0].map('{:,.0f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Total Bridge Transactions**', value=str(df.loc[df['index'] == 'Transactions', 0].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Total Bridgers**', value=str(df.loc[df['index'] == 'Bridgers', 0].map('{:,.0f}'.format).values[0]))

    st.subheader('Market Shares')

    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.pie(bridges_overview, values='Volume', names='Bridge', title='Share of Total Bridged Volume', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(bridges_overview, values='Transactions', names='Bridge', title='Share of Total Transactions', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(bridges_overview, values='Bridgers', names='Bridge', title='Share of Total Bridgers', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='bridges_interval', horizontal=True)

    if st.session_state.bridges_interval == 'Daily':
        bridges_over_time = bridges_daily
    elif st.session_state.bridges_interval == 'Weekly':
        bridges_over_time = bridges_daily
        bridges_over_time = bridges_over_time.groupby([pd.Grouper(freq='W', key='Date'), 'Bridge']).agg('sum').reset_index()
    elif st.session_state.bridges_interval == 'Monthly':
        bridges_over_time = bridges_daily
        bridges_over_time = bridges_over_time.groupby([pd.Grouper(freq='M', key='Date'), 'Bridge']).agg('sum').reset_index()

    fig = px.line(bridges_over_time, x='Date', y='Volume', color='Bridge', custom_data=['Bridge'], title='Bridged Volume Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.line(bridges_over_time, x='Date', y='Transactions', color='Bridge', custom_data=['Bridge'], title='Bridge Transactions Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.line(bridges_over_time, x='Date', y='Bridgers', color='Bridge', custom_data=['Bridge'], title='Bridgers Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Bridgers', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_tokens:

    st.subheader('Market Shares')

    c1, c2, c3 = st.columns(3)
    with c1:
        df = bridges_tokens_overview.sort_values('Volume', ascending=False).reset_index(drop=True)
        df.loc[bridges_tokens_overview.index >= 10, 'Token'] = 'Other'
        fig = px.pie(df, values='Volume', names='Token', title='Share of Total Bridged Volume', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = bridges_tokens_overview.sort_values('Transactions', ascending=False).reset_index(drop=True)
        df.loc[bridges_tokens_overview.index >= 10, 'Token'] = 'Other'
        fig = px.pie(df, values='Transactions', names='Token', title='Share of Total Transactions', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = bridges_tokens_overview.sort_values('Bridgers', ascending=False).reset_index(drop=True)
        df.loc[bridges_tokens_overview.index >= 10, 'Token'] = 'Other'
        fig = px.pie(df, values='Bridgers', names='Token', title='Share of Total Bridgers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='tokens_interval', horizontal=True)

    if st.session_state.tokens_interval == 'Daily':
        df = bridges_tokens_daily
        df = df.groupby(['Date', 'Token']).agg('sum').reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Token'] = 'Other'
        df = df.groupby(['Date', 'Token']).agg('sum').reset_index()
    elif st.session_state.tokens_interval == 'Weekly':
        df = bridges_tokens_daily
        df = df.groupby([pd.Grouper(freq='W', key='Date'), 'Token']).agg('sum').reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Token'] = 'Other'
        df = df.groupby(['Date', 'Token']).agg('sum').reset_index()
    elif st.session_state.tokens_interval == 'Monthly':
        df = bridges_tokens_daily
        df = df.groupby([pd.Grouper(freq='M', key='Date'), 'Token']).agg('sum').reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Token'] = 'Other'
        df = df.groupby(['Date', 'Token']).agg('sum').reset_index()

    fig = px.bar(df, x='Date', y='Volume', color='Token', custom_data=['Token'], title='Bridged Volume Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.bar(df, x='Date', y='Transactions', color='Token', custom_data=['Token'], title='Bridge Transactions Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.bar(df, x='Date', y='Bridgers', color='Token', custom_data=['Token'], title='Bridgers Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Bridgers', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
