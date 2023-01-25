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
st.set_page_config(page_title='Transfers - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('💸 Transfers')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
@st.cache(ttl=1000, allow_output_mutation=True)
def get_data(query):
    if query == 'Transfers Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/748dc207-2309-4afb-8b09-9e979aa6007f/data/latest')
    elif query == 'Transfers Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/e4353f8e-2e61-486e-8d7f-d5bf05d9bfed/data/latest')
    elif query == 'Transfers Heatmap':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9135ad92-3e0c-4c07-9af8-905f204533eb/data/latest')
    elif query == 'Transfers Distribution':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/a17c8548-2834-4600-bc78-a0efb6d12de4/data/latest')
    elif query == 'Transfers Assets Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/c14f77c5-76be-4fc1-8e50-595462b36f64/data/latest')
    elif query == 'Transfers Assets Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/c1e767c2-3601-43e4-b159-f5fb8efbedfb/data/latest')
    return None

transfers_overview = get_data('Transfers Overview')
transfers_daily = get_data('Transfers Daily')
transfers_heatmap = get_data('Transfers Heatmap')
transfers_distribution = get_data('Transfers Distribution')
transfers_assets_overview = get_data('Transfers Assets Overview')
transfers_assets_daily = get_data('Transfers Assets Daily')

# Content
tab_overview, tab_heatmap, tab_assets = st.tabs(['**Overview**', '**Heatmap**', '**Assets**'])

with tab_overview:

    st.subheader('Overview')

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Total Transferred Volume**', value=str(transfers_overview['Volume'].map('{:,.0f}'.format).values[0]), help='USD')
        st.metric(label='**Average Daily Transferred Volume**', value=str(transfers_overview['Volume/Day'].map('{:,.0f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Total Transfers**', value=str(transfers_overview['Transfers'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Transfers**', value=str(transfers_overview['Transfers/Day'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Total Transferring Users**', value=str(transfers_overview['Users'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Transferring Users**', value=str(transfers_overview['Users/Day'].map('{:,.0f}'.format).values[0]))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Average Transferred Amount**', value=str(transfers_overview['AmountAverage'].map('{:,.2f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Median Transferred Amount**', value=str(transfers_overview['AmountMedian'].map('{:,.2f}'.format).values[0]), help='USD')
    with c3:
        st.metric(label='**Average Volume/User**', value=str(transfers_overview['Volume/User'].map('{:,.0f}'.format).values[0]), help='USD')
    with c4:
        st.metric(label='**Average Transfers/User**', value=str(transfers_overview['Transfers/User'].map('{:,.0f}'.format).values[0]))

    st.subheader('Transferred Amount Distribution')

    df = transfers_distribution
    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.pie(df, values='Volume', names='Bucket', title='Share of Total Transferred Volume')
        fig.update_layout(legend_title='USD Amount', legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Transfers', names='Bucket', title='Share of Total Transfers')
        fig.update_layout(legend_title='USD Amount', legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(df, values='Users', names='Bucket', title='Share of Total Transferring Users')
        fig.update_layout(legend_title='USD Amount', legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(df, x='Bucket', y='AmountAverage', color='Bucket', title='Average Transferred Amount', histfunc='avg', log_y=True)
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Average [USD]', xaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.histogram(df, x='Bucket', y='AmountMedian', color='Bucket',  title='Median Transferred Amount', histfunc='avg', log_y=True)
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Median [USD]', xaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='transfers_interval', horizontal=True)

    if st.session_state.transfers_interval == 'Daily':
        transfers_over_time = transfers_daily
    elif st.session_state.transfers_interval == 'Weekly':
        transfers_over_time = transfers_daily
        transfers_over_time = transfers_daily.groupby([pd.Grouper(freq='W', key='Date')]).agg(
            {'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum', 'AmountAverage': 'mean',
                'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
    elif st.session_state.transfers_interval == 'Monthly':
        transfers_over_time = transfers_daily
        transfers_over_time = transfers_daily.groupby([pd.Grouper(freq='MS', key='Date')]).agg(
            {'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum', 'AmountAverage': 'mean',
                'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()

    fig = px.area(x=transfers_over_time['Date'], y=transfers_over_time['Volume'].round(), title='Transferred Volume Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=transfers_over_time['Date'], y=transfers_over_time['Transfers'], name='Transfers'), secondary_y=False)
    fig.add_trace(go.Line(x=transfers_over_time['Date'], y=transfers_over_time['Users'], name='Users'), secondary_y=True)
    fig.update_layout(title_text='Number of Transfers and Transferring Users Over Time')
    fig.update_yaxes(title_text='Transfers', secondary_y=False)
    fig.update_yaxes(title_text='Users', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=transfers_over_time['Date'], y=transfers_over_time['AmountAverage'].round(2), name='Average'), secondary_y=False)
    fig.add_trace(go.Line(x=transfers_over_time['Date'], y=transfers_over_time['AmountMedian'].round(2), name='Median'), secondary_y=True)
    fig.update_layout(title_text='Average and Median Transferred Amount Over Time')
    fig.update_yaxes(title_text='Average [USD]', secondary_y=False)
    fig.update_yaxes(title_text='Median [USD]', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=transfers_over_time['Date'], y=transfers_over_time['Volume/User'].round(2), name='Volume/User'), secondary_y=False)
    fig.add_trace(go.Line(x=transfers_over_time['Date'], y=transfers_over_time['Transfers/User'].round(2), name='Transfers/User'), secondary_y=True)
    fig.update_layout(title_text='Average Transferred Volume and Transfers per User Over Time')
    fig.update_yaxes(title_text='Volume/User [USD]', secondary_y=False)
    fig.update_yaxes(title_text='Transfers/User', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_heatmap:

    st.subheader('Activity Heatmap')

    fig = px.density_heatmap(transfers_heatmap, x='Hour', y='Day', z='Volume', histfunc='avg', title='Heatmap of Transferred Volume', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Volume [USD]'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.density_heatmap(transfers_heatmap, x='Hour', y='Day', z='Transfers', histfunc='avg', title='Heatmap of Transfers', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Transfers'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.density_heatmap(transfers_heatmap, x='Hour', y='Day', z='Users', histfunc='avg', title='Heatmap of Transferring Users', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Users'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Heatmap of Transferred Amount')

    fig = px.density_heatmap(transfers_heatmap, x='Hour', y='Day', z='AmountAverage', histfunc='avg', title='Heatmap of Average Transferred Amount', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Average [USD]'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.density_heatmap(transfers_heatmap, x='Hour', y='Day', z='AmountMedian', histfunc='avg', title='Heatmap of Median Transferred Amount', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Median [USD]'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_assets:

    st.subheader('Market Shares')
    
    c1, c2, c3 = st.columns(3)
    with c1:
        df = transfers_assets_overview.sort_values('Volume', ascending=False).reset_index(drop=True)
        df.loc[transfers_assets_overview.index >= 7, 'Asset'] = 'Other'
        fig = px.pie(df, values='Volume', names='Asset', title='Share of Total Transferred Volume', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = transfers_assets_overview.sort_values('Transfers', ascending=False).reset_index(drop=True)
        df.loc[transfers_assets_overview.index >= 7, 'Asset'] = 'Other'
        fig = px.pie(df, values='Transfers', names='Asset', title='Share of Total Transfers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = transfers_assets_overview.sort_values('Users', ascending=False).reset_index(drop=True)
        df.loc[transfers_assets_overview.index >= 7, 'Asset'] = 'Other'
        fig = px.pie(df, values='Users', names='Asset', title='Share of Total Transferring Users', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Averages')

    c1, c2 = st.columns(2)
    with c1:
        df = transfers_assets_overview.sort_values('AmountAverage', ascending=False).reset_index(drop=True)
        df.loc[transfers_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='AmountAverage', color='Asset', title='Average Transferred Amount')
        fig.update_layout(showlegend=False, yaxis_title='Average Amount [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        df = transfers_assets_overview.sort_values('Volume/User', ascending=False).reset_index(drop=True)
        df.loc[transfers_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='Volume/User', color='Asset', title='Average Transferred Volume/User')
        fig.update_layout(showlegend=False, yaxis_title='Volume/User [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = transfers_assets_overview.sort_values('AmountMedian', ascending=False).reset_index(drop=True)
        df.loc[transfers_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='AmountMedian', color='Asset', title='Median Transferred Amount')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Median Amount [USD]', xaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        df = transfers_assets_overview.sort_values('Transfers/User', ascending=False).reset_index(drop=True)
        df.loc[transfers_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='Transfers/User', color='Asset', title='Average Transfers/User')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Transfers/User', xaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')
    
    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='assets_interval', horizontal=True)

    if st.session_state.assets_interval == 'Daily':
        df = transfers_assets_daily
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Asset'] = 'Other'
        df = df.groupby(['Date', 'Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
    elif st.session_state.assets_interval == 'Weekly':
        df = transfers_assets_daily
        df = df.groupby([pd.Grouper(freq='W', key='Date'), 'Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Asset'] = 'Other'
        df = df.groupby(['Date', 'Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
    elif st.session_state.assets_interval == 'Monthly':
        df = transfers_assets_daily
        df = df.groupby([pd.Grouper(freq='MS', key='Date'), 'Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Asset'] = 'Other'
        df = df.groupby(['Date', 'Asset']).agg({'Transfers': 'sum', 'Users': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Transfers/User': 'mean', 'Volume/User': 'mean'}).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='Asset', custom_data=['Asset'], title='Transferred Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Transfers'], ascending=[True, False]), x='Date', y='Transfers', color='Asset', custom_data=['Asset'], title='Transfers Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transfers', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Users'], ascending=[True, False]), x='Date', y='Users', color='Asset', custom_data=['Asset'], title='Transferring Users Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'AmountAverage'], ascending=[True, False]), x='Date', y='AmountAverage', color='Asset', custom_data=['Asset'], title='Average Transferred Amount Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average Amount [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Volume/User'], ascending=[True, False]), x='Date', y='Volume/User', color='Asset', custom_data=['Asset'], title='Average Transferred Volume per User Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume/User [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = go.Figure()
        for i in df['Asset'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Asset == @i")['Date'],
                y=df.query("Asset == @i")['Volume'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Transferred Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Asset'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Asset == @i")['Date'],
                y=df.query("Asset == @i")['Transfers'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Transfers Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Asset'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Asset == @i")['Date'],
                y=df.query("Asset == @i")['Users'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Transferring Users Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'AmountMedian'], ascending=[True, False]), x='Date', y='AmountMedian', color='Asset', custom_data=['Asset'], title='Median Transferred Amount Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median Amount [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Transfers/User'], ascending=[True, False]), x='Date', y='Transfers/User', color='Asset', custom_data=['Asset'], title='Average Transfers per User Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transfers/User', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)