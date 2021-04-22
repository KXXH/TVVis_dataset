import requests
import json
from algoliasearch.search_client import SearchClient
import os

# Step1: 从cloudflare KV获取现有列表

print("Step1: 从cloudflare KV获取现有列表")
res = requests.get("https://list_main.kxxh.workers.dev")
tv_ids = [item['name'] for item in res.json()['tv_ids']]

# Step2: 从KV获取电视详情
print("Step2: 从KV获取电视详情")
tvs = []
for tv_id in tv_ids:
    print(f"----正在获取电视id={tv_id}")
    res = requests.get(f"https://tv.kxxh.workers.dev/{tv_id}")
    tv_json = res.json()
    tvs.append(tv_json)

# Step3: 向algolia 更新索引
print("Step3: 向algolia 更新索引")
APP_ID = os.getenv("ALGOLIA_APP_ID")
API_KEY = os.getenv("ALGOLIA_API_KEY")
client = SearchClient.create(APP_ID, API_KEY)
index = client.init_index("prod_TV_vis")
objects = [
    {
        "name": item["name"],
        "url": f'/tv/{item["meta"]["tv_id"]}'
    } for item in tvs if "name" in item
]
index.replace_all_objects(objects, {
                          'autoGenerateObjectIDIfNotExist': True
                          })

# Step4: 写数据到json
print("Step4: 写数据到json")
for tv_json in tvs:
    if "name" not in tv_json:
        continue
    name = tv_json["name"]
    print(f"----正在写out/{name}.json")
    with open(f"out/{name}.json", "w", encoding="utf8") as f:
        json.dump(tv_json, f)
