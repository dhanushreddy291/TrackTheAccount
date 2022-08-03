import requests, json, os, tweepy
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler

load_dotenv()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        auth = tweepy.OAuthHandler(
            os.getenv("consumer_key"), os.getenv("consumer_secret")
        )
        auth.set_access_token(os.getenv("access_token"), os.getenv("access_secret"))
        api = tweepy.API(auth)
        msg = self.twit(
            [
                {"name": "iamDCinvestor"},
                {"name": "j1mmyeth"},
                {"name": "DCLBlogger"},
                {"name": "Zeneca_33"},
                {"name": "NFTsAreNice"},
                {"name": "VonMises14"},
                {"name": "gmoneyNFT"},
            ]
        )
        api.update_status(status=msg)
        self.wfile.write(str(msg).encode())
        return

    def getUserID(self, userName, allUserstoCheck):
        url = "https://api.twitter.com/2/users/by/username/" + str(userName)
        payload = {}
        headers = {"Authorization": os.getenv("Bear")}
        response = requests.request("GET", url, headers=headers, data=payload)
        json_obj = json.loads(response.text)
        Id = json_obj["data"]["id"]
        return Id

    def getFollowingsByUserName(self, userName, allUserstoCheck):
        userid = self.getUserID(userName, allUserstoCheck)
        names = []

        NextToken = ""
        resp_json = self.getFollowings(userid, allUserstoCheck)
        for user in resp_json["data"]:
            names.append(user["name"])
        return names

    def getFollowings(self, userID, allUserstoCheck):
        url = (
            "https://api.twitter.com/2/users/"
            + str(userID)
            + "/following"
            + "?max_results=50"
        )
        payload = {}
        headers = {"Authorization": os.getenv("Bear")}
        response = requests.request("GET", url, headers=headers, data=payload)
        json_obj = json.loads(response.text)
        return json_obj

    def getIntersect(self, A, B, C, allUserstoCheck):
        AFoll = A["followings"]
        BFoll = B["followings"]
        for a in AFoll:
            if a in BFoll:
                if a not in C:
                    C[a] = []
                C[a].append(A["name"])
                C[a].append(B["name"])
                C[a] = list(set(C[a]))

    def twit(self, allUserstoCheck):
        for i in range(len(allUserstoCheck)):
            allUserstoCheck[i]["followings"] = self.getFollowingsByUserName(
                allUserstoCheck[i]["name"], allUserstoCheck
            )
        intersect = {}
        for i in range(len(allUserstoCheck)):
            for j in range(i, len(allUserstoCheck)):
                self.getIntersect(
                    allUserstoCheck[i], allUserstoCheck[j], intersect, allUserstoCheck
                )
        tweet = "Trending Follows:\n\n"
        index = 1

        for key in intersect:
            if len(intersect[key]) > 1:
                tweet += (
                    str(index)
                    + ") @"
                    + str(key)
                    + " x "
                    + str(len(intersect[key]))
                    + ":\n"
                )
                for i in range(len(intersect[key])):
                    tweet += "@" + str(intersect[key][i])
                    if i != len(intersect[key]) - 1:
                        tweet += ", "
                tweet += "\n\n"
                index += 1
        return tweet
