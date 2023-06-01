import requests
import json


def getLevelCnt(cookie):

    cntLst = dict({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0})

    url = f'https://school.programmers.co.kr/api/v1/school/challenges/?perPage=20&statuses[]=solved'
    cookies = {'_programmers_session_production': cookie}

    totalPages = int(json.loads(requests.get(url, cookies=cookies).text)['totalPages'])

    for i in range(totalPages):

        url = f'https://school.programmers.co.kr/api/v1/school/challenges/?perPage=20&statuses[]=solved&order=recent&page={i + 1}'

        request = requests.get(url, cookies=cookies)
        req = json.loads(request.text)

        if request.status_code == requests.codes.ok:

            for j in list(map(dict, req['result'])):
                cntLst[j['level']] += 1

    return cntLst


def getUsers(cookie):
    url = r'https://school.programmers.co.kr/api/v1/school/challenges/users/'
    cookies = {'_programmers_session_production': cookie}

    response = dict(json.loads(requests.get(url, cookies=cookies).text))

    response['solved_challenges_count'] = response.pop('solvedChallengesCount')

    return response
