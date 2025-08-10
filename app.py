from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

# Replace with your actual token
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJiN2JhZmIyZjEwY2FlMmIxZjA3ZjM4MTZjNTQyMmJlY2NhNWMyMjMiLCJ0eXAiOiJKV1QifQ"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

@app.route("/")
def run_scraper():
    url = "https://hackathon.twisminds.gg/hackathon"
    response = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(response.content, "lxml")
    next_data_script = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})
    json_data = json.loads(next_data_script.string)

    page_props = json_data.get("props", {}).get("pageProps", {})
    teams = page_props.get("teams", [])
    total_participants = page_props.get('totalParticipants', [])

    all_teams = []
    for idx, team in enumerate(teams, start=1):
        team_name = team["Name"]
        team_members = []
        pending_members = []
        leader = None

        for m in team["Memberships"]:
            member_data = {
                "name": m["Name"][0],
                "handler": m["Handler"][0],
                "sector": m["Sector"]
            }
            if m["RequestStatus"] == "Approved":
                team_members.append(member_data)
            else:
                pending_members.append(member_data)
            if m.get("Role") == "Leader":
                leader = m["Name"][0]

        all_teams.append({
            "id": idx,
            "team_name": team_name,
            "leader": leader,
            "members_no": len(team_members),
            "members": team_members,
            "pending_no": len(pending_members),
            "pending_members": pending_members
        })
    hackathon_info = {
    "number of all teams": len(teams),
    "number of participants": total_participants,
    "teams": all_teams
    }

    # return jsonify(hackathon_info)
    return jsonify(hackathon_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
