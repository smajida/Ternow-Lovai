# coding=utf-8

# Credit to
# Seyed Majid Azimi
# 24.03.2018

import json

import requests

headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
}

host = 'https://api.gotinder.com'

def get_auth_token(fb_auth_token, fb_user_id, host):
    if "error" in fb_auth_token:
        return {"error": "could not retrieve fb_auth_token"}
    if "error" in fb_user_id:
        return {"error": "could not retrieve fb_user_id"}
    url = host + '/auth'
    req = requests.post(url,
                        headers=headers,
                        data=json.dumps(
                            {'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
                        )
    try:
        tinder_auth_token = req.json()["token"]
        headers.update({"X-Auth-Token": tinder_auth_token})
        print("You have been successfully authorized!")
        return tinder_auth_token
    except Exception as e:
        print(e)
        return {"error": "Something went wrong. Sorry, but we could not authorize you."}


def authverif(fb_access_token, fb_user_id, host):
    res = get_auth_token(fb_access_token, fb_user_id, host)
    if "error" in res:
        return False
    return True


def get_recommendations():
    try:
        r = requests.get('https://api.gotinder.com/user/recs', headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting recomendations:", e)


def get_updates(host, last_activity_date=""):

    try:
        url = host + '/updates'
        r = requests.post(url,
                          headers=headers,
                          data=json.dumps({"last_activity_date": last_activity_date}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting updates:", e)


def get_self(host):
    '''
    Returns your own profile data
    '''
    try:
        url = host + '/profile'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your data:", e)


def change_preferences(**kwargs):
    '''
    ex: change_preferences(age_filter_min=30, gender=0)
    kwargs: a dictionary - whose keys become separate keyword arguments and the values become values of these arguments
    age_filter_min: 18..46
    age_filter_max: 22..55
    age_filter_min <= age_filter_max - 4
    gender: 0 == seeking males, 1 == seeking females
    distance_filter: 1..100
    discoverable: true | false
    {"photo_optimizer_enabled":false}
    '''
    try:
        url = host + '/profile'
        r = requests.post(url, headers=headers, data=json.dumps(kwargs))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not change your preferences:", e)


def get_meta():
    try:
        url = host + '/meta'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your metadata:", e)

def update_location(lat, lon):
    '''
    Updates your location to the given float inputs
    Note: Requires a passport / Tinder Plus
    '''
    try:
        url = host + '/passport/user/travel'
        r = requests.post(url, headers=headers, data=json.dumps({"lat": lat, "lon": lon}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)

def reset_real_location():
    try:
        url = host + '/passport/user/reset'
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)


def get_recs_v2():
    '''
    This works more consistently then the normal get_recommendations becuase it seeems to check new location
    '''
    try:
        url = host + '/v2/recs/core?locale=en-US'
        r = requests.get(url, headers=headers)
        return r.json()
    except Exception as e:
        print('excepted')

def set_webprofileusername(username):
    '''
    Sets the username for the webprofile: https://www.gotinder.com/@YOURUSERNAME
    '''
    try:
        url = host + '/profile/username'
        r = requests.put(url, headers=headers, 
                         data=json.dumps({"username": username}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not set webprofile username:", e)

def reset_webprofileusername(username):
    '''
    Resets the username for the webprofile
    '''
    try:
        url = host + '/profile/username'
        r = requests.delete(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not delete webprofile username:", e)        
        
def get_person(id):
    '''
    Gets a user's profile via their id
    '''
    try:
        url = host + '/user/%s' % id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get that person:", e)


def send_msg(match_id, msg):
    try:
        url = host + '/user/matches/%s' % match_id
        r = requests.post(url, headers=headers,
                          data=json.dumps({"message": msg}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not send your message:", e)


def superlike(person_id):
    try:
        url = host + '/like/%s/super' % person_id
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not superlike:", e)


def like(person_id):
    try:
        url = host + '/like/%s' % person_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not like:", e)


def dislike(person_id):
    try:
        url = host + '/pass/%s' % person_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not dislike:", e)


def report(person_id, cause, explanation=''):
    '''
    There are three options for cause:
        0 : Other and requires an explanation
        1 : Feels like spam and no explanation
        4 : Inappropriate Photos and no explanation
    '''
    try:
        url = host + '/report/%s' % person_id
        r = requests.post(url, headers=headers, data={
                          "cause": cause, "text": explanation})
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not report:", e)


def match_info(match_id):
    try:
        url = host + '/matches/%s' % match_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)


# def see_friends():
#     try:
#         url = host + '/group/friends'
#         r = requests.get(url, headers=headers)
#         return r.json()['results']
#     except requests.exceptions.RequestException as e:
#         print("Something went wrong. Could not get your Facebook friends:", e)
