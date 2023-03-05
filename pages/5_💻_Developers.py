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
st.set_page_config(page_title='Developer Activity - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('💻 Developer Activity')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
developers_overview = data.get_data('Developers Overview')
developers_daily = data.get_data('Developers Daily')
developers_weekly = data.get_data('Developers Weekly')
developers_monthly = data.get_data('Developers Monthly')
states_overview = data.get_data('States Overview')
new_developers_daily = data.get_data('New Developers Daily')
new_developers_weekly = data.get_data('New Developers Weekly')
new_developers_monthly = data.get_data('New Developers Monthly')
associations_overview = data.get_data('Associations Overview')
associations_daily = data.get_data('Associations Daily')
associations_weekly = data.get_data('Associations Weekly')
associations_monthly = data.get_data('Associations Monthly')
contributions_overview = data.get_data('Contributions Overview')
contributions_monthly = data.get_data('Contributions Monthly')

# Content
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