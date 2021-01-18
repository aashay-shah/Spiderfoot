import requests
from datetime import datetime
from collections import Counter
import time
import json


def reddit(username: str):
    lastaction = 0
    headers = {"User-Agent": "testbot"}
    curts = int(time.time())
    commentdata = []
    linkdata = []
    timelist = []
    hourseconds = 3600
    houroffset = -7
    offset = hourseconds * houroffset

    r3 = requests.get(
        "https://www.reddit.com/user/" + username + "/about.json", headers=headers
    )

    if r3.status_code == 200:
        userdata = r3.json()["data"]

        while True:
            comurl = (
                "https://api.pushshift.io/reddit/search/comment/?author="
                + username
                + "&size=500&before="
                + str(curts)
            )
            r1 = requests.get(comurl, headers=headers)
            tempdata = r1.json()["data"]
            commentdata += tempdata
            try:
                if tempdata[499]:
                    curts = tempdata[499]["created_utc"]
            except BaseException:
                break

        # re-establish current time
        curts = int(time.time())

        # fetch posts/submissionsm
        while True:
            linkurl = (
                "https://api.pushshift.io/reddit/search/submission/?author="
                + username
                + "&size=500&before="
                + str(curts)
            )
            r2 = requests.get(linkurl, headers=headers)
            postdata = r2.json()["data"]
            linkdata += postdata
            try:
                if postdata[499]:
                    curts = postdata[499]['created_utc']
            except BaseException:
                break

        if not commentdata == []:
            # set last active time
            lastcomment = commentdata[0]["created_utc"]
            lastpost = postdata[0]["created_utc"]

            if lastcomment > lastpost:
                lastaction = lastcomment
            else:
                lastaction = lastpost
            # add all subreddits to a list
            # add all timed activities to a list
            subList = []
            for x in commentdata:
                subList.append(x["subreddit"].lower())
                timelist.append(x["created_utc"])

            for x in postdata:
                subList.append(x["subreddit"].lower())
                timelist.append(x["created_utc"])
            # adjust time for offset
            timelist = [x + offset for x in timelist]

            # and create a set for comparison purposes
            sublistset = set(subList)

        else:
            sublist = []
            sublistset = set([])

        # load subreddits from file and check them against comments
        locList = [line.rstrip("\n").lower()
                   for line in open("Account/all-locations.txt")]
        loclistset = set(locList)

        userdet = {}
        # print user data
        # print("[+] total links     : "+str(len(linkdata)))
        # print("[+] link karma      : "+str(userdata["link_karma"]))
        userdet["username"] = userdata["name"]
        userdet["createDate"] = str(
            datetime.fromtimestamp(userdata["created_utc"]))
        userdet["lastAction"] = str(datetime.fromtimestamp(lastaction))
        userdet["verifiedEmail"] = userdata["has_verified_email"]
        dict1 = {}
        if not commentdata == []:
            userdet["totalComments"] = len(commentdata)
            userdet["commentKarma"] = userdata["comment_karma"]
            userdet["locationReddits"] = list(
                sublistset.intersection(loclistset))
            # print(userdet)
            # this can be used to retrieve the comments
            # print(commentdata)
            counter = Counter(subList)
            dict1["commentdata"] = counter

        for k, v in userdet.items():
            dict1[k] = v

        # print(dict)
        data = json.dumps(dict1)
        return dict1
    else:
        return {"status": "user not found"}
