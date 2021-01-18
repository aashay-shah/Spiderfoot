import os
import requests

data = {}


def get_headers():
    key = ""
    if key is not None:
        headers = {"Authorization": "Bearer " + key}
        return headers
    else:
        return


def get_info_from_email(email, headers):
    global data
    r = requests.get(
        "https://api.github.com/users/" + "/search/users",
        params={"q": email},
        headers=headers,
    )
    results = r.json()

    if not results["incomplete_results"]:
        data["email"] = email
        return results["items"][0]["login"]
    return data


def get_info_from_username(username, headers):
    global data
    r = requests.get('https://api.github.com/users/' + username,
                     headers=headers)
    results = r.json()
    data['username'] = results['login']
    data['name'] = results['name']
    data['image'] = results['avatar_url']
    data['bio'] = results['bio']
    if results['email']:
        data['email'] = results['email']

    data['location'] = results['location']
    return results


def get_org_info(organizations_url, headers):
    global data
    data["organisation"] = []
    r = requests.get(organizations_url, headers=headers)
    for org in r.json():
        org_details = {}
        org_details['image'] = org['avatar_url']
        org_details['name'] = org['login']
        org_details['bio'] = org['description']
        org_details['url'] = 'https:github.com/' + org['login']
        data['organisation'].append(org_details)
    return


def get_followers_info(followers, headers):
    global data
    data['followers'] = followers
    data['followers_data'] = []
    r = requests.get('https://api.github.com/users/' +
                     data['username'] + '/followers',
                     headers=headers)
    for follower in r.json():
        follower_details = {}
        follower_details['username'] = follower['login']
        follower_details['profile_image'] = follower['avatar_url']
        follower_details['url'] = 'https:github.com/' + follower['login']
        data['followers_data'].append(follower_details)
    return


def get_following_info(following, headers):
    global data
    data['following'] = following
    data['following_data'] = []
    r = requests.get('https://api.github.com/users/' +
                     data['username'] + '/following',
                     headers=headers)
    for following in r.json():
        following_details = {}
        following_details['username'] = following['login']
        following_details['profile_image'] = following['avatar_url']
        following_details['url'] = 'https:github.com/' + following['login']
        data['following_data'].append(following_details)
    return


def get_repos_info(repos_url, headers):
    global data
    data["repos"] = []
    r = requests.get(repos_url, headers=headers)
    for repo in r.json():
        repo_data = {}
        repo_data["description"] = repo["description"]
        repo_data["name"] = repo["name"]
        repo_data["url"] = repo["html_url"]
        repo_data["forked"] = repo["fork"]
        data["repos"].append(repo_data)
    return


def get_commit_history(headers):
    global data
    for repo in data['repos']:
        x = repo['name']
        r = requests.get('https://api.github.com/repos/' +
                         data['username'] + '/' + x + '/commits',
                         headers=headers)
        commit_response = r.json()
        commits = []
        try:
            for i in commit_response:
                commit = {}
                commit["commit"] = i.get("commit").get("author")
                commit["message"] = i.get("commit").get("message")
                commits.append(commit)

            data['commit_history'][x] = commits
        except Exception:
            continue
    return


def get_info(results, headers):
    global data
    get_org_info(results["organizations_url"], headers)
    get_followers_info(results["followers"], headers)
    get_following_info(results["following"], headers)
    get_repos_info(results["repos_url"], headers)
    get_commit_history(headers)
    return


def github(username: str):
    global data
    headers = get_headers()
    if headers is None:
        return

    results = get_info_from_username(username, headers)
    get_info(results, headers)
    return data
