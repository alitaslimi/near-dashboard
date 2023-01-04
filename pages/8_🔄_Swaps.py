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
st.set_page_config(page_title='Swaps - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('🔄 Swaps')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

theme_plotly = None # None or streamlit

# Data Sources
@st.cache(ttl=3600)
def get_data(query):
    if query == 'Swaps Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/18f8dc36-dc82-45ce-8ffb-563ac0122407/data/latest')
    elif query == 'Swaps Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/c3237ea2-2027-4b28-b47c-00e0a62cba07/data/latest')
    elif query == 'Swaps Heatmap':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/b6561ad9-7ee3-4126-95f3-1c423df8b1a9/data/latest')
    elif query == 'Swaps DEXs Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/b3948af5-0d86-4609-b4c3-d45b8454ca8b/data/latest')
    elif query == 'Swaps DEXs Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/362dc974-4449-49ef-85e2-7e60b2170831/data/latest')
    elif query == 'Swaps Asset Types Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/f7f75d73-aea2-4616-9840-416de08e7fa6/data/latest')
    elif query == 'Swaps Asset Types Daily':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/a558f0f1-3d95-47ee-a58c-1132bb2d8034/data/latest')
    elif query == 'Swaps Assets Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/c8305309-2276-4a8d-8871-0cd66fc22203/data/latest')
    elif query == 'Swaps Assets Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/068e71ce-7767-437a-8ff3-45e94a354714/data/latest')
    return None

swaps_overview = get_data('Swaps Overview')
swaps_daily = get_data('Swaps Daily')
swaps_heatmap = get_data('Swaps Heatmap')
swaps_dexs_overview = get_data('Swaps DEXs Overview')
swaps_dexs_daily = get_data('Swaps DEXs Daily')
swaps_asset_types_overview = get_data('Swaps Asset Types Overview')
swaps_asset_types_daily = get_data('Swaps Asset Types Daily')
swaps_assets_overview = get_data('Swaps Assets Overview')
swaps_assets_daily = get_data('Swaps Assets Daily')

# Content
tab_overview, tab_heatmap, tab_dexs, tab_asset_types, tab_assets = st.tabs(['**Overview**', '**Heatmap**', '**DEXs**', '**Asset Types**', '**Assets**'])

with tab_overview:

    st.subheader('Overview')

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Total Swapped Volume**', value=str(swaps_overview['Volume'].map('{:,.0f}'.format).values[0]), help='USD')
        st.metric(label='**Average Daily Swapped Volume**', value=str(swaps_overview['Volume/Day'].map('{:,.0f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Total Swaps**', value=str(swaps_overview['Swaps'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Swaps**', value=str(swaps_overview['Swaps/Day'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Total Swappers**', value=str(swaps_overview['Swappers'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Swappers**', value=str(swaps_overview['Swappers/Day'].map('{:,.0f}'.format).values[0]))
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Average Swapped Amount**', value=str(swaps_overview['AmountAverage'].map('{:,.2f}'.format).values[0]), help='USD')
    with c2:
        st.metric(label='**Median Swapped Amount**', value=str(swaps_overview['AmountMedian'].map('{:,.2f}'.format).values[0]), help='USD')
    with c3:
        st.metric(label='**Average Volume/Swapper**', value=str(swaps_overview['Volume/Swapper'].map('{:,.0f}'.format).values[0]), help='USD')
    with c4:
        st.metric(label='**Average Swaps/Swapper**', value=str(swaps_overview['Swaps/Swapper'].map('{:,.0f}'.format).values[0]))

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='swaps_interval', horizontal=True)

    if st.session_state.swaps_interval == 'Daily':
        swaps_over_time = swaps_daily
    elif st.session_state.swaps_interval == 'Weekly':
        swaps_over_time = swaps_daily
        swaps_over_time = swaps_daily.groupby([pd.Grouper(freq='W', key='Date')]).agg(
            {'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum', 'AmountAverage': 'mean',
                'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
    elif st.session_state.swaps_interval == 'Monthly':
        swaps_over_time = swaps_daily
        swaps_over_time = swaps_daily.groupby([pd.Grouper(freq='M', key='Date')]).agg(
            {'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum', 'AmountAverage': 'mean',
                'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()

    fig = px.area(swaps_over_time, x='Date', y='Volume', title='Swapped Volume Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=swaps_over_time['Date'], y=swaps_over_time['Swaps'], name='Swaps'), secondary_y=False)
    fig.add_trace(go.Line(x=swaps_over_time['Date'], y=swaps_over_time['Swappers'], name='Swappers'), secondary_y=True)
    fig.update_layout(title_text='Number of Swaps and Swappers Over Time')
    fig.update_yaxes(title_text='Swaps', secondary_y=False)
    fig.update_yaxes(title_text='Swappers', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=swaps_over_time['Date'], y=swaps_over_time['AmountAverage'].round(2), name='Average'), secondary_y=False)
    fig.add_trace(go.Line(x=swaps_over_time['Date'], y=swaps_over_time['AmountMedian'].round(2), name='Median'), secondary_y=True)
    fig.update_layout(title_text='Average and Median Swapped Amount Over Time')
    fig.update_yaxes(title_text='Average [USD]', secondary_y=False)
    fig.update_yaxes(title_text='Median [USD]', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=swaps_over_time['Date'], y=swaps_over_time['Volume/Swapper'].round(2), name='Volume/Swapper'), secondary_y=False)
    fig.add_trace(go.Line(x=swaps_over_time['Date'], y=swaps_over_time['Swaps/Swapper'].round(2), name='Swaps/Swapper'), secondary_y=True)
    fig.update_layout(title_text='Average Swapped Volume and Swaps per Swapper Over Time')
    fig.update_yaxes(title_text='Volume/Swapper [USD]', secondary_y=False)
    fig.update_yaxes(title_text='Swaps/Swapper', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_heatmap:

    st.subheader('Activity Heatmap')

    fig = px.density_heatmap(swaps_heatmap, x='Hour', y='Day', z='Volume', histfunc='avg', title='Heatmap of Swapped Volume', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Volume [USD]'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.density_heatmap(swaps_heatmap, x='Hour', y='Day', z='Swaps', histfunc='avg', title='Heatmap of Swaps', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Swaps'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.density_heatmap(swaps_heatmap, x='Hour', y='Day', z='Swappers', histfunc='avg', title='Heatmap of Swappers', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Swappers'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Heatmap of Swapped Amount')

    fig = px.density_heatmap(swaps_heatmap, x='Hour', y='Day', z='AmountAverage', histfunc='avg', title='Heatmap of Average Swapped Amount', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Average [USD]'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.density_heatmap(swaps_heatmap, x='Hour', y='Day', z='AmountMedian', histfunc='avg', title='Heatmap of Median Swapped Amount', nbinsx=24)
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 1}, coloraxis_colorbar=dict(title='Median [USD]'))
    fig.update_yaxes(categoryorder='array', categoryarray=week_days)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_dexs:

    st.subheader('Market Shares')

    c1, c2, c3 = st.columns(3)
    with c1:
        df = swaps_dexs_overview.sort_values('Volume', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 5, 'DEX'] = 'Other'
        fig = px.pie(df, values='Volume', names='DEX', title='Share of Total Swapped Volume', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = swaps_dexs_overview.sort_values('Swaps', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 5, 'DEX'] = 'Other'
        fig = px.pie(df, values='Swaps', names='DEX', title='Share of Total Swaps', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = swaps_dexs_overview.sort_values('Swappers', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 5, 'DEX'] = 'Other'
        fig = px.pie(df, values='Swappers', names='DEX', title='Share of Total Swappers', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Averages')

    c1, c2, c3 = st.columns(3)
    with c1:
        df = swaps_dexs_overview.sort_values('Volume/Day', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 10, 'DEX'] = 'Other'
        df = df.groupby(['DEX']).agg({'Volume/Day': 'mean'}).reset_index()
        fig = px.bar(df, x='DEX', y='Volume/Day', color='DEX', title='Average Daily Swapped Volume')
        fig.update_layout(showlegend=False, yaxis_title='Volume/Day [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = swaps_dexs_overview.sort_values('Swaps/Day', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 10, 'DEX'] = 'Other'
        df = df.groupby(['DEX']).agg({'Swaps/Day': 'mean'}).reset_index()
        fig = px.bar(df, x='DEX', y='Swaps/Day', color='DEX', title='Average Daily Swaps')
        fig.update_layout(showlegend=False, yaxis_title='Swaps/Day')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = swaps_dexs_overview.sort_values('Swappers/Day', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 10, 'DEX'] = 'Other'
        df = df.groupby(['DEX']).agg({'Swappers/Day': 'mean'}).reset_index()
        fig = px.bar(df, x='DEX', y='Swappers/Day', color='DEX', title='Average Daily Swappers')
        fig.update_layout(showlegend=False, yaxis_title='Swappers/Day')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns(2)
    with c1:
        df = swaps_dexs_overview.sort_values('AmountAverage', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 10, 'DEX'] = 'Other'
        df = df.groupby(['DEX']).agg({'AmountAverage': 'mean'}).reset_index()
        fig = px.bar(df, x='DEX', y='AmountAverage', color='DEX', title='Average Swapped Amount')
        fig.update_layout(showlegend=False, yaxis_title='Average Amount [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = swaps_dexs_overview.sort_values('Volume/Swapper', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 10, 'DEX'] = 'Other'
        df = df.groupby(['DEX']).agg({'Volume/Swapper': 'mean'}).reset_index()
        fig = px.bar(df, x='DEX', y='Volume/Swapper', color='DEX', title='Average Swapped Volume/Swapper')
        fig.update_layout(showlegend=False, yaxis_title='Volume/Swapper [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = swaps_dexs_overview.sort_values('AmountMedian', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 10, 'DEX'] = 'Other'
        df = df.groupby(['DEX']).agg({'AmountMedian': 'mean'}).reset_index()
        fig = px.bar(df, x='DEX', y='AmountMedian', color='DEX', title='Median Swapped Amount')
        fig.update_layout(showlegend=False, yaxis_title='Median Amount [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = swaps_dexs_overview.sort_values('Swaps/Swapper', ascending=False).reset_index(drop=True)
        df.loc[swaps_dexs_overview.index >= 10, 'DEX'] = 'Other'
        df = df.groupby(['DEX']).agg({'Swaps/Swapper': 'mean'}).reset_index()
        fig = px.bar(df, x='DEX', y='Swaps/Swapper', color='DEX', title='Average Swaps/Swapper')
        fig.update_layout(showlegend=False, yaxis_title='Swaps/Swapper')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='dexs_interval', horizontal=True)

    if st.session_state.dexs_interval == 'Daily':
        df = swaps_dexs_daily
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'DEX'] = 'Other'
        df = df.groupby(['Date', 'DEX']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
    elif st.session_state.dexs_interval == 'Weekly':
        df = swaps_dexs_daily
        df = df.groupby([pd.Grouper(freq='W', key='Date'), 'DEX']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'DEX'] = 'Other'
        df = df.groupby(['Date', 'DEX']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
    elif st.session_state.dexs_interval == 'Monthly':
        df = swaps_dexs_daily
        df = df.groupby([pd.Grouper(freq='M', key='Date'), 'DEX']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'DEX'] = 'Other'
        df = df.groupby(['Date', 'DEX']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='DEX', custom_data=['DEX'], title='Swapped Volume of Top DEXs by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Swaps'], ascending=[True, False]), x='Date', y='Swaps', color='DEX', custom_data=['DEX'], title='Swaps of Top DEXs by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swaps', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Swappers'], ascending=[True, False]), x='Date', y='Swappers', color='DEX', custom_data=['DEX'], title='Swappers of Top DEXs by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swappers', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'AmountAverage'], ascending=[True, False]), x='Date', y='AmountAverage', color='DEX', custom_data=['DEX'], title='Average Swapped Amount of Top DEXs by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average Amount [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'Volume/Swapper'], ascending=[True, False]), x='Date', y='Volume/Swapper', color='DEX', custom_data=['DEX'], title='Average Swapped Volume of Top DEXs by Volume per Swapper Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume/Swapper [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = go.Figure()
        for i in df['DEX'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("DEX == @i")['Date'],
                y=df.query("DEX == @i")['Volume'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Swapped Volume of Top DEXs by Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['DEX'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("DEX == @i")['Date'],
                y=df.query("DEX == @i")['Swaps'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Swaps of Top DEXs by Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['DEX'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("DEX == @i")['Date'],
                y=df.query("DEX == @i")['Swappers'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Swappers of Top DEXs by Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'AmountMedian'], ascending=[True, False]), x='Date', y='AmountMedian', color='DEX', custom_data=['DEX'], title='Median Swapped Amount of Top DEXs by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median Amount [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'Swaps/Swapper'], ascending=[True, False]), x='Date', y='Swaps/Swapper', color='DEX', custom_data=['DEX'], title='Average Swaps per Swapper of Top DEXs by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swaps/Swapper', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_asset_types:

    st.subheader('Market Shares')

    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.pie(swaps_asset_types_overview, values='Volume', names='Type', title='Share of Total Swapped Volume', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(swaps_asset_types_overview, values='Swaps', names='Type', title='Share of Total Swaps', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(swaps_asset_types_overview, values='Swappers', names='Type', title='Share of Total Swappers', hole=0.4)
        fig.update_traces(showlegend=False, textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Averages')

    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.bar(swaps_asset_types_overview, x='Type', y='Volume/Day', color='Type', title='Average Daily Swapped Volume')
        fig.update_layout(showlegend=False, yaxis_title='Volume/Day [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.bar(swaps_asset_types_overview, x='Type', y='Swaps/Day', color='Type', title='Average Daily Swaps')
        fig.update_layout(showlegend=False, yaxis_title='Swaps/Day')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.bar(swaps_asset_types_overview, x='Type', y='Swappers/Day', color='Type', title='Average Daily Swappers')
        fig.update_layout(showlegend=False, yaxis_title='Swappers/Day')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(swaps_asset_types_overview, x='Type', y='AmountAverage', color='Type', title='Average Swapped Amount')
        fig.update_layout(showlegend=False, yaxis_title='Average Amount [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(swaps_asset_types_overview, x='Type', y='Volume/Swapper', color='Type', title='Average Swapped Volume/Swapper')
        fig.update_layout(showlegend=False, yaxis_title='Volume/Swapper [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.bar(swaps_asset_types_overview, x='Type', y='AmountMedian', color='Type', title='Median Swapped Amount')
        fig.update_layout(showlegend=False, yaxis_title='Median Amount [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(swaps_asset_types_overview, x='Type', y='Swaps/Swapper', color='Type', title='Average Swaps/Swapper')
        fig.update_layout(showlegend=False, yaxis_title='Swaps/Swapper')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='asset_types_interval', horizontal=True)

    if st.session_state.asset_types_interval == 'Daily':
        df = swaps_asset_types_daily
    elif st.session_state.asset_types_interval == 'Weekly':
        df = swaps_asset_types_daily
        df = swaps_asset_types_daily.groupby([pd.Grouper(freq='W', key='Date'), 'Type']).agg(
            {'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum', 'AmountAverage': 'mean',
                'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
    elif st.session_state.asset_types_interval == 'Monthly':
        df = swaps_asset_types_daily
        df = swaps_asset_types_daily.groupby([pd.Grouper(freq='M', key='Date'), 'Type']).agg(
            {'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum', 'AmountAverage': 'mean',
                'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='Type', custom_data=['Type'], title='Swapped Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'Swaps'], ascending=[True, False]), x='Date', y='Swaps', color='Type', custom_data=['Type'], title='Swaps Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swaps', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'Swappers'], ascending=[True, False]), x='Date', y='Swappers', color='Type', custom_data=['Type'], title='Swappers Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swappers', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.line(df.sort_values(['Date', 'AmountAverage'], ascending=[True, False]), x='Date', y='AmountAverage', color='Type', custom_data=['Type'], title='Average Swapped Amount Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average Amount [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.line(df.sort_values(['Date', 'Volume/Swapper'], ascending=[True, False]), x='Date', y='Volume/Swapper', color='Type', custom_data=['Type'], title='Average Swapped Volume per Swapper Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume/Swapper [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = go.Figure()
        for i in df['Type'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Type == @i")['Date'],
                y=df.query("Type == @i")['Volume'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Swaps Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Type'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Type == @i")['Date'],
                y=df.query("Type == @i")['Swaps'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Swaps Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = go.Figure()
        for i in df['Type'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Type == @i")['Date'],
                y=df.query("Type == @i")['Swappers'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Swappers Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.line(df.sort_values(['Date', 'AmountMedian'], ascending=[True, False]), x='Date', y='AmountMedian', color='Type', custom_data=['Type'], title='Median Swapped Amount Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median Amount [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.line(df.sort_values(['Date', 'Swaps/Swapper'], ascending=[True, False]), x='Date', y='Swaps/Swapper', color='Type', custom_data=['Type'], title='Average Swaps per Swapper Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swaps/Swapper', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_assets:

    st.subheader('Market Shares')

    c1, c2, c3 = st.columns(3)
    with c1:
        df = swaps_assets_overview.sort_values('Volume', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        fig = px.pie(df, values='Volume', names='Asset', title='Share of Total Swapped Volume', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = swaps_assets_overview.sort_values('Swaps', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        fig = px.pie(df, values='Swaps', names='Asset', title='Share of Total Swaps', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = swaps_assets_overview.sort_values('Swappers', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        fig = px.pie(df, values='Swappers', names='Asset', title='Share of Total Swappers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Averages')

    c1, c2, c3 = st.columns(3)
    with c1:
        df = swaps_assets_overview.sort_values('Volume/Day', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Volume/Day': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='Volume/Day', color='Asset', title='Average Daily Swapped Volume')
        fig.update_layout(showlegend=False, yaxis_title='Volume/Day [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = swaps_assets_overview.sort_values('Swaps/Day', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Swaps/Day': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='Swaps/Day', color='Asset', title='Average Daily Swaps')
        fig.update_layout(showlegend=False, yaxis_title='Swaps/Day')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = swaps_assets_overview.sort_values('Swappers/Day', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Swappers/Day': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='Swappers/Day', color='Asset', title='Average Daily Swappers')
        fig.update_layout(showlegend=False, yaxis_title='Swappers/Day')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns(2)
    with c1:
        df = swaps_assets_overview.sort_values('AmountAverage', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'AmountAverage': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='AmountAverage', color='Asset', title='Average Swapped Amount')
        fig.update_layout(showlegend=False, yaxis_title='Average Amount [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = swaps_assets_overview.sort_values('Volume/Swapper', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Volume/Swapper': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='Volume/Swapper', color='Asset', title='Average Swapped Volume/Swapper')
        fig.update_layout(showlegend=False, yaxis_title='Volume/Swapper [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = swaps_assets_overview.sort_values('AmountMedian', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'AmountMedian': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='AmountMedian', color='Asset', title='Median Swapped Amount')
        fig.update_layout(showlegend=False, yaxis_title='Median Amount [USD]')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = swaps_assets_overview.sort_values('Swaps/Swapper', ascending=False).reset_index(drop=True)
        df.loc[swaps_assets_overview.index >= 10, 'Asset'] = 'Other'
        df = df.groupby(['Asset']).agg({'Swaps/Swapper': 'mean'}).reset_index()
        fig = px.bar(df, x='Asset', y='Swaps/Swapper', color='Asset', title='Average Swaps/Swapper')
        fig.update_layout(showlegend=False, yaxis_title='Swaps/Swapper')
        fig.update_xaxes(title=None, categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Daily', 'Weekly', 'Monthly'], key='assets_interval', horizontal=True)

    if st.session_state.assets_interval == 'Daily':
        df = swaps_assets_daily
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Asset'] = 'Other'
        df = df.groupby(['Date', 'Asset']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
    elif st.session_state.assets_interval == 'Weekly':
        df = swaps_assets_daily
        df = df.groupby([pd.Grouper(freq='W', key='Date'), 'Asset']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Asset'] = 'Other'
        df = df.groupby(['Date', 'Asset']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
    elif st.session_state.assets_interval == 'Monthly':
        df = swaps_assets_daily
        df = df.groupby([pd.Grouper(freq='M', key='Date'), 'Asset']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()
        df['RowNumber'] = df.groupby('Date')['Volume'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 3, 'Asset'] = 'Other'
        df = df.groupby(['Date', 'Asset']).agg({'Swaps': 'sum', 'Swappers': 'sum', 'Volume': 'sum',
            'AmountAverage': 'mean', 'AmountMedian': 'mean', 'Swaps/Swapper': 'mean', 'Volume/Swapper': 'mean'}).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'Volume'], ascending=[True, False]), x='Date', y='Volume', color='Asset', custom_data=['Asset'], title='Swapped Volume of Top Assets by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Swaps'], ascending=[True, False]), x='Date', y='Swaps', color='Asset', custom_data=['Asset'], title='Swaps of Top Assets by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swaps', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df.sort_values(['Date', 'Swappers'], ascending=[True, False]), x='Date', y='Swappers', color='Asset', custom_data=['Asset'], title='Swappers of Top Assets by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swappers', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'AmountAverage'], ascending=[True, False]), x='Date', y='AmountAverage', color='Asset', custom_data=['Asset'], title='Average Swapped Amount of Top Assets by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Average Amount [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'Volume/Swapper'], ascending=[True, False]), x='Date', y='Volume/Swapper', color='Asset', custom_data=['Asset'], title='Average Swapped Volume of Top Assets by Volume per Swapper Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume/Swapper [USD]', hovermode='x unified')
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
        fig.update_layout(title='Share of Swapped Volume of Top Assets by Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Asset'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Asset == @i")['Date'],
                y=df.query("Asset == @i")['Swaps'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Swaps of Top Assets by Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Asset'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Asset == @i")['Date'],
                y=df.query("Asset == @i")['Swappers'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Share of Swappers of Top Assets by Volume Over Time')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'AmountMedian'], ascending=[True, False]), x='Date', y='AmountMedian', color='Asset', custom_data=['Asset'], title='Median Swapped Amount of Top Assets by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Median Amount [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.2f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df.sort_values(['Date', 'Swaps/Swapper'], ascending=[True, False]), x='Date', y='Swaps/Swapper', color='Asset', custom_data=['Asset'], title='Average Swaps per Swapper of Top Assets by Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Swaps/Swapper', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)