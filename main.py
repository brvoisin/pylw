import requests
import pprint

r = requests.post('https://leekwars.com/api/farmer/login-token/',
                  data={"login": "user", "password": "password"})

data = r.json()
token = data["token"]

print("Inscriptions au tournois")
leeks = data["farmer"]["leeks"]
for id, leek in leeks.items():
    r = requests.post('https://leekwars.com/api/leek/register-tournament/',
                      data={"token": token, "leek_id": id})
    res = r.json()
    if res["success"]:
        print("Succès de l'enregistrement du poireau {}.".format(leek["name"]))
    else:
        print("Échec de l'enregistrement du poireau {}. raison: {}".format(
            leek["name"], res["error"]))

r = requests.post('https://leekwars.com/api/farmer/register-tournament/',
                  data={"token": token})
res = r.json()
if res["success"]:
    print("Succès de l'enregistrement au tournoi eleveur.")
else:
    print("Échec de l'enregistrement au tournoi eleveur. raison: {}".format(
        res["error"]))

team_id = data["farmer"]["team"]["id"]
r = requests.post('https://leekwars.com/api/team/get-private/',
                  data={"token": token, "team_id": team_id})

compos = r.json()["team"]["compositions"]

for compo in compos:
    r = requests.post('https://leekwars.com/api/team/register-tournament/',
                      data={"token": token, "composition_id": compo["id"]})
    res = r.json()
    if res["success"]:
        print("Succès de l'enregistrement de la compo {}.".format(
            compo["name"]))
    else:
        print("Échec de l'enregistrement de la compo {}. raison: {}".format(
            compo["name"], res["error"]))
    print(compo["leeks"][0]["team_fights"])
    team_fights = compo["leeks"][0]["team_fights"]
    for i in range(0, team_fights):
        r = requests.post('https://leekwars.com/api/garden/get-composition-opponents/',
                          data={"token": token, "composition": compo["id"]})
        res = r.json()
        if res["opponents"]:
            pprint.pprint(res["opponents"][0]["id"])
            r = requests.post('https://leekwars.com/api/garden/start-team-fight/',
                              data={"token": token,
                                    "composition_id": compo["id"],
                                    "target_id": res["opponents"][0]["id"]},
                              cookies=r.cookies)
            res = r.json()
            pprint.pprint(res)


fights = data["farmer"]["fights"]

for i in range(50, fights):
    r = requests.post('https://leekwars.com/api/garden/get-farmer-opponents/',
                      data={"token": token})
    res = r.json()
    pprint.pprint(res["opponents"][0]["id"])
    r = requests.post('https://leekwars.com/api/garden/start-farmer-fight/',
                      data={"token": token,
                            "target_id": res["opponents"][0]["id"]},
                      cookies=r.cookies)
    res = r.json()
    pprint.pprint(res)

