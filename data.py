# Libraries
import streamlit as st
import pandas as pd

# Data Sources
# @st.cache(ttl=1000, allow_output_mutation=True)
def get_data(query):
    # Prices
    if query == 'Prices Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/60300b70-dd1e-4716-bc75-3bfc5709250f/data/latest')
    
    # Blocks
    elif query == 'Blocks Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/024b2e03-1063-4bcf-a8de-b35d17e01cbd/data/latest')
    
    elif query == 'Blocks Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/1d55b381-77a7-4e03-b951-58421139cb09/data/latest')
    
    # Transactions
    elif query == 'Transactions Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/3479cc40-da43-4231-b8e8-c5e62974720d/data/latest')
    
    elif query == 'Transactions Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/c984af6f-5955-45f4-bffd-2bab056ee78f/data/latest')
    
    elif query == 'Transactions Heatmap':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/f0f4e88d-4c8c-4ed8-acf9-ccbd213bcec1/data/latest')
    
    elif query == 'Transactions Status Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/bb9626e1-16ac-49dc-a101-54622b0bc96c/data/latest')
    
    elif query == 'Transactions Status Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/1979b40a-c981-486f-a4b6-ca774cc835f5/data/latest')
    
    # Validators
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
    
    # Contracts
    elif query == 'Contracts Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/6eb672c4-e52a-43c1-822f-a1e43cb52b10/data/latest')
    
    elif query == 'Contracts Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/cd150022-71ff-4d0b-8a79-53d1de1ec0b2/data/latest')
    
    elif query == 'Contracts Interactions Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/646055c7-cb50-4933-b897-b2939d328c07/data/latest')
    
    elif query == 'Contracts Interactions Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/baa3c16c-8861-4dfb-99e8-d5fa5d3097ec/data/latest')
    
    # Developers
    elif query == 'Developers Overview':
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
    
    # Bridges
    elif query == 'Bridges Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/4e31e12c-bf4e-40c7-b81b-68927d9d537a/data/latest')
    
    elif query == 'Bridges Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/fea096a4-db6d-48ec-abab-28966966137f/data/latest')
    
    elif query == 'Bridges Tokens Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/137df1be-0ba5-4cdb-9764-bb6935f73e27/data/latest')
    
    elif query == 'Bridges Tokens Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/85db43ba-7b4a-40c8-a805-2759be0b4623/data/latest')

    # Transfers
    elif query == 'Transfers Overview':
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
    
    # CEXs
    elif query == 'CEXs Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/3c4330b0-36d2-4016-a092-1fb72b414f80/data/latest')
    
    elif query == 'CEXs Exchanges Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/ea5814fb-ba21-4b01-9e12-0d44f25980a8/data/latest')
    
    elif query == 'CEXs Exchanges Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/84fc0987-4902-4295-82de-dbdcf0703660/data/latest')
    
    # Swaps
    elif query == 'Swaps Overview':
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
    
    # NFTs
    elif query == 'NFTs Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/90bb096b-e1eb-4b6b-9aab-d74a6d1cf0e8/data/latest')
    
    elif query == 'NFTs Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/e107f8ba-bf27-493d-9c59-c83314007bdb/data/latest')
    
    elif query == 'NFTs Heatmap':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/92e6c337-9045-4f98-94ff-28ecc7285d92/data/latest')
    
    elif query == 'NFTs Marketplaces Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/f810cf3b-bfdd-4945-a416-84aa1c650433/data/latest')
    
    elif query == 'NFTs Marketplaces Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/eacf6eca-444c-48a9-9017-632bcbe63e82/data/latest')
    
    elif query == 'NFTs Collections Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/7db40092-0ef8-4091-9cba-b617846e1642/data/latest')
    
    elif query == 'NFTs Collections Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/252137a6-5992-4ea7-b625-5b6d8847c45b/data/latest')
    
    # Lending - Burrow
    elif query == 'Burrow Netflow':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/215ed4b5-e745-42f9-be3c-87b724ffa22a/data/latest')
    
    elif query == 'Burrow Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/8eb9c5ea-e4bc-41cf-97c4-30e319ffc0cf/data/latest')
    
    elif query == 'Burrow Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/87b41b8b-450b-41d0-b529-fb42e44cd328/data/latest')
    
    elif query == 'Burrow Liquidity Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/f60ab852-fe85-48da-b71a-7022874b661b/data/latest')
    
    elif query == 'Burrow Liquidity Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/78d406b6-ab8d-4ee4-8d90-6943965badbd/data/latest')
    
    # Whales
    elif query == 'Wallet Balances Distribution':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/eee5e19b-2632-4fec-b337-e52d85509eb5/data/latest')
    
    elif query == 'Wallet Balances Whales':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/efb88e24-abba-44e3-ac66-2dfeedb4813b/data/latest')
    
    elif query == 'Whales Activities':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/296269d7-65e5-422d-a5f5-b28b65d3bf43/data/latest')
    
    # Social
    
    elif query == 'Social Creation Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/7dfa5093-2701-4134-aba2-2645e1885e52/data/latest')
    
    elif query == 'Social Changes Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/2e507b1d-5e0a-40f2-8f1a-96a5962795ae/data/latest')
    
    elif query == 'Social Changes Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/a66106f1-6349-48f1-8afe-a9bcc0146ff3/data/latest')
    
    elif query == 'Social Tags Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/a19cd13f-5d61-4750-8b7f-efc3024d59d5/data/latest')
    
    elif query == 'Social Tags Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/52070e5e-cbc4-45e4-95ce-35be6bd9b856/data/latest')
    
    elif query == 'Social Linktree Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/f0bc3334-7c2a-426e-a243-2665adb9b57e/data/latest')
    
    elif query == 'Social Linktree Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/37e88d51-9121-443d-a482-b6f3d40e2e2d/data/latest')
    
    elif query == 'Social Image Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/b8f691a2-bebf-4711-a98f-43c01ca0c4ae/data/latest')
    
    elif query == 'Social Image Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/e81bfbad-f31d-4b8a-b002-843d3cf0b5c9/data/latest')
    
    elif query == 'Social NFTs Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/d0c5ef3b-f173-4b35-b81e-ac109e96b66d/data/latest')
    
    elif query == 'Social NFTs Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/9ae52cb5-7abd-4497-bdf4-f7c1f2b5a3d0/data/latest')
    
    elif query == 'Social Actions Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/ecd84aac-038b-4d96-8733-e5dca7525ad8/data/latest')
    
    elif query == 'Social Actions Daily':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/fd67cbff-6180-42de-b0f5-575f77668aa1/data/latest')
    
    return None