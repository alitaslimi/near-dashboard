# Libraries
import streamlit as st
import PIL

# Page Favicon
favicon = PIL.Image.open('favicon.png')

# Layout
st.set_page_config(page_title='NEAR Mega Dashboard', page_icon=favicon, layout='wide')
st.title('NEAR Mega Dashboard')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Content
st.subheader('Introduction')

st.write(
    """
    [**NEAR Protocol**](https://near.org) is a sharded, proof-of-stake (PoS), layer1 blockchain
    that is simple to use, secure and scalable. It is designed to provide the best possible
    experience for developers and users to ultimately, facilitate the mainstream adoption of
    decentralized applications. Unlike other blockchains, this network has been built from the
    ground up to be the easiest in the world for both developers and their end-users while
    still providing the scalability necessary to serve those users. It facilitates the development
    of decentralized applications, even if developers are only used to building with traditional
    web or app concepts. Besides, NEAR onboards users with a smooth experience, even if they
    have never used crypto, tokens, keys, wallets, or other blockchain artifacts. It also allows
    the application to scale seamlessly. The underlying platform automatically expands capacity
    via sharding without additional costs or effort on your part.

    NEAR is the native token of the NEAR blockchain. It is used for transaction fees, staking,
    acquiring a validator seat, and decentralized applications. All transactions which occur on
    the NEAR blockchain must be paid for using NEAR. Fundamental to PoS ecosystems, NEAR can be
    delegated to validators (staked) to earn NEAR rewards. To become a validator on the NEAR
    blockchain a minimum amount of NEAR is required. Last but not least, those building on the
    NEAR ecosystem can choose to leverage the NEAR token in several ways expanding on its utility.
    """
)

st.subheader('Methodology')

st.write(
    """
    The data for this mega dashboard were selected from the [**Flipside Crypto**](https://flipsidecrypto.xyz)
    data platform by using its **REST API**. These queries are currently set to **re-run every 24 hours** to
    cover the latest data and are imported as a JSON file directly to each page. The code for this tool is
    saved and accessible in its [**GitHub Repository**](https://github.com/alitaslimi/near-dashboard).

    This mega dashboard is designed and structured in multiple **Pages** that are accessible using the sidebar.
    Each of these Pages addresses a different segment of the NEAR ecosystem. By browsing each page
    (Macro, Transfers, Swaps, NFTs, etc.) you are able to dive deeper into each secotr of the NEAR's
    network.
    """
)

st.write("#")

# Credits
c1, c2, c3 = st.columns(3)
with c1:
    st.info('**Data Analyst: [@AliTslm](https://twitter.com/AliTslm)**', icon="💡")
with c2:
    st.info('**GitHub: [@alitaslimi](https://github.com/alitaslimi)**', icon="💻")
with c3:
    st.info('**Data: [Flipside Crypto](https://flipsidecrypto.xyz)**', icon="🧠")