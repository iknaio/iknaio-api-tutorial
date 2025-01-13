import json
import time
import requests
import json_api_doc
import concurrent.futures
import pandas as pd
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# define the retry strategy
retry_strategy = Retry(
    total=4,  # maximum number of retries
    status_forcelist=[429],  # the HTTP status codes to retry on
)

# create an HTTP adapter with the retry strategy and mount it to the session
adapter = HTTPAdapter(max_retries=retry_strategy)

# create a new session object
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

base_path = "https://api.dark-web-monitor.cflw.com/v3/"

def authenticate_api(credentials: dict):
    response = requests.post(url=f"{base_path}auth", data=credentials)

    if response.status_code != 201:
        raise ConnectionError("Authentication Failed", response.status_code)

    content = json.loads(response.content.decode("utf-8"))
    auth_token = content["accessToken"]
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {0}".format(auth_token),
    }
    return headers


def send_request(
    endpoint: str, headers, params={}, deserialize: bool = True
):
    response = session.get(
        url=base_path + endpoint,
        headers=headers,
        params=params,
        timeout=120,
    )

    # Handle Successful Requests
    if response.status_code == 200 or response.status_code == 201:
        content = json.loads(response.content.decode("utf-8"))
        meta = content.get("meta", content)
        data = (
            json_api_doc.deserialize(content)
            if deserialize
            else content.get("data", content)
        )
        return data, meta
    elif response.status_code == 429:
        print(response)
    return None

def get_domains_by_title(title, headers):
    # Collect all domains in a list first
    domain_data = []

    # Loop until all pages have been collected
    page = 1
    while True:
        # request domains with title
        data, meta = send_request(
            endpoint="darknet-domains",
            headers=headers,
            params={
                "title": title,
                "page": page,
                "limit": 1000,
            },
        )

        # add domains to domain data
        domain_data.extend(data)

        print(f"Processed {page} out of {meta['pagination']['total_pages']} pages")
        
        # stop if all pages have been collected
        if meta["pagination"]["total_pages"] == page:
            del data, meta
            break
        page += 1

    # convert to dataframe
    domain_columns = [
        "type",
        "id",
        "domain_url",
        "title",
        "status",
        "uptime",
        "page_count",
        "clearnet_cohost_count",
        "darknet_cohost_count",
        "inbound_count",
        "outbound_count",
        "discovered_at",
    ]
    return pd.DataFrame(domain_data, columns=domain_columns)

def get_crypto_addresses_for_domains(df_domains, headers):
    # Collect all crypto-asset data in a list first
    crypto_data = []

    # function to request crypto-assets for a specific domain
    def request_crypto_data(row):
        domain_id = row["id"]
        data, meta = send_request(
            endpoint="crypto-asset-addresses",
            headers=headers,
            params={
                "filter[relatedObject][type]": "darknet-domain",
                "filter[relatedObject][id]": domain_id,
                "limit": 1000,
                "page": 1,
            },
        )
        
        # Add domain_id to each entry in data
        for entry in data:
            entry["domain_id"] = domain_id
        return data


    # Process domains using a ThreadPoolExecutor for concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(request_crypto_data, row): idx
            for idx, row in df_domains.iterrows()
        }
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Processing domains",
        ):
            idx = futures[future]
            try:
                data = future.result()
                crypto_data.extend(data)
            except Exception as exc:
                # import traceback
                # print(traceback.format_exc())
                print(f"Domain {idx} generated an exception: {exc}")


    # Convert the list of crypto-asset data to a DataFrame
    crypto_columns = [
        "domain_id",
        "id",
        "type",
        "address",
        "appearances",
        "discovered_at",
    ]
    df_cryptos = pd.DataFrame(crypto_data, columns=crypto_columns)
    df_cryptos = df_cryptos.rename(columns={"id": "crypto_asset_id"})
    return df_cryptos