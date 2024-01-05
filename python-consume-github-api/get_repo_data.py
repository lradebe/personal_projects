import requests
import os
import re


def needs_token(url):
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        return requests.get(url)
    return requests.get(url, headers={"Authorization": f"Token {TOKEN}"})


def get_last_page_number(pulls_url):
    pulls = needs_token(f"{pulls_url}?state=all&per_page=50")
    link = pulls.headers.get("link", None)
    if link is None:
        return 1
    pages = re.findall("page=(\\d{1,}>)", link)
    return int(pages[1][:-1])


def make_repo_set(pulls, start_date, end_date):
    repo_set = set()
    for pull in pulls:
        created_at_timeframe = start_date <= pull["created_at"][:10] <= end_date
        updated_at_timeframe = start_date <= pull["updated_at"][:10] <= end_date
        merged_at_timeframe = (
            pull["merged_at"] != None
            and start_date <= pull["merged_at"][:10] <= end_date
        )
        closed_at_timeframe = (
            pull["closed_at"] != None
            and start_date <= pull["closed_at"][:10] <= end_date
        )

        if (
            created_at_timeframe
            or updated_at_timeframe
            or merged_at_timeframe
            or closed_at_timeframe
        ):
            repo_data = {
                "id": pull["id"],
                "state": pull["state"],
                "title": pull["title"],
                "user": pull["user"]["login"],
                "created_at": pull["created_at"][:10],
            }
            repo_set.add(tuple(repo_data.items()))
    return repo_set


def validate_url(repo_url):
    response = needs_token(repo_url)
    if response.ok is False:
        raise NameError("Error 404 User or Repo Not Found")
    return response


def get_pull_requests(owner, repo_name, start_date, end_date):
    """Please setup an environment variable named 'TOKEN' and its value should be your Github access token.
If you don't have a Github acces token, see:
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

To set up an environment variable, you open your terminal then type the following command:

$ export TOKEN=Value

For more on this, visit: http://syllabus.africacode.net/topics/linux/os-environmental-variables/"""

    repo_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = validate_url(repo_url)
    pulls_url = response.json()["pulls_url"][:-9]
    last_page = get_last_page_number(pulls_url)
    repo_set = set()

    for page_no in range(1, last_page + 1):
        pulls = needs_token(f"{pulls_url}?state=all&per_page=50&page={page_no}").json()
        repo_set.update(make_repo_set(pulls, start_date, end_date))
    repo_data_list = [dict(tup) for tup in repo_set]
    return repo_data_list


if __name__ == "__main__":
#    print(len(get_pull_requests("Umuzi-org", "ACN-syllabus", "2022-03-01", "2022-03-10")))
    print(get_pull_requests("Umuzi-org", "Lwazi-Radebe-186-consume-github-api-python", "2022-01-01", "2022-08-25"))
#    print(get_pull_requests("Umuzi-org", "Lwazi-Radebe-625-validate-a-south-african-id-number-python", "2022-01-01", "2022-11-08"))
