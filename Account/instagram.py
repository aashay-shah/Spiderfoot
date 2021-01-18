import requests

def get_possible_accounts(name):
    r = requests.get(
        "https://www.instagram.com/web/search/topsearch/?context=blended&query="
        + name
        + "&include_reel=true"
    )
    results = r.json()
    data = list()
    for x in results['users']:
        data.append({'username': x['user']['username'],
                     'name': x['user']['full_name'],
                     'image': x['user']['profile_pic_url'],
                     'is_private': x['user']['is_private']
                     })
    return data

def instagram(name: str):
    """
    name: Pass anything -> username, first name, last name, full name
    Results: The insta name, id, profile_pic, is_private
    """
    results = get_possible_accounts(name)
    return results
