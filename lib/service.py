import requests

class Service(object):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.session = requests.Session()

    def reset_session(self):
        self.session.cookies.clear()

    def first_request(self):
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
        self.session.post(self.url, data=data, timeout=3)

        def second_request(self, user, password):
            data = {
                "operationName":
                "userLogin",
                "variables": {
                    "input": {
                        "email": user,
                        "password": password,
                    }
                },
                "query":
                "mutation userLogin($input: LoginInput!) {\\n  userLogin(input: $input) {\\n    user {\\n      id\\n      ...featureFlagsFatQuery\\n      account {\\n        id\\n        ...accountFatQuery\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment accountFatQuery on Account {\\n  accountId\\n  accountType\\n  displayName\\n  emailAddress\\n  hasProductSubscription\\n  token\\n  __typename\\n}\\n\\nfragment featureFlagsFatQuery on User {\\n  sessionId\\n  account {\\n    accountId\\n    accountType\\n    featureFlagsHash\\n    hasProductSubscription\\n    productSubscription {\\n      id\\n      type\\n      typeCode\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n"
            }
            r = self.session.post(self.url,
                                  headers=self.headers,
                                  data=data)

            print(r.content)
