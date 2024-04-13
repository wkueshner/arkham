import requests
import csv
import os
from datetime import datetime

def fetch_and_save_crypto_prices(api_key):
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameters = {
        'symbol': '1INCH,AAVE,ACA,AEVO,AGIX,AKT,ALGO,ALT,APE,APT,ARB,ARKM,ATOM,AVAX,AXL,AXS,AZERO,BAL,BEAM,BIT,BLUR,BONK,C98,COMP,COW,CRV,CTSI,CYBER,DOGE,DOT,DYDX,DYM,EDU,EGLD,ENS,EUL,FIL,FLOW,FORT,FTM,FTT,FXS,GAL,GALA,GEL,GLMR,GMT,GMX,GRT,GTC,HFT,HNT,HOP,ID,ILV,IMX,INJ,JOE,JTO,JUP,KDA,KUJI,LBR,LDO,LINK,LOOKS,LQTY,LUNA,MANA,MANTA,MASK,MATIC,MAV,MAVIA,MC,MEME,METIS,MINA,MNT,MULTI,MYRIA,NEAR,NEON,NTRN,NYM,OKB,OKT,ONDO,OP,OSMO,PENDLE,PEPE,PIXEL,POL,POOL,PRIME,PYTH,RBN,RDNT,RNDR,RON,ROSE,RPL,SAFE,SAND,SEI,SHIB,SOL,STG,STRK,SUDO,SUI,SUPER,SUSHI,SWISE,TIA,TORN,UNI,WLD,X2Y2,XAI,YFI,YGG,ZETA'
        #All symbols with unlock schedules, whether standardized or not
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()['data']

    # Ensure the directory exists
    os.makedirs('token_price_data', exist_ok=True)

    # Define the CSV file path
    csv_file_path = os.path.join('token_price_data', 'crypto_prices.csv')

    # Open the CSV file for writing
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        #writer.writerow(['timestamp', 'symbol', 'price', 'volume_24h'])

        for symbol, details_list in data.items():  # details_list is a list of dictionaries
            if not details_list:  # Check if the list is empty
                continue  # Skip this symbol if there are no details

            details = details_list[0]  # Assuming we're interested in the first item

            # Now, details is a dictionary from which we can extract the required information
            timestamp = datetime.strptime(details['quote']['USD']['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            price = details['quote']['USD']['price']
            volume_24h = details['quote']['USD']['volume_24h']
            writer.writerow([timestamp, symbol, price, volume_24h])

    print(f"Data successfully saved to {csv_file_path}")

# Example usage
fetch_and_save_crypto_prices('8a31612b-40b3-4357-8dc5-1a7e783c83af')
