import requests
import time

def handleResponse(request):
    response = requests.get(request)
    
    print(response.status_code)
    if (response.status_code != 200):
        return None
    
    json = response.json()
    print(json['status'])
    if (json['status'] != 'OK'):
        print(json['comment'])
        return None
    
    return json

def getSubmissions(handle):
    response = handleResponse(f'https://codeforces.com/api/user.status?handle={handle}&from=1&count=10000')
    if (response is None):
        time.sleep(2)
        return getSubmissions(handle)

    return response['result']

def getProblems(tags):
    response = handleResponse(f'https://codeforces.com/api/problemset.problems?tags={tags}')
    if (response is None):
        time.sleep(2)
        return getProblems(tags)
    
    return response['result']

def fetch(startId, count, handles, ratings):
    problems = getProblems('')['problems']
    solved = []
    fetched = []

    for handle in handles:
        submissions = getSubmissions(handle)
        for submission in submissions:
            if (submission.get('verdict') == 'OK'):
                solved.append(submission['problem'])

    problems.reverse()
    for problem in problems:
        if (problem.get('contestId') is None or problem.get('contestId') < startId):
            continue  

        try:
            solved.index(problem)
            continue
        except ValueError:
            pass

        try:
            ratings.index(problem.get('rating'))
            pass
        except ValueError:
            continue

        fetched.append(problem)
        count -= 1
        if (count == 0):
            break

    return fetched
    
def getVjudgeFormat(fetched):
    ans = []
    for problem in fetched:
        ans.append('CodeForces|' + str(problem['contestId']) + str(problem['index']) + '|1|')
    return ans

def getLinks(fetched):
    ans = []
    for problem in fetched:
        ans.append('https://codeforces.com/problemset/problem/' + str(problem['contestId']) + '/' + str(problem['index']))
    return ans
    
def main():
    problems = getLinks(fetch(1800, 20, ['ahmad_salah'], [2100, 2200, 2300]))

    for problem in problems:
        print(problem)
    print(len(problems))
    
main()
