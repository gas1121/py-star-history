import random
import requests
import datetime
from star_history.auth import get_auth_data
from star_history.exceptions import (
    StarHistoryError, NoEnoughStargazorsError, ReachLimitError, ConnectionError
)


def get_star_history(user, repo_name):
    """Get given repo's star growth history.
    Use stargazers' timestamp to log star history
    Behavior differs by repo's stargazer page count:
    0< page <= 15:
        Gather all stargazers' timestamp.
    15 < page:
        Divide all pages into 15 parts and get one timestamp for each.
    """

    # add data storage to reduce github api request
    try:
        star_count = get_star_count(user, repo_name)
    except StarHistoryError:
        raise
    curr_time = datetime.datetime.now().isoformat()
    page_count = get_page_count(star_count)
    history_result = dict()
    history_result['repo_name'] = repo_name
    history_result['history_data'] = []
    headers = {'Accept': 'application/vnd.github.v3.star+json'}
    all_scanned_page_count = 15
    scan_page_data = []
    # raise exception if page<2
    if page_count < 2:
        raise NoEnoughStargazorsError
    elif page_count <= all_scanned_page_count:
        for curr_page in range(page_count):
            page_url = get_stargazers_page_url(user, repo_name, curr_page)
            scan_page_data.append((curr_page, page_url))
    else:
        step = page_count//15
        for curr_page in range(1, page_count, step):
            page_url = get_stargazers_page_url(user, repo_name, curr_page)
            scan_page_data.append((curr_page, page_url))
    for curr_page_data in scan_page_data:
        try:
            result = requests.get(curr_page_data[1], headers=headers, params=get_params())
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
            raise ConnectionError
        if result.status_code == 422:
            #422 mains page is unreachable,manually add last count
            history_result['history_data'].append({
                "date": curr_time,
                "count": star_count
            })
            break
        curr_page_stargazers = result.json()
        history_result['history_data'] += get_history_from_stargazer_data(
            curr_page_stargazers, curr_page_data[0])
    return history_result


auth_data = get_auth_data()


def get_params():
    return {
        'access_token': random.choice(auth_data['access_token'])
    }


def get_star_count(user, repo_name):
    url = "https://api.github.com/repos/{}/{}".format(user, repo_name)
    try:
        result = requests.get(url, params=get_params())
    except (requests.ConnectionError, requests.Timeout):
        raise ConnectionError
    rest_limit_count = result.headers['X-RateLimit-Remaining']
    if rest_limit_count == 0:
        raise ReachLimitError
    if result.status_code == 200:
        return result.json()["stargazers_count"]
    else:
        return -1


def get_page_count(star_count):
    stars_per_page = 30
    if star_count == 0:
        return 0
    page_count = (star_count - 1) // stars_per_page + 1
    return page_count


def get_stargazers_page_url(user, repo_name, curr_page):
    real_page = max(1, curr_page+1)
    url = 'https://api.github.com/repos/{}/{}/stargazers?page={}'.format(user, repo_name, real_page)
    return url


def get_history_from_stargazer_data(stargazers_data, curr_page):
    #TODO handle error like
    #{'documentation_url': 'https://developer.github.com/v3/#pagination', 'message': 'In order to ....'}
    result = []
    start_count = curr_page*30+1
    end_count = curr_page*30+len(stargazers_data)
    result.append({
        "date": stargazers_data[0]["starred_at"],
        "count": start_count
    })
    if start_count != end_count:
        result.append({
            "date": stargazers_data[-1]["starred_at"],
            "count": end_count
        })
    return result
