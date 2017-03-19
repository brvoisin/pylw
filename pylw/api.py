import requests

from exceptions import LeekWarsApiException 


LW_HOST_URL = 'https://leekwars.com'


class LeekWarsApi(object):
    def __init__(self, host_url=LW_HOST_URL):
        self.host_url = host_url
        self.token = None
        self.farmer = None

    @property
    def leeks(self):
        if self.farmer:
            return sorted(self.farmer['leeks'].values(), key=lambda l: l['id'])

    def raise_for_failure(self, response):
        try:
            if not response.ok or not response.json().get('success'):
                raise LeekWarsApiException(response)
        except ValueError:
            raise LeekWarsApiException(response)

    def farmer_login_token(self, login, password):
        response = requests.post(
            self.host_url + '/api/farmer/login-token/',
            {'login': login, 'password': password}
        )
        self.raise_for_failure(response)
        data = response.json()
        self.token = data['token']
        self.farmer = data['farmer']
        return data

    def garden_get(self, token=None):
        response = requests.get(self.host_url + '/api/garden/get/{}'.format(token or self.token))
        self.raise_for_failure(response)
        return response.json()

    def garden_get_leek_opponents(self, leek_id, token=None):
        response = requests.get(
            self.host_url + '/api/garden/get-leek-opponents/{leek_id}/{token}'.format(
                leek_id=leek_id, token=token or self.token
            )
        )
        self.raise_for_failure(response)
        return response.json()

    def garden_start_solo_fight(self, leek_id, target_id, token=None):
        response = requests.post(
            self.host_url + '/api/garden/start-solo-fight',
            {'leek_id': leek_id, 'target_id': target_id, 'token': token or self.token}
        )
        self.raise_for_failure(response)
        return response.json()


