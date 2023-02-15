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
st.set_page_config(page_title='Whales - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('🐋 Whales')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
@st.cache(ttl=1000, allow_output_mutation=True)
def get_data(query):
    if query == 'Wallet Balances Distribution':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/eee5e19b-2632-4fec-b337-e52d85509eb5/data/latest')
    elif query == 'Wallet Balances Whales':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/efb88e24-abba-44e3-ac66-2dfeedb4813b/data/latest')
    elif query == 'Whales Activities':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/296269d7-65e5-422d-a5f5-b28b65d3bf43/data/latest')
    return None

balances_distribution = get_data('Wallet Balances Distribution')
balances_whales = get_data('Wallet Balances Whales')
whales_activities = get_data('Whales Activities')
whales_types = balances_whales.groupby(['Type']).agg(
    {'Address': 'count', 'Transactions': 'sum', 'Inflows': 'sum', 'Outflows': 'sum', 'Balance': 'sum'}).reset_index()

# Content
tab_whales, tab_distribution = st.tabs(['**Whales**', '**Distribution**'])

with tab_whales:
    with st.expander('**Methodology**'):
        st.write(
            """
            This section (Whales) of this mega dashboard was particularly created for the
            **NEAR - 12. The Whales of NEAR** challenge on [**MetricsDAO**](https://metricsdao.xyz).

            The data for this dashboard was imported from the [**Flipside Crypto**](https://flipsidecrypto.xyz)
            data platform by using its **REST API**. The code for this report is saved and accessible in the
            **pages** directory of the app's [**GitHub Repository**](https://github.com/alitaslimi/near-dashboard).
            The links to the SQL queries are all available on the repo's main page.

            To calculate the **wallet balances** for each address, the total **inflows** and **outflows** of NEAR
            tokens to their wallet were measured. Ultimately, the **top 20 addresses** with the highest NEAR balance
            were selected to further analyze their behavior.
            - Inflows: inbound transfers, unstakings, swaps to
            - Outflows: outbound transfers, stakings, swaps from, transaction fees, NFT purchases
            It is worth mentioning that since there are limitations in the calculation of the NFT sales, the inflow
            volume of selling NFTs has not been measured in the current balance model.

            After calculating the balances, the
            [Glassnode's article on Bitcoin Whales](https://insights.glassnode.com/bitcoin-supply-distribution/)
            was adjusted to the NEAR data and those wallet addresses with a NEAR balance of more
            than **20M** tokens were selected as the whales.

            The type of whale addresses could be filtered on each chain to limit the output to your desired categories.
            """
        )

    st.subheader('Overview')

    st.write(
        """
        While more than half of the whales consisted of unlabeled addresses with unknown owners,
        the CEX addresses accounted for more than 50% of the NEARS held by whales. The blockchain
        administrative wallets and a few addresses attributed to DeFi protocols are also among the
        whales but account for just a portion of the overall NEAR balance.
        """
    )

    df = whales_types
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='Balance', names='Type', title='Balance Share of Each Wallet Type Among Whales')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Address', names='Type', title='Address Share of Each Wallet Type Among Whales')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Balances')

    st.write(
        """
        Based on the methodology used in this dashboard to select the whale addresses, only less than 40
        wallets were fitted to the criteria and were chosen as the whales. As the data shows, the wallet
        `5c33c6218d47e00ef229f60da78d0897e1ee9665312550b8afd5f9c7bc6957d2` has been one of the biggest
        whales with massive NEAR holdings.
        """
    )

    df = balances_whales
    fig = px.bar(df, x='Address', y='Balance', color='Type', title='NEAR Balance of Whales')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Balance', hovermode='x unified')
    fig.update_traces(hovertemplate='%{y:,.0f} NEAR<extra></extra>')
    fig.update_xaxes(type='category', categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.write(
        """
        Among the whales and the unlabeled addresses, the wallets of `simpleguy.near`,
        `5c33c6218d47e00ef229f60da78d0897e1ee9665312550b8afd5f9c7bc6957d2` and
        `7981ae28a8314f939c7b2d0cb4fca0cb0ea70e5c022b219425bc9c4d5723e8ce` have conducted a considerable
        number of transactions, showing their level of activity.
        """
    )

    fig = px.bar(df, x='Address', y='Transactions', color='Type', title='Number of Transactions Conducted by Whales')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
    fig.update_traces(hovertemplate='%{y:,.0f}<extra></extra>')
    fig.update_xaxes(type='category', categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    with st.expander('**Data Table**', expanded=False):
        st.dataframe(balances_whales, use_container_width=True)

    st.subheader('Token Flow')

    df = whales_activities.groupby('Flow').agg('sum').reset_index()
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='Volume', names='Flow', title='Volume Share of Activities Among Whales')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Transactions', names='Flow', title='Transactions Share of Activities Among Whales')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    df = balances_whales
    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Address'], y=df['Inflows'], name='Inflows', hovertemplate='Inflow: %{y:,.0f} NEAR<extra></extra>'))
    fig.add_trace(go.Bar(x=df['Address'], y=df['Outflows'], name='Outflows', hovertemplate='Outflow: %{y:,.0f} NEAR<extra></extra>'))
    fig.update_layout(title_text='NEAR Volume of Inflows and Outflows of Whales', yaxis_title='Volume', hovermode='x unified')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activities')

    df = whales_activities.groupby('Action').agg('sum').reset_index()
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='Volume', names='Action', title='Volume Share of Each Activity Among Whales')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Transactions', names='Action', title='Transactions Share of Each Activity Among Whales')
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    df = whales_activities
    fig = px.bar(df, x='Address', y='Volume', color='Action', custom_data=['Action'], title='Number of Transactions Conducted by Whales')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Transactions', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    fig.update_xaxes(type='category', categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_distribution:
    st.subheader('Overview')

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