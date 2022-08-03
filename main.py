allUserstoCheck = [
    {"name": "icebergy_"},
    {"name": "Pentosh1"},
    {"name": "ASvanevik"},
]


import requests, json, os
from dotenv import load_dotenv

load_dotenv()


def getUserID(userName):
    url = "https://api.twitter.com/2/users/by/username/" + str(userName)
    payload = {}
    headers = {"Authorization": os.getenv("Bear")}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_obj = json.loads(response.text)
    Id = json_obj["data"]["id"]
    return Id


def getFollowingsByUserName(userName):
    userid = getUserID(userName)
    names = []

    NextToken = ""
    resp_json = getFollowings(userid)
    for user in resp_json["data"]:
        names.append(user["name"])
    return names


def getFollowings(userID):
    url = (
        "https://api.twitter.com/2/users/"
        + str(userID)
        + "/following"
        + "?max_results=10"
    )
    payload = {}
    headers = {"Authorization": os.getenv("Bear")}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_obj = json.loads(response.text)
    return json_obj


for i in range(len(allUserstoCheck)):
    allUserstoCheck[i]["followings"] = getFollowingsByUserName(
        allUserstoCheck[i]["name"]
    )


def getIntersect(A, B, C):
    AFoll = A["followings"]
    BFoll = B["followings"]
    for a in AFoll:
        if a in BFoll:
            if a not in C:
                C[a] = []
            C[a].append(A["name"])
            C[a].append(B["name"])
            C[a] = list(set(C[a]))


intersect = {}
for i in range(len(allUserstoCheck)):
    for j in range(i, len(allUserstoCheck)):
        getIntersect(allUserstoCheck[i], allUserstoCheck[j], intersect)

for key in intersect:
    if len(intersect[key]) > 1:
        print(key, ": ", intersect[key])
