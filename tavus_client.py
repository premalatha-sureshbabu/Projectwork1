import requests

class TavusClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://tavusapi.com/v2/videos"

    def create_video(self, script, replica_id):
        payload = {"replica_id": replica_id, "script": script}
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        response = requests.post(self.base_url, json=payload, headers=headers)
        data = response.json()
        if data.get("status") == "queued":
            return data.get("video_id")
        raise Exception(f"Video creation failed: {data}")

    def get_video_status(self, video_id):
        headers = {"x-api-key": self.api_key}
        url = f"{self.base_url}/{video_id}"
        response = requests.get(url, headers=headers)
        return response.json()
