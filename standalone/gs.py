import requests
import time
from tqdm import tqdm

# header = {
#     "cookie": f"remember_prod={config['graphsense']['session']}"
# }

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

def get_QL_results_many(addresses, currency: str, header, params={}):
    results_list = []
    for address in tqdm(addresses, desc="Searching centralized exchange connections for addresses"):
        results_list.append(get_QL_results(address, currency, header, params))
    return results_list



# df_ql = pd.DataFrame(results_list)
# df_ql.drop(columns=["paths"])