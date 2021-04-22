import requests
import json
from algoliasearch.search_client import SearchClient
import os

# Step1: 从cloudflare KV获取现有列表

res = requests.get("https://list_main.kxxh.workers.dev")
tv_ids = [item['name'] for item in res.json()['tv_ids']]

# Step2: 从KV获取电视详情
tvs = []
for tv_id in tv_ids:
    res = requests.get(f"https://tv.kxxh.workers.dev/{tv_id}")
    tv_json = res.json()
    name = tv_json.name
    tvs.append(tv_json)

# Step3: 向algolia 更新索引
APP_ID = os.env("ALGOLIA_APP_ID")
API_KEY = os.env("ALGOLIA_API_KEY")
client = SearchClient.create(APP_ID, API_KEY)
index = client.init_index("prod_TV_vis")
objects = [
    {
        "name": item.name,
        "url": f"/tv/{item.meta.tv_id}"
    } for item in tvs
]
index.replace_all_objects(objects)

# Step4: 写数据到json
for tv_json in tvs:
    with open(f"out/{name}.json", "w", encoding="utf8") as f:
        json.dump(tv_json, f)
