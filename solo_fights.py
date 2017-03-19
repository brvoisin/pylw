import getpass
import random

from pylw import LeekWarsApi


def make_solo_fights():
    login = raw_input('Login: ')
    password = getpass.getpass(prompt='Password: ')
    api = LeekWarsApi()
    api.farmer_login_token(login, password)
    print('Choose your leeks')
    print('\n'.join('{}: {}'.format(i, l['name']) for i, l in enumerate(api.leeks, 1)))
    choice = int(raw_input('Choice [1]: ') or 1)
    leek = api.leeks[choice - 1]
    print('leek ' + leek['name'])
    #api.garden_get()
    opponents = api.garden_get_leek_opponents(leek['id'])['opponents']
    print(opponents)
    print(api.garden_start_solo_fight(leek['id'], random.choice(opponents)['id']))


if __name__ == '__main__':
    make_solo_fights()

