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
st.set_page_config(page_title='Governance - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('🌍 Governance')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
@st.cache(ttl=1000, allow_output_mutation=True)
def get_data(query):
    if query == 'Blocks Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/024b2e03-1063-4bcf-a8de-b35d17e01cbd/data/latest')
    elif query == 'Blocks Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/1d55b381-77a7-4e03-b951-58421139cb09/data/latest')
    elif query == 'Validators Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/053529d5-6b21-41b9-9a62-32f12ea0532d/data/latest')
    elif query == 'Validators Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/fca955ff-ade0-4454-95ff-59c733ff846b/data/latest')
    elif query == 'Validators Actions Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/6a80300f-3a83-4be7-a701-9f3081535fba/data/latest')
    elif query == 'Validators Actions Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/711833dd-317c-4556-a789-36cdf6cd4b81/data/latest')
    elif query == 'Validators Staking Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/a07278ef-5126-4642-9694-fd374000d5b1/data/latest')
    elif query == 'Validators Staking Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/ac94cdae-9791-469e-bf6a-b3b84ca04704/data/latest')
    return None

blocks_overview = get_data('Blocks Overview')
blocks_daily = get_data('Blocks Daily')
validators_overview = get_data('Validators Overview')
validators_daily = get_data('Validators Daily')
validators_actions_overview = get_data('Validators Actions Overview')
validators_actions_daily = get_data('Validators Actions Daily')
validators_staking_overview = get_data('Validators Staking Overview')
validators_staking_daily = get_data('Validators Staking Daily')

# Content
tab_validators, tab_staking = st.tabs(['**Validators**', '**Staking**'])

with tab_validators:

    st.subheader('Overview')

    st.metric(label='**Total Unique Validators**', value=str(blocks_overview['Validators'].map('{:,.0f}'.format).values[0]))

    c1, c2= st.columns(2)
    with c1:
        df = validators_overview.sort_values('Blocks', ascending=False).reset_index(drop=True)
        df.loc[validators_overview.index >= 15, 'Validator'] = 'Other'
        fig = px.pie(df, values='Blocks', names='Validator', title='Share of Validated Blocks', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = validators_overview.sort_values('Transactions', ascending=False).reset_index(drop=True)
        df.loc[validators_overview.index >= 15, 'Validator'] = 'Other'
        fig = px.pie(df, values='Transactions', names='Validator', title='Share of Validated Transactions', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='validators_interval', horizontal=True)

    if st.session_state.validators_interval == 'Daily':
        blocks_over_time = blocks_daily
        df = validators_daily
        df['RowNumber'] = df.groupby('Date')['Blocks'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Validator'] = 'Other'
        df = df.groupby(['Date', 'Validator']).agg({'Blocks': 'sum', 'Transactions': 'sum'}).reset_index()
    elif st.session_state.validators_interval == 'Weekly':
        blocks_over_time = blocks_daily
        blocks_over_time = blocks_over_time.groupby([pd.Grouper(freq='W', key='Date')]).agg(
            {'Blocks': 'sum', 'Transactions': 'sum', 'Validators': 'sum', 'BlockTime': 'mean'}).reset_index()
        df = validators_daily
        df = df.groupby([pd.Grouper(freq='W', key='Date'), 'Validator']).agg({'Blocks': 'sum', 'Transactions': 'sum'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Blocks'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Validator'] = 'Other'
        df = df.groupby(['Date', 'Validator']).agg({'Blocks': 'sum', 'Transactions': 'sum'}).reset_index()
    elif st.session_state.validators_interval == 'Monthly':
        blocks_over_time = blocks_daily
        blocks_over_time = blocks_over_time.groupby([pd.Grouper(freq='MS', key='Date')]).agg(
            {'Blocks': 'sum', 'Transactions': 'sum', 'Validators': 'sum', 'BlockTime': 'mean'}).reset_index()
        df = validators_daily
        df = df.groupby([pd.Grouper(freq='MS', key='Date'), 'Validator']).agg({'Blocks': 'sum', 'Transactions': 'sum'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Blocks'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Validator'] = 'Other'
        df = df.groupby(['Date', 'Validator']).agg({'Blocks': 'sum', 'Transactions': 'sum'}).reset_index()

    fig = px.line(blocks_over_time, x='Date', y='Validators', title='Number of Block Validators Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Validators')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'Blocks'], ascending=[True, False]), x='Date', y='Blocks', color='Validator', custom_data=['Validator'], title='Validated Blocks of Top Validators Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Blocks', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Transactions'], ascending=[True, False]), x='Date', y='Transactions', color='Validator', custom_data=['Validator'], title='Validated Transactions of Top Validators Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = go.Figure()
        for i in df['Validator'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Validator == @i")['Date'],
                y=df.query("Validator == @i")['Blocks'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Validated Blocks of Top Validators Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Validator'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Validator == @i")['Date'],
                y=df.query("Validator == @i")['Transactions'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Validated Transactions of Top Validators Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_staking:

    st.subheader('Overview')
    df = validators_staking_overview.sort_values('Balance', ascending=False).reset_index(drop=True)
    df.loc[validators_staking_overview.index >= 10, 'Validator'] = 'Other'
    df = df.groupby(['Validator']).agg('sum').reset_index()
    c1, c2= st.columns(2)
    with c1:
        fig = px.bar(df, x='Validator', y='Balance', color='Validator', title='Total Balance of Top Validators')
        fig.update_layout(showlegend=False, yaxis_title='Balance [NEAR]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = sp.make_subplots()
        fig.add_trace(go.Bar(x=df['Validator'], y=df['VolumeStaked'], name='Staked'))
        fig.add_trace(go.Bar(x=df['Validator'], y=df['VolumeUnstaked'], name='Unstaked'))
        fig.update_layout(title_text='Volume of Staked and Unstaked NEAR', yaxis_title='Volume [NEAR]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Balance', names='Validator', title='Share of Total Balance of Top Validators', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = sp.make_subplots()
        fig.add_trace(go.Bar(x=df['Validator'], y=df['Stakers'], name='Stakers'))
        fig.add_trace(go.Bar(x=df['Validator'], y=df['Unstakers'], name='Unstakers'))
        fig.update_layout(title_text='Number of Stakers and Unstakers', yaxis_title='Addresses')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='staking_interval', horizontal=True)

    if st.session_state.staking_interval == 'Daily':
        df = validators_staking_daily
        df['RowNumber'] = df.groupby('Date')['Balance'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Validator'] = 'Other'
        df = df.groupby(['Date', 'Validator']).agg('sum').reset_index()
    elif st.session_state.staking_interval == 'Weekly':
        df = validators_staking_daily
        df = df.groupby([pd.Grouper(freq='W', key='Date'), 'Validator']).agg('sum').reset_index()
        df['RowNumber'] = df.groupby('Date')['Balance'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Validator'] = 'Other'
        df = df.groupby(['Date', 'Validator']).agg('sum').reset_index()
    elif st.session_state.staking_interval == 'Monthly':
        df = validators_staking_daily
        df = df.groupby([pd.Grouper(freq='M', key='Date'), 'Validator']).agg('sum').reset_index()
        df['RowNumber'] = df.groupby('Date')['Balance'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Validator'] = 'Other'
        df = df.groupby(['Date', 'Validator']).agg('sum').reset_index()
    
    fig = px.bar(df, x='Date', y='Balance', color='Validator', custom_data=['Validator'], title='Balance of Validators Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Balance [NEAR]', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'VolumeStaked'], ascending=[True, False]), x='Date', y='VolumeStaked', color='Validator', custom_data=['Validator'], title='VolumeStaked of Top Validators Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [NEAR]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Stakers'], ascending=[True, False]), x='Date', y='Stakers', color='Validator', custom_data=['Validator'], title='Stakers of Top Validators Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Addresses', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.bar(df.sort_values(['Date', 'VolumeUnstaked'], ascending=[True, False]), x='Date', y='VolumeUnstaked', color='Validator', custom_data=['Validator'], title='Untaked Volume of Top Validators Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [NEAR]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Unstakers'], ascending=[True, False]), x='Date', y='Unstakers', color='Validator', custom_data=['Validator'], title='Unstakers of Top Validators Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)