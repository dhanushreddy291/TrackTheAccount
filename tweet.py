import requests, json, os
from dotenv import load_dotenv

load_dotenv()


def getUserID(userName):
    url = "https://api.twitter.com/2/users/by/username/" + str(userName)
    payload = {}
    headers = {
        "Authorization": os.getenv("Bear"),
        "Cookie": os.getenv("Cookie"),
    }
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
        names.append(user["username"])
    return names


def getFollowings(userID):
    url = (
        "https://api.twitter.com/2/users/"
        + str(userID)
        + "/following"
        + "?max_results=100"
    )
    payload = {}
    headers = {
        "Authorization": os.getenv("Bear"),
        "Cookie": os.getenv("Cookie"),
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_obj = json.loads(response.text)
    return json_obj


def getIntersect(A, B, C):
    AFoll = A["followings"]
    BFoll = B["followings"]
    for a in AFoll:
        if a in BFoll:
            if a not in C:
                C[a] = []
            C[a].append(A["username"])
            C[a].append(B["username"])
            C[a] = list(set(C[a]))


def twit(allUserstoCheck):

    for i in range(len(allUserstoCheck)):
        allUserstoCheck[i]["followings"] = getFollowingsByUserName(
            allUserstoCheck[i]["username"]
        )

    intersect = {}
    for i in range(len(allUserstoCheck)):
        for j in range(i, len(allUserstoCheck)):
            getIntersect(allUserstoCheck[i], allUserstoCheck[j], intersect)

    tweet = "Trending Follows:\n\n"
    index = 1

    for key in intersect:
        if len(intersect[key]) > 1:
            tweet += (
                str(index) + ") " + str(key) + " x " + str(len(intersect[key])) + ":\n"
            )
            for i in range(len(intersect[key])):
                tweet += str(intersect[key][i])
                if i != len(intersect[key]) - 1:
                    tweet += ", "
            tweet += "\n\n"
            index += 1

    return tweet


print(
    twit(
        [
            {"username": "ASvanevik"},
            {"username": "cobie"},
            {"username": "pythianism"},
            {"username": "Pentosh1"},
            {"username": "_Checkmatey_"},
            {"username": "CanteringClark"},
        ]
    )
)
