""" Import required libraries """
import json
import requests

URL = "https://api.bitbucket.org/2.0/repositories/{team}/{repo_name}"


def main(username, password, team, repo_name):
    """ Create a new repository. """

    response = {
        "code": 400,
        "type": "error"
    }

    headers = {"Content-Type": "application/json"}

    data = {
        "scm": "git",
        "is_private": "true",
        "fork_policy": "no_public_forks"
    }

    try:
        result = requests.post(
            URL.format(team=team, repo_name=repo_name),
            auth=(username, password),
            data=json.dumps(data),
            headers=headers)

        status_code = result.status_code

        result = json.loads(result.text)

        if status_code == 200:
            if "error" in result:
                response["error"] = result["error"]["message"]
            else:
                response["type"] = "success"
                response["data"] = result
        else:
            response["error"] = result["error"]["message"]

        response["code"] = status_code
    except requests.exceptions.HTTPError as err:
        response["code"] = 500
        response["error"] = {
            "message": "Failed to connect."
        }
    except Exception, err:
        response["code"] = 500
        response["error"] = {
            "message": str(err)
        }

    return response
