 1 import requests
 2 
 3 url = "https://api.rabby.io/v1/points/claim_snapshot"
 4 
 5 headers = {
 6     "Host": "api.rabby.io",
 7     "Connection": "keep-alive",
 8     "Content-Length": "224",
 9     "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
10     "X-Version": "0.92.48",
11     "sec-ch-ua-mobile": "?0",
12     "User-Agent": UserAgent().random,
13     "x-api-ts": str(int(time.time())),
14     "Content-Type": "application/json",
15     "x-api-ver": "v2",
16     "Accept": "application/json, text/plain, */*",
17     "X-Client": "Rabby",
18     "sec-ch-ua-platform": '"Windows"',
19     "Origin": "chrome-extension://acmacodkjb dgmoleebolmdjonilkdbch",
20     "Sec-Fetch-Site": "none",
21     "Sec-Fetch-Mode": "cors",
22     "Sec-Fetch-Dest": "empty",
23     "Accept-Encoding": "gzip, deflate, br",
24     "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
25 }
26 
27 wallets = file_to_list("inputs/wallets.txt")
28 proxy_list = file_to_list("inputs/proxies.txt")
29 
30 for raw_wallet in wallets:
31     try:
32         if " " in raw_wallet.strip():
33             client = Web3Utils(mnemonic=raw_wallet)
34         else:
35             client = Web3Utils(key=raw_wallet)
36 
37         address = client.acct.address.lower()
38         msg = f"{address} Claims Rabby Points"
39 
40         payload = {
41             "id": address,
42             "signature": client.get_signed_code(msg),
43             "invite_code": BONUS_CODE
44         }
45 
46         proxies = {"http": f"http://{proxy_list.pop(0)}"} if proxy_list else None
47 
48         response = requests.post(url, headers=headers, json=payload, proxies=proxies)
49 
50         if response.json().get("error_code") == 0:
51             resp_msg = "Claimed!"
52             logger.success(f"{address} | Claimed!")
53         else:
54             resp_msg = response.json().get("error_msg")
55             logger.info(f"{address} | {resp_msg}")
56 
57         time.sleep(random.uniform(*DELAY))
58     except Exception as e:
59         logger.error(f"{raw_wallet[:15]}... | {e}")
