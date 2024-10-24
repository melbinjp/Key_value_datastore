from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_object(self):
        self.client.get("/api/object/some_key", headers={"Authorization": "Bearer YOUR_TOKEN_HERE"})

    @task
    def create_object(self):
        self.client.post("/api/object", json={
            "key": "another_key",
            "data": {"info": "value"},
            "ttl": 3600
        }, headers={"Authorization": "Bearer YOUR_TOKEN_HERE"})
