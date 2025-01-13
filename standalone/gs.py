import requests
import time
from tqdm import tqdm
import graphsense
from graphsense.api import bulk_api, general_api
import pandas as pd
from datetime import datetime

def ts_to_pds(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def get_QL_results(address: str, currency: str, header, params={}) -> dict:

    seconds = params.get("seconds",60)
    max_depth = params.get("max_depth",30)
    max_breadth = params.get("max_breadth",200)
    base_uri = params.get("base_uri", "https://api.ikna.io")

    def get_task_id(address: str) -> str:
        rq = f"{base_uri}/quicklock/follow_flows_to_exchange/{currency}?perpetrator_address={address}&max_search_depth={max_depth}&max_search_breadth={max_breadth}&search_time_seconds={seconds}"

        response = requests.get(rq, headers=header)
        response.json()
        return response.json()['task_id']

    def get_data(task_id):

        response_got = False
        while not response_got:
            req = f"{base_uri}/quicklock/get_task_state/{task_id}?include_path_details=false"
            response = requests.get(req, headers=header)
            response_json = response.json()
            if response_json['state'] in ["done", "timeout"]:
                response_got = True
            elif response_json['state'] in ["error"]:
                raise Exception(response_json["error_ctx"])
            else:
                time.sleep(2)

        rq_get_result = f"{base_uri}/quicklock/get_task_state/{task_id}?include_path_details=true"

        response = requests.get(rq_get_result, headers=header)
        result = response.json()
        results = result['results']
        data = {
            "address": address,
            "pct_traced_to_exchange": results['pct_traced_to_exchange'],
            "nr_pathes_found": results['nr_pathes_found'],
            "paths": results['paths']
        }
        return data

    task_id = get_task_id(address)
    return get_data(task_id)

def get_QL_results_many(addresses, currency: str, header, cache, params={}):
    results_list = []
    for address in tqdm(addresses, desc="Searching centralized exchange connections for addresses"):
        if address in cache:
            result = cache[address]
        else:
            result = get_QL_results(address, currency, header, params)
            cache[address] = result
        results_list.append(result)
    return results_list


def get_Pathfinder_link_from_ql_result(ql_result):
    paths = ql_result["paths"]
    path = paths[0]["nodes"]
    addresses_ql = [node["output_address"] for node in path]
    transactions_ql = [node["tx_hash"] for node in path]

    # assemble the trace string
    transaction_prefix = "T_"
    perpetrator_prefix = "PA_"
    neutral_prefix = "HA_"
    trace_str = f"{perpetrator_prefix}{addresses_ql[0]}"
    n_txs = len(transactions_ql)
    for i in range(1, n_txs):
        trace_str += f",{transaction_prefix}{transactions_ql[i]},{neutral_prefix}{addresses_ql[i]}"

    return f"https://app.ikna.io/pathfinder/btc/path/{trace_str}"


def get_csv(configuration, operation, CURRENCY, body):
    with graphsense.ApiClient(configuration) as clnt:
        blkapi = bulk_api.BulkApi(clnt)

        # documentation about available bulk operations can be found
        # here https://api.ikna.io/#/bulk/bulk_csv
        rcsv = blkapi.bulk_csv(
                    CURRENCY,
                    operation=operation,
                    body=body,
                    num_pages=1,
                    _preload_content=False
                )
        return pd.read_csv(rcsv)