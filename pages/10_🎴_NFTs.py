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
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Page Favicon
favicon = PIL.Image.open('favicon.png')

# Layout
st.set_page_config(page_title='NFTs - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('🎴 NFTs')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
nfts_overview = data.get_data('NFTs Overview')
nfts_daily = data.get_data('NFTs Daily')
nfts_heatmap = data.get_data('NFTs Heatmap')
nfts_marketplaces_overview = data.get_data('NFTs Marketplaces Overview')
nfts_marketplaces_daily = data.get_data('NFTs Marketplaces Daily')
nfts_collections_overview = data.get_data('NFTs Collections Overview')
nfts_collections_daily = data.get_data('NFTs Collections Daily')

# Content
tab_overview, tab_heatmap, tab_marketplaces, tab_collections = st.tabs(['**Overview**', '**Heatmap**', '**Marketplaces**', '**Collections**'])

with tab_overview:

    st.subheader('Overview')
    
    df = nfts_overview
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Total Sales Volume**', value=str(df['Volume'].map('{:,.0f}'.format).values[0]), help='USD')
        st.metric(label='**Total Traded NFTs**', value=str(df['NFTs'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average NFT Price**', value=str(df['PriceAverage'].map('{:,.2f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Total Sales**', value=str(df['Sales'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Total Traded Collections**', value=str(df['Collections'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Median NFT Price**', value=str(df['PriceMedian'].map('{:,.2f}'.format).values[0]), help='USD')
    with c3:
        st.metric(label='**Total Unique Buyers**', value=str(df['Buyers'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Marketplaces**', value=str(df['Marketplaces'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Highest NFT Price**', value=str(df['PriceMax'].map('{:,.0f}'.format).values[0]), help='USD')
    
    st.subheader('Averages')
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Average Daily Volume**', value=str(df['Volume/Day'].map('{:,.0f}'.format).values[0]), help='USD')
        st.metric(label='**Average Daily Traded NFTs**', value=str(df['NFTs/Day'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Volume/Collection**', value=str(df['Volume/Collection'].map('{:,.0f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Average Volume/Buyer**', value=str(df['Volume/Buyer'].map('{:,.0f}'.format).values[0]), help='USD')
        st.metric(label='**Average NFTs/Buyer**', value=str(df['NFTs/Buyer'].map('{:,.2f}'.format).values[0]))
        st.metric(label='**Average NFTs/Collection**', value=str(df['NFTs/Collection'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Average Daily Sales**', value=str(df['Sales/Day'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Traded Collections**', value=str(df['Collections/Day'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average NFTs/Sale**', value=str(df['NFTs/Sale'].map('{:,.2f}'.format).values[0]), help='USD')
    with c4:
        st.metric(label='**Average Sales/Buyer**', value=str(df['Sales/Buyer'].map('{:,.2f}'.format).values[0]))
        st.metric(label='**Average Collections/Buyer**', value=str(df['Collections/Buyer'].map('{:,.2f}'.format).values[0]))
        st.metric(label='**Average Daily Buyers**', value=str(df['Buyers/Day'].map('{:,.0f}'.format).values[0]))

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='nfts_interval', horizontal=True)

    if st.session_state.nfts_interval == 'Daily':
        df = nfts_daily
    elif st.session_state.nfts_interval == 'Weekly':
        df = nfts_daily
        df = nfts_daily.groupby([pd.Grouper(freq='W', key='Date')]).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum', 'Collections': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
    elif st.session_state.nfts_interval == 'Monthly':
        df = nfts_daily
        df = nfts_daily.groupby([pd.Grouper(freq='MS', key='Date')]).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'Volume': 'sum', 'NFTs': 'sum', 'Collections': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()

    fig = px.area(df, x='Date', y='Volume', title='Daily Sales Volume')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=df['Date'], y=df['Sales'], name='Sales'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['Buyers'], name='Buyers'), secondary_y=True)
    fig.update_layout(title_text='Daily Sales and Buyers')
    fig.update_yaxes(title_text='Sales', secondary_y=False)
    fig.update_yaxes(title_text='Buyers', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=df['Date'], y=df['NFTs'], name='NFTs'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['Collections'], name='Collections'), secondary_y=True)
    fig.update_layout(title_text='Daily Traded NFTs and Collections')
    fig.update_yaxes(title_text='NFTs', secondary_y=False)
    fig.update_yaxes(title_text='Collections', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=df['Date'], y=df['PriceAverage'].round(2), name='Average'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['PriceMedian'].round(2), name='Median'), secondary_y=True)
    fig.update_layout(title_text='Daily Average and Median NFT Prices')
    fig.update_yaxes(title_text='Average [USD]', secondary_y=False)
    fig.update_yaxes(title_text='Median [USD]', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_heatmap:

    st.subheader('Activity Heatmap')

    df = nfts_heatmap
    c1, c2 = st.columns(2)
    with c1:
        fig = px.density_heatmap(df, x='Hour', y='Day', z='Volume', histfunc='avg', title='Heatmap of Sales Volume', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Volume [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='PriceAverage', histfunc='avg', title='Heatmap of Average NFT Price', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Average [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='PriceMedian', histfunc='avg', title='Heatmap of Median NFT Price', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Median [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='PriceMax', histfunc='avg', title='Heatmap of Max NFT Price', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Max Price [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.density_heatmap(df, x='Hour', y='Day', z='Sales', histfunc='avg', title='Heatmap of Sales', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Sales'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='Buyers', histfunc='avg', title='Heatmap of Unique Buyers', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Buyers'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='NFTs', histfunc='avg', title='Heatmap of Traded NFTs', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='NFTs'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='Collections', histfunc='avg', title='Heatmap of Traded Collections', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Collections'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_marketplaces:
    
    st.subheader('Market Shares')

    c1, c2 = st.columns(2)
    with c1:
        df = nfts_marketplaces_overview.sort_values('Volume', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 7, 'Marketplace'] = 'Other'
        fig = px.pie(df, values='Volume', names='Marketplace', title='Share of Total Sales Volume', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = nfts_marketplaces_overview.sort_values('Sales', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 7, 'Marketplace'] = 'Other'
        fig = px.pie(df, values='Sales', names='Marketplace', title='Share of Total Sales', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2, c3 = st.columns(3)
    with c1:
        df = nfts_marketplaces_overview.sort_values('Buyers', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 7, 'Marketplace'] = 'Other'
        fig = px.pie(df, values='Buyers', names='Marketplace', title='Share of Total Buyers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = nfts_marketplaces_overview.sort_values('NFTs', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 7, 'Marketplace'] = 'Other'
        fig = px.pie(df, values='NFTs', names='Marketplace', title='Share of Total Traded NFTs', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = nfts_marketplaces_overview.sort_values('Collections', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 7, 'Marketplace'] = 'Other'
        fig = px.pie(df, values='Collections', names='Marketplace', title='Share of Total Traded Collections', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Prices')

    c1, c2 = st.columns(2)
    with c1:
        df = nfts_marketplaces_overview.sort_values('PriceAverage', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 10, 'Marketplace'] = 'Other'
        df = df.groupby(['Marketplace']).agg({'PriceAverage': 'mean'}).reset_index()
        fig = px.bar(df, x='Marketplace', y='PriceAverage', color='Marketplace', title='Average NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title='Average Price [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = nfts_marketplaces_overview.sort_values('PriceMax', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 10, 'Marketplace'] = 'Other'
        df = df.groupby(['Marketplace']).agg({'PriceMax': 'mean'}).reset_index()
        fig = px.bar(df, x='Marketplace', y='PriceMax', color='Marketplace', title='Maximum NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title='Maximum Price [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = nfts_marketplaces_overview.sort_values('PriceMedian', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 10, 'Marketplace'] = 'Other'
        df = df.groupby(['Marketplace']).agg({'PriceMedian': 'mean'}).reset_index()
        fig = px.bar(df, x='Marketplace', y='PriceMedian', color='Marketplace', title='Median NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title='Median Price [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = nfts_marketplaces_overview.sort_values('PriceFloor', ascending=False).reset_index(drop=True)
        df.loc[nfts_marketplaces_overview.index >= 10, 'Marketplace'] = 'Other'
        df = df.groupby(['Marketplace']).agg({'PriceFloor': 'mean'}).reset_index()
        fig = px.bar(df, x='Marketplace', y='PriceFloor', color='Marketplace', title='Floor NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title='Floor Price [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='marketplaces_interval', horizontal=True)

    if st.session_state.marketplaces_interval == 'Daily':
        df = nfts_marketplaces_daily
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Marketplace'] = 'Other'
        df = df.groupby(['Date', 'Marketplace']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Collections': 'sum', 'Volume': 'sum',
            'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
    elif st.session_state.marketplaces_interval == 'Weekly':
        df = nfts_marketplaces_daily
        df = df.groupby([pd.Grouper(freq='W', key='Date'), 'Marketplace']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Collections': 'sum', 'Volume': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Marketplace'] = 'Other'
        df = df.groupby(['Date', 'Marketplace']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Collections': 'sum', 'Volume': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
    elif st.session_state.marketplaces_interval == 'Monthly':
        df = nfts_marketplaces_daily
        df = df.groupby([pd.Grouper(freq='MS', key='Date'), 'Marketplace']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Collections': 'sum', 'Volume': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Marketplace'] = 'Other'
        df = df.groupby(['Date', 'Marketplace']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Collections': 'sum', 'Volume': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='Marketplace', custom_data=['Marketplace'], title='Sales Volume of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'Sales'], ascending=[True, False]), x='Date', y='Sales', color='Marketplace', custom_data=['Marketplace'], title='Sales of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'Buyers'], ascending=[True, False]), x='Date', y='Buyers', color='Marketplace', custom_data=['Marketplace'], title='Buyers of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Buyers', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'NFTs'], ascending=[True, False]), x='Date', y='NFTs', color='Marketplace', custom_data=['Marketplace'], title='Traded NFTs of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='NFTs', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'Collections'], ascending=[True, False]), x='Date', y='Collections', color='Marketplace', custom_data=['Marketplace'], title='Traded Collections of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Collections', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = go.Figure()
        for i in df['Marketplace'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Marketplace == @i")['Date'],
                y=df.query("Marketplace == @i")['Volume'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Sales Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Marketplace'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Marketplace == @i")['Date'],
                y=df.query("Marketplace == @i")['Sales'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Sales Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Marketplace'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Marketplace == @i")['Date'],
                y=df.query("Marketplace == @i")['Buyers'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Buyers Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Marketplace'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Marketplace == @i")['Date'],
                y=df.query("Marketplace == @i")['NFTs'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Traded NFTs Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Marketplace'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Marketplace == @i")['Date'],
                y=df.query("Marketplace == @i")['Collections'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Traded Collections Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Prices Over Time')

    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(df.sort_values(['Date', 'PriceAverage'], ascending=[True, False]), x='Date', y='PriceAverage', color='Marketplace', custom_data=['Marketplace'], title='Average NFT Prices of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average Price [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'PriceMax'], ascending=[True, False]), x='Date', y='PriceMax', color='Marketplace', custom_data=['Marketplace'], title='Maximum NFT Prices of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Maximum Price [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.line(df.sort_values(['Date', 'PriceMedian'], ascending=[True, False]), x='Date', y='PriceMedian', color='Marketplace', custom_data=['Marketplace'], title='Median NFT Prices of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median Price [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
        fig = px.line(df.sort_values(['Date', 'PriceFloor'], ascending=[True, False]), x='Date', y='PriceFloor', color='Marketplace', custom_data=['Marketplace'], title='Floor NFT Prices of Top Marketplaces by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Floor Price [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.4f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_collections:
    
    st.subheader('Market Shares')

    c1, c2 = st.columns(2)
    with c1:
        df = nfts_collections_overview.sort_values('Volume', ascending=False).reset_index(drop=True)
        df.loc[nfts_collections_overview.index >= 10, 'Collection'] = 'Other'
        fig = px.pie(df, values='Volume', names='Collection', title='Share of Total Sales Volume', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        df = nfts_collections_overview.sort_values('Buyers', ascending=False).reset_index(drop=True)
        df.loc[nfts_collections_overview.index >= 10, 'Collection'] = 'Other'
        fig = px.pie(df, values='Buyers', names='Collection', title='Share of Total Buyers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = nfts_collections_overview.sort_values('Sales', ascending=False).reset_index(drop=True)
        df.loc[nfts_collections_overview.index >= 10, 'Collection'] = 'Other'
        fig = px.pie(df, values='Sales', names='Collection', title='Share of Total Sales', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        df = nfts_collections_overview.sort_values('NFTs', ascending=False).reset_index(drop=True)
        df.loc[nfts_collections_overview.index >= 10, 'Collection'] = 'Other'
        fig = px.pie(df, values='NFTs', names='Collection', title='Share of Total Traded NFTs', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Prices')

    c1, c2 = st.columns(2)
    with c1:
        df = nfts_collections_overview.sort_values('PriceAverage', ascending=False).reset_index(drop=True)
        df.loc[nfts_collections_overview.index >= 10, 'Collection'] = 'Other'
        df = df.groupby(['Collection']).agg({'PriceAverage': 'mean'}).round(2).reset_index()
        fig = px.bar(df, x='Collection', y='PriceAverage', color='Collection', title='Average NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title='Average Price [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = nfts_collections_overview.sort_values('PriceMax', ascending=False).reset_index(drop=True)
        df.loc[nfts_collections_overview.index >= 10, 'Collection'] = 'Other'
        df = df.groupby(['Collection']).agg({'PriceMax': 'mean'}).round(2).reset_index()
        fig = px.bar(df, x='Collection', y='PriceMax', color='Collection', title='Maximum NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title='Maximum Price [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = nfts_collections_overview.sort_values('PriceMedian', ascending=False).reset_index(drop=True)
        df.loc[nfts_collections_overview.index >= 10, 'Collection'] = 'Other'
        df = df.groupby(['Collection']).agg({'PriceMedian': 'mean'}).round(2).reset_index()
        fig = px.bar(df, x='Collection', y='PriceMedian', color='Collection', title='Median NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title='Median Price [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = nfts_collections_overview.sort_values('PriceFloor', ascending=False).reset_index(drop=True)
        df.loc[nfts_collections_overview.index >= 10, 'Collection'] = 'Other'
        df = df.groupby(['Collection']).agg({'PriceFloor': 'mean'}).round(2).reset_index()
        fig = px.bar(df, x='Collection', y='PriceFloor', color='Collection', title='Floor NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title='Floor Price [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='collections_interval', horizontal=True)

    if st.session_state.collections_interval == 'Daily':
        df = nfts_collections_daily
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Collection'] = 'Other'
        df = df.groupby(['Date', 'Collection']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Volume': 'sum',
            'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
    elif st.session_state.collections_interval == 'Weekly':
        df = nfts_collections_daily
        df = df.groupby([pd.Grouper(freq='W', key='Date'), 'Collection']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Volume': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Collection'] = 'Other'
        df = df.groupby(['Date', 'Collection']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Volume': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
    elif st.session_state.collections_interval == 'Monthly':
        df = nfts_collections_daily
        df = df.groupby([pd.Grouper(freq='MS', key='Date'), 'Collection']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Volume': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Collection'] = 'Other'
        df = df.groupby(['Date', 'Collection']).agg(
            {'Sales': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Volume': 'sum',
                'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceFloor': 'mean'}).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='Collection', custom_data=['Collection'], title='Sales Volume of Top Collections by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'Sales'], ascending=[True, False]), x='Date', y='Sales', color='Collection', custom_data=['Collection'], title='Sales of Top Collections by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'Buyers'], ascending=[True, False]), x='Date', y='Buyers', color='Collection', custom_data=['Collection'], title='Buyers of Top Collections by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Buyers', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'NFTs'], ascending=[True, False]), x='Date', y='NFTs', color='Collection', custom_data=['Collection'], title='Traded NFTs of Top Collections by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='NFTs', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
    with c2:
        fig = go.Figure()
        for i in df['Collection'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Collection == @i")['Date'],
                y=df.query("Collection == @i")['Volume'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Sales Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Collection'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Collection == @i")['Date'],
                y=df.query("Collection == @i")['Sales'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Sales Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Collection'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Collection == @i")['Date'],
                y=df.query("Collection == @i")['Buyers'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Buyers Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Collection'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Collection == @i")['Date'],
                y=df.query("Collection == @i")['NFTs'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Traded NFTs Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Prices Over Time')

    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(df.sort_values(['Date', 'PriceAverage'], ascending=[True, False]), x='Date', y='PriceAverage', color='Collection', custom_data=['Collection'], title='Average NFT Prices of Top Collections by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average Price [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'PriceMax'], ascending=[True, False]), x='Date', y='PriceMax', color='Collection', custom_data=['Collection'], title='Maximum NFT Prices of Top Collections by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Maximum Price [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.line(df.sort_values(['Date', 'PriceMedian'], ascending=[True, False]), x='Date', y='PriceMedian', color='Collection', custom_data=['Collection'], title='Median NFT Prices of Top Collections by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median Price [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
        fig = px.line(df.sort_values(['Date', 'PriceFloor'], ascending=[True, False]), x='Date', y='PriceFloor', color='Collection', custom_data=['Collection'], title='Floor NFT Prices of Top Collections by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Floor Price [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.4f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)