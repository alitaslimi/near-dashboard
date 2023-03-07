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
st.set_page_config(page_title='Social - NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('👤 Social')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
social_overview = data.get_data('Social Overview')
social_daily = data.get_data('Social Daily')
profile_changes_overview = data.get_data('Profile Changes Overview')
profile_changes_daily = data.get_data('Profile Changes Daily')
profile_tags_overview = data.get_data('Profile Tags Overview')
profile_tags_daily = data.get_data('Profile Tags Daily')
profile_linktree_overview = data.get_data('Profile Linktree Overview')
profile_linktree_daily = data.get_data('Profile Linktree Daily')
profile_image_overview = data.get_data('Profile Image Overview')
profile_image_daily = data.get_data('Profile Image Daily')
profile_nfts_overview = data.get_data('Profile NFTs Overview')
profile_nfts_daily = data.get_data('Profile NFTs Daily')
social_actions_overview = data.get_data('Social Actions Overview')
social_actions_daily = data.get_data('Social Actions Daily')
social_activity_overview = data.get_data('Social Activity Overview')
social_activity_daily = data.get_data('Social Activity Daily')
social_active_users = data.get_data('Social Active Users')
social_following_daily = data.get_data('Social Following Daily')
social_following_counts = data.get_data('Social Following Counts')
social_widgets_overview = data.get_data('Social Widgets Overview')
social_widgets_daily = data.get_data('Social Widgets Daily')
social_widgets_creators = data.get_data('Social Widgets Creators')

# Content
st.write(
    """
    [NEAR Social](https://near.social) is a decentralized social network built on the NEAR Protocol
    blockchain. It allows users to connect, share content, and earn rewards for their activity on
    the platform. NEAR Protocol Social employs a unique approach to content moderation, where users
    are incentivized to identify and flag inappropriate content, rather than relying solely on
    centralized moderation. The platform aims to create a more equitable and transparent social
    media experience, where users have more control over their data and can earn tokens for their
    contributions to the network. Overall, NEAR Protocol Social represents a promising alternative
    to traditional social media platforms, offering a decentralized and community-driven approach
    to content creation and moderation.
    """
)

with st.expander('**Methodology**'):
    st.write(
        """
        This section (Social) of this mega dashboard was particularly created for the
        **NEAR - 18. Social Dashboard** challenge on [**MetricsDAO**](https://metricsdao.xyz).

        The data for this dashboard was imported from the [**Flipside Crypto**](https://flipsidecrypto.xyz)
        data platform by using its **REST API**. The code for this report is saved and accessible in the
        **pages** directory of the app's [**GitHub Repository**](https://github.com/alitaslimi/near-dashboard).

        Here are the links to the SQL queries:
        
        **Overview**:
        [NEAR Social Overview](https://flipsidecrypto.xyz/edit/queries/7dfa5093-2701-4134-aba2-2645e1885e52) |
        [NEAR Social Daily](https://flipsidecrypto.xyz/edit/queries/bd7034cd-4056-47da-ad26-8fa5ef4b2c4e)

        **Profiles**:
        [Changes Overview](https://flipsidecrypto.xyz/edit/queries/2e507b1d-5e0a-40f2-8f1a-96a5962795ae) |
        [Changes Daily](https://flipsidecrypto.xyz/edit/queries/a66106f1-6349-48f1-8afe-a9bcc0146ff3) |
        [Tags Overview](https://flipsidecrypto.xyz/edit/queries/a19cd13f-5d61-4750-8b7f-efc3024d59d5) |
        [Tags Daily](https://flipsidecrypto.xyz/edit/queries/52070e5e-cbc4-45e4-95ce-35be6bd9b856) |
        [Linktree Overview](https://flipsidecrypto.xyz/edit/queries/f0bc3334-7c2a-426e-a243-2665adb9b57e) |
        [Linktree Daily](https://flipsidecrypto.xyz/edit/queries/37e88d51-9121-443d-a482-b6f3d40e2e2d) |
        [Image Overview](https://flipsidecrypto.xyz/edit/queries/b8f691a2-bebf-4711-a98f-43c01ca0c4ae) |
        [Image Daily](https://flipsidecrypto.xyz/edit/queries/e81bfbad-f31d-4b8a-b002-843d3cf0b5c9) |
        [NFTs Overview](https://flipsidecrypto.xyz/edit/queries/d0c5ef3b-f173-4b35-b81e-ac109e96b66d)

        **Activities**:
        [Actions Overview](https://flipsidecrypto.xyz/edit/queries/ecd84aac-038b-4d96-8733-e5dca7525ad8) |
        [Actions Daily](https://flipsidecrypto.xyz/edit/queries/fd67cbff-6180-42de-b0f5-575f77668aa1) |
        [Activity Overview](https://flipsidecrypto.xyz/edit/queries/3fd04ee6-1d12-41e8-9fe9-98213907078c) |
        [Activity Daily](https://flipsidecrypto.xyz/edit/queries/9a727f42-ebdf-4998-8890-9429d6b9469e) |
        [Active Users](https://flipsidecrypto.xyz/edit/queries/0221868e-b0d9-4f0f-99c8-3a79aa2692d7)

        **Followings**:
        [Following Daily](https://flipsidecrypto.xyz/edit/queries/0824497f-a8c0-4869-a922-c786196398a7) |
        [Following Counts](https://flipsidecrypto.xyz/edit/queries/6582612a-2527-4129-9770-62690e188bc5)

        **Widgets**:
        [Widgets Overview](https://flipsidecrypto.xyz/edit/queries/b51c9aee-7c4f-43d9-b015-564f28b25545) |
        [Widgets Daily](https://flipsidecrypto.xyz/edit/queries/204b47f7-a3dc-4b22-88d9-8742360281d9) |
        [Widgets Creators](https://flipsidecrypto.xyz/edit/queries/04675497-866c-406e-b522-0ada2c2a44f7)
        """
    )

st.header('Analysis')
st.write(
    """
    This section covers the users' journey from creating and updating their profiles to doing different
    types of activities on the network.
    """
)

tab_overview, tab_profiles, tab_activities, tab_followings, tab_widgets = st.tabs(
    ['**Overview**', '**Profiles**', '**Activities**', '**Followings**', '**Widgets**'])

with tab_overview:
    st.subheader('Overview')

    df = social_overview
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Total Conducted Actions**', value=str(df['Actions'].map('{:,.0f}'.format).values[0]))
    with c2:
        st.metric(label='**Total Profile Changes**', value=str(df['Changes'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Total Users**', value=str(df['Users'].map('{:,.0f}'.format).values[0]))
    with c4:
        st.metric(label='**Total Profiles**', value=str(df['Profiles'].map('{:,.0f}'.format).values[0]))

    df = social_daily
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['Date'], y=df['Actions'], name='User Interactions', hovertemplate='Interactions: %{y:,.0f}<extra></extra>'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['NewUsersCumulative'], name='Cumulative New Users', hovertemplate='Cumulative New Users: %{y:,.0f}<extra></extra>'), secondary_y=True)
    fig.update_layout(title_text='Daily Number of User Interactions and Cumulative New Users', hovermode='x unified')
    fig.update_yaxes(title_text='Interactions', secondary_y=False, rangemode='tozero')
    fig.update_yaxes(title_text='Addresses', secondary_y=True, rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots()
    fig.add_trace(go.Line(x=df['Date'], y=df['ActiveUsers'], name='Active', hovertemplate='Active: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Date'], y=df['NewUsers'], name='New', hovertemplate='New: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Daily Number of Active and New Users', hovermode='x unified')
    fig.update_yaxes(title_text='Addresses', rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_profiles:
    st.subheader('Profile Changes')

    df = profile_changes_overview
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='Changes', names='Section', title='Share of Changes by each Profile Section', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df, values='Profiles', names='Section', title='Share of Users Changing each Profile Section', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Changes Over Time')

    df = profile_changes_daily
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values(['Date', 'Changes'], ascending=[True, False]), x='Date', y='Changes', color='Section', custom_data=['Section'], title='Daily Number of Profile Changes by Section')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Changes', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df.sort_values(['Date', 'Profiles'], ascending=[True, False]), x='Date', y='Profiles', color='Section', custom_data=['Section'], title='Daily Number of Users Changing Their Profile by Section')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = go.Figure()
        for i in df['Section'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Section == @i")['Date'],
                y=df.query("Section == @i")['Changes'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Daily Share of Profile Changes by Section', hovermode='x unified')
        fig.update_traces(hovertemplate='%{y:,.0f}%<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Section'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Section == @i")['Date'],
                y=df.query("Section == @i")['Profiles'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Daily Share of Users Changing Their Profile by Section', hovermode='x unified')
        fig.update_traces(hovertemplate='%{y:,.0f}%<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Profile Sections')
    st.write(
        """
        **Tags**
        
        This segment covers the individual section of each user's profile to determine the most popular
        tags, other social networks, and profile images among users.
        """
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        df = profile_tags_daily
        df.loc[df['Profiles'] == 1, 'Tag'] = 'Other'
        df = df.groupby(['Date', 'Tag']).agg('sum').reset_index()
        fig = px.bar(df, x='Date', y='Profiles', color='Tag', custom_data=['Tag'], title='Daily Popular Profile Tags')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = profile_tags_overview.sort_values('Profiles', ascending=False).reset_index(drop=True)
        df.loc[profile_tags_overview.index >= 10, 'Tag'] = 'Other'
        df = df.groupby('Tag').agg('sum').reset_index()
        fig = px.pie(df, values='Profiles', names='Tag', title='Most Popular Profile Tags', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.write(
        """
        **Linktree**
        
        Twitter has been the most linked social network in NEAR Social user profiles with nearly 50%
        of the total. Telegram has been the 2nd most popular social platform among web3 users on
        NEAR Social.
        """
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        df = profile_linktree_daily
        fig = px.bar(df, x='Date', y='Profiles', color='Network', custom_data=['Network'], title='Daily Popular Social Networks Among Users')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = profile_linktree_overview
        fig = px.pie(df, values='Profiles', names='Network', title='Most Popular Social Networks Among Users', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.write(
        """
        **Profile Image**

        The data shows that more than 75% of users have uploaded their profile image, while
        less than 10% of them used a URL for their image. Interestingly, a portion of the users
        used their NEAR NFTs as their profile images.
        """
    )

    c1, c2 = st.columns(2)
    with c1:
        df = profile_image_overview
        fig = px.pie(df, values='Profiles', names='Type', title='Most Popular Profile Images by Type', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = profile_nfts_overview.sort_values('Profiles', ascending=False).reset_index(drop=True)
        df.loc[profile_nfts_overview.index >= 10, 'Collection'] = 'Other'
        df = df.groupby('Collection').agg('sum').reset_index()
        fig = px.pie(df, values='Profiles', names='Collection', title='Most Popular NFT Profile Images by Collection', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    df = profile_image_daily
    fig = px.bar(df, x='Date', y='Profiles', color='Type', custom_data=['Type'], title='Daily Popular Profile Image Types')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_activities:
    st.subheader('Overview')

    c1, c2 = st.columns([2, 1])
    with c1:
        df = social_actions_daily.groupby(['Date', 'Action']).agg('sum').reset_index()
        df['RowNumber'] = df.groupby(['Date'])['Users'].rank(method='max', ascending=False)
        df.loc[df['RowNumber'] > 5, 'Action'] = 'Other'
        df = df.groupby(['Date', 'Action']).agg('sum').reset_index()
        fig = px.bar(df, x='Date', y='Users', color='Action', custom_data=['Action'], title='Daily Number of Users by Action Type')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = social_actions_overview
        df = social_actions_overview.sort_values('Users', ascending=False).reset_index(drop=True)
        df.loc[social_actions_overview.index >= 10, 'Action'] = 'Other'
        df = df.groupby('Action').agg('sum').reset_index()
        fig = px.pie(df, values='Users', names='Action', title='Most Popular Action Types Among Users', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activities')

    st.write(
        """
        The analysis of the activities conducted by users has demonstrated that posts accounted for
        less than 30% of the total activities on the network. On the other hand, less than 20% of
        activities consist of comments of users' responding to others. The majority of user interaction
        with the network is liking posts, with more than half of the total.

        Interestingly, the share of users conducting these activities is different with more than
        60% of them posting at least once on the network. While only a portion of users commented
        on posts, nearly 30% of them interacted with others by liking their posts.
        """
    )

    c1, c2 = st.columns(2)
    with c1:
        df = social_activity_overview
        fig = px.pie(df, values='Transactions', names='Action', title='Share of Activities', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        df = social_activity_daily
        fig = px.bar(df, x='Date', y='Transactions', color='Action', custom_data=['Action'], title='Daily Number of Activities')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Profiles', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Action'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Action == @i")['Date'],
                y=df.query("Action == @i")['Transactions'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Daily Share of Users Activities', hovermode='x unified')
        fig.update_traces(hovertemplate='%{y:,.0f}%<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = social_activity_overview
        fig = px.pie(df, values='Users', names='Action', title='Share of Users by Activity', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        df = social_activity_daily
        fig = px.bar(df, x='Date', y='Users', color='Action', custom_data=['Action'], title='Daily Number of Users Doing Different Activities')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Users', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = go.Figure()
        for i in df['Action'].unique():
            fig.add_trace(go.Scatter(
                name=i,
                x=df.query("Action == @i")['Date'],
                y=df.query("Action == @i")['Users'],
                mode='lines',
                stackgroup='one',
                groupnorm='percent'
            ))
        fig.update_layout(title='Daily Share of Users Doing Different Activities', hovermode='x unified')
        fig.update_traces(hovertemplate='%{y:,.0f}%<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Most Active Users')
    
    c1, c2, c3 = st.columns(3)
    with c1:
        df = social_active_users.query("Action == 'Post'").sort_values('Transactions', ascending=False).head(20)
        fig = px.bar(df, x='User', y='Transactions', color='User', title='Users With the Highest Number of Posts')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Posts', xaxis={'categoryorder':'total ascending'}, hovermode='x unified')
        fig.update_traces(hovertemplate='Posts: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        df = social_active_users.query("Action == 'Comment'").sort_values('Transactions', ascending=False).head(20)
        fig = px.bar(df, x='User', y='Transactions', color='User', title='Users With the Highest Number of Comments')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Comments', xaxis={'categoryorder':'total ascending'}, hovermode='x unified')
        fig.update_traces(hovertemplate='Comments: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        df = social_active_users.query("Action == 'Like'").sort_values('Transactions', ascending=False).head(20)
        fig = px.bar(df, x='User', y='Transactions', color='User', title='Users With the Highest Number of Likes')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Likes', xaxis={'categoryorder':'total ascending'}, hovermode='x unified')
        fig.update_traces(hovertemplate='Likes: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    with st.expander('**Data Table**', expanded=False):
        st.dataframe(social_active_users, use_container_width=True)

with tab_followings:
    st.subheader('Overview')

    df = social_following_daily
    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Date'], y=df['Transactions'], name='Followings', hovertemplate='Followings: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Date'], y=df['Users'], name='Users', hovertemplate='Users: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Daily Number of Users Following Others and Their Following Actions', hovermode='x unified')
    fig.update_yaxes(title_text='Number')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    df = social_following_counts
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values('Followers', ascending=False).head(20), x='User', y='Followers', color='User', title='Users With the Highest Number of Followers')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Followers', xaxis={'categoryorder':'total ascending'}, hovermode='x unified')
        fig.update_traces(hovertemplate='Followers: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.bar(df.sort_values('Followings', ascending=False).head(20), x='User', y='Followings', color='User', title='Users With the Highest Number of Followings')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Followings', xaxis={'categoryorder':'total ascending'}, hovermode='x unified')
        fig.update_traces(hovertemplate='Followings: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    with st.expander('**Data Table**', expanded=False):
        st.dataframe(social_following_counts, use_container_width=True)

with tab_widgets:
    st.subheader('Overview')

    df = social_widgets_overview
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label='**Total Widgets Created**', value=str(df['Widgets'].map('{:,.0f}'.format).values[0]))
    with c2:
        st.metric(label='**Total Users Creating Widgets**', value=str(df['Creators'].map('{:,.0f}'.format).values[0]))

    st.subheader('Activity Over Time')

    df = social_widgets_daily
    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Date'], y=df['Widgets'], name='Active', hovertemplate='Widgets: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Date'], y=df['Creators'], name='New', hovertemplate='Creators: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Daily Number of Widgets Created and Users Creating Them', hovermode='x unified')
    fig.update_yaxes(title_text='Number', rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Top Creators')
    
    df = social_widgets_creators
    fig = px.bar(df.sort_values('Widgets', ascending=False).head(40), x='Creator', y='Widgets', color='Creator', title='Top Widget Creators')
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Widgets', xaxis={'categoryorder':'total ascending'}, hovermode='x unified')
    fig.update_traces(hovertemplate='Widgets: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    with st.expander('**Data Table**', expanded=False):
        st.dataframe(social_widgets_creators, use_container_width=True)

st.header('Conclusion')
st.write(
    """
    Activity on NEAR Social has slowly but surely been increasing since its launch, especially in
    March 2023 when a surge of new users came into the platform. Adding new features and enabling
    users to create widgets, in addition to integrating NFTs as their PFP, helped the social network
    see growth in user engagement. The numbers are not insane, but its prospect seems promising for
    the whole NEAR ecosystem.
    """
)

# Whitespace
st.write("""
    #
    #
    #
""")

# Credits
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.info('**Data Analyst: [@AliTslm](https://twitter.com/AliTslm)**', icon="💡")
with c2:
    st.info('**GitHub: [@alitaslimi](https://github.com/alitaslimi)**', icon="💻")
with c3:
    st.info('**Data: [Flipside Crypto](https://flipsidecrypto.xyz)**', icon="🧠")
with c4:
    st.info('**Bounty Program: [MetricsDAO](https://metricsdao.xyz)**', icon="🏦")