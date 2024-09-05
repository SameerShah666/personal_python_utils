from requests import request
import json

class User:
    def __init__(self, user_name):
        self.url = "https://www.credly.com/users/{}/badges.json".format(user_name)
        self.badges = json.dumps(self.get_badges(), indent=4)

    def get_badges(self):
        t = request(method="GET", url=self.url)
        resp = t.json()
        badges = []
        for data in resp.get("data"):
            badge = {}
            badge["badge_id"] = data.get("id")
            badge["badge_issued_on"] = data.get("issued_at_date")
            badge["badge_expires_on"] = data.get("expires_at_date")
            badge["badge_name"] = data.get("badge_template").get("name")
            badge["badge_issued_by"] = [entity.get("entity").get("name") for entity in data.get("badge_template").get("issuer").get("entities")]
            badge["badge_description"] = data.get("badge_template").get("description")
            badges.append(badge)
        return badges
    
    def display_badges(self):
        print(self.badges)
