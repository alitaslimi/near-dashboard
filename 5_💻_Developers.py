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
st.set_page_config(page_title='Developer Activity - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('💻 Developer Activity')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
# @st.cache(ttl=1000, allow_output_mutation=True)
def get_data(query):
    if query == 'Developers Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/785522fc-11fd-4653-ba4c-59d97de43fac/data/latest')
    elif query == 'Developers Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/cee2f6fc-cb23-4c3e-b0a3-b9513c3f51ae/data/latest')
    elif query == 'Developers Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/1cd7ee81-f6c2-4f55-93e9-441de0dd74e2/data/latest')
    elif query == 'Developers Monthly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/f6ebee22-5bd8-45ee-ab54-dc6b5b5cfe16/data/latest')
    elif query == 'States Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/b4561434-a051-417d-9191-46dbcb6952e6/data/latest')
    elif query == 'New Developers Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/64a24714-c19f-4129-9122-c0dcaaf579cd/data/latest')
    elif query == 'New Developers Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/9676f2a5-7b64-4f1d-8f7d-e1f80045451a/data/latest')
    elif query == 'New Developers Monthly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/7104e52b-cd6a-449d-8b7d-f35ed6691f92/data/latest')
    elif query == 'Associations Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/0c1e829f-af1a-4a1b-8678-83f26198a091/data/latest')
    elif query == 'Associations Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/52aa6f7f-bd6c-4412-996c-2d2f0b8d9a58/data/latest')
    elif query == 'Associations Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/5ee7ec79-e65f-4b6b-bed6-2376a27ba3b0/data/latest')
    elif query == 'Associations Monthly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/77960b92-ea71-4d81-894d-69c5bf27b7f3/data/latest')
    elif query == 'Contributions Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/836fb799-c6e4-4b45-965c-2b52eed754f5/data/latest')
    elif query == 'Contributions Monthly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/d5b2c0c8-3152-4383-805a-4ca9594ac7a6/data/latest')
    return None

developers_overview = get_data('Developers Overview')
developers_daily = get_data('Developers Daily')
developers_weekly = get_data('Developers Weekly')
developers_monthly = get_data('Developers Monthly')
states_overview = get_data('States Overview')
new_developers_daily = get_data('New Developers Daily')
new_developers_weekly = get_data('New Developers Weekly')
new_developers_monthly = get_data('New Developers Monthly')
associations_overview = get_data('Associations Overview')
associations_daily = get_data('Associations Daily')
associations_weekly = get_data('Associations Weekly')
associations_monthly = get_data('Associations Monthly')
contributions_overview = get_data('Contributions Overview')
contributions_monthly = get_data('Contributions Monthly')

# Content
st.write(
    """
    [Electric Capital](https://www.electriccapital.com) has recently published its 2022
    [Developer Report](https://www.developerreport.com), which explores code commits across public
    GitHub repositories. In this section of the present dashboard, the developer activity on the
    NEAR blockchain has been investigated.
    """
)

with st.expander('**Methodology**'):
    st.write(
        """
        This section (Developer Activity) of this mega dashboard was particularly created for the
        **NEAR's Developer Activity** challenge on [**MetricsDAO**](https://metricsdao.xyz).

        The data for this dashboard was imported from the [**Flipside Crypto**](https://flipsidecrypto.xyz)
        data platform by using its **REST API**. The data were selected from the **github_activity**
        table of the **Beta** schema of the **NEAR** database, created by [**forg**](https://github.com/forgxyz).
        This data was curated by using Electric Capital's NEAR sub-ecosystems available through their
        [**GitHub repository**](https://github.com/electric-capital/crypto-ecosystems/tree/master/data/ecosystems/n).

        The code for this report is saved and accessible in the **pages** directory of its
        [**GitHub Repository**](https://github.com/alitaslimi/near-dashboard). The links to the SQL queries
        are all available on the repo's main page.

        **Definitions:**
        - **Active Developers:** Those who commit a pull request at least once per selected interval;
        - **New Developers:** Those who commit a pull request for the first time over the selected interval;
        - **Full-Time Developers:** Those who commit at least 10 days each month;
        - **Part-Time Developers:** Those who commit more than once and less than 10 days each month;
        - **One-Time Developers:** Those who commit on only one day each month.
        """
    )

tab_overview, tab_associations, tab_contributions = st.tabs(['**Overview**', '**Associations**', '**Contributions**'])

with tab_overview:
    st.subheader('Overview')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Total Developers**', value=str(developers_overview['Developers'].map('{:,.0f}'.format).values[0]))
    with c2:
        st.metric(label='**Total Organizations**', value=str(developers_overview['Organizations'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Total Repositories**', value=str(developers_overview['Repositories'].map('{:,.0f}'.format).values[0]))
    with c4:
        st.metric(label='**Total Commits**', value=str(developers_overview['Commits'].map('{:,.0f}'.format).values[0]))

    st.subheader('State of Pull Requests')

    c1, c2, c3 = st.columns(3)
    df = states_overview
    with c1:
        fig = px.pie(df, values='Developers', names='State', title='Share of Developers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Repositories', names='State', title='Share of Repositories', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(df, values='Commits', names='State', title='Share of Commits', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Monthly', 'Weekly', 'Daily'], key='developers_interval', horizontal=True)

    if st.session_state.developers_interval == 'Daily':
        df = developers_daily
        new_df = new_developers_daily
    elif st.session_state.developers_interval == 'Weekly':
        df = developers_weekly
        new_df = new_developers_weekly
    elif st.session_state.developers_interval == 'Monthly':
        df = developers_monthly
        new_df = new_developers_monthly

    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Date'], y=df['Commits'], name='Commits'))
    fig.add_trace(go.Line(x=df['Date'], y=df['Repositories'].round(), name='Repositories'))
    fig.update_layout(title_text='Total Number of Commits and Repositories Over Time', yaxis_title='Numbers', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Date'], y=df['Developers'].round(), name='Active Developers'))
    fig.add_trace(go.Line(x=new_df['Date'], y=new_df['NewDevelopers'].round(), name='New Developers'))
    fig.update_layout(title_text='Total Number of Active and New Developers Over Time', yaxis_title='Numbers', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_associations:
    st.subheader('Overview')

    c1, c2, c3 = st.columns(3)
    df = associations_overview
    with c1:
        fig = px.pie(df, values='Developers', names='Association', title='Share of Developers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Repositories', names='Association', title='Share of Repositories', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(df, values='Commits', names='Association', title='Share of Commits', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    interval = st.radio('**Time Interval**', ['Monthly', 'Weekly', 'Daily'], key='associations_interval', horizontal=True)

    if st.session_state.associations_interval == 'Daily':
        df = associations_daily
    elif st.session_state.associations_interval == 'Weekly':
        df = associations_weekly
    elif st.session_state.associations_interval == 'Monthly':
        df = associations_monthly

    fig = px.line(df, x='Date', y='Developers', color='Association', custom_data=['Association'], title='Total Number of Developers by Association Type Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Developers', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.line(df, x='Date', y='Repositories', color='Association', custom_data=['Association'], title='Total Number of Repositories by Association Type Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Repositories', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.line(df, x='Date', y='Commits', color='Association', custom_data=['Association'], title='Total Number of Commits by Association Type Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Commits', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_contributions:
    st.subheader('Overview')

    c1, c2, c3 = st.columns(3)
    df = contributions_overview
    with c1:
        fig = px.pie(df, values='Developers', names='Contribution', title='Share of Developers', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Repositories', names='Contribution', title='Share of Repositories', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(df, values='Commits', names='Contribution', title='Share of Commits', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')

    df = contributions_monthly

    fig = px.line(df, x='Date', y='Developers', color='Contribution', custom_data=['Contribution'], title='Total Number of Developers by Contribution Type Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Developers', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.line(df, x='Date', y='Repositories', color='Contribution', custom_data=['Contribution'], title='Total Number of Repositories by Contribution Type Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Repositories', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.line(df, x='Date', y='Commits', color='Contribution', custom_data=['Contribution'], title='Total Number of Commits by Contribution Type Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Commits', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Conclusion')
st.write(
    """
    As the data suggested, the developer activity has stagnated over 2022 and it started to
    decrease over the months leading to the end of the year. The number of new developers
    has decreased to one-third compared to mid-2022 which shows the lack of interest in this blockchain.
    The number of commits has also decreased since the fall of 2022. The majority of developers have
    only committed once to a repository and less than 3% of the total developers count are
    full-time contributors. While the number of both full-time and part-time developers has remained
    relatively the same over the final months of 2022, the decrease in one-time developers has
    also been an indication of a lack of interest for new developers to contribute and involve in the
    development of the NEAR ecosystem.
    """
)