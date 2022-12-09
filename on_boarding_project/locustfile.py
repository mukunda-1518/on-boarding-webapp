from locust import Locust, HttpLocust, TaskSet, task, between
import json
import structlog

log = structlog.getLogger(__name__)

class UserBehavior(TaskSet):
    access_token = ""

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post("api/v1/user/login/", json={"username":"Merchant", "password":"admin1234"})
        response = response.json()
        self.access_token = response['access_token']

    @task
    def get_stores(self):
        self.client.get("api/v1/get_stores/", headers={"Authorization": "Bearer " + self.access_token})
        log.info("fetched_all_store_details")

    @task
    def get_store_details(self):
        for i in range(20, 30):
            self.client.get("api/v1/get_stores/{}/".format(i), headers={"Authorization": "Bearer " + self.access_token})
            log.info("fetched_details_of_store_id", store_id=i)

    @task
    def get_orders(self):
        self.client.get("api/v1/order/", headers={"Authorization": "Bearer " + self.access_token})
        log.info("fetched_all_order_details")

    @task
    def get_order_details(self):

        for i in range(30, 40):
            self.client.get("api/v1/order/{}/".format(i), headers={"Authorization": "Bearer " + self.access_token})
            log.info("fetched_details_of_order_id", order_id=i)

    @task
    def create_store(self):
        store = {
            "name": "Store",
            "city": "City",
            "address": "Address",
            "lat": 2.345,
            "lon": 45.678
        }
        self.client.post("api/v1/create_store/", json=store, headers={"Authorization": "Bearer " + self.access_token})
        log.info("created_new_store")

    
    @task
    def create_order(self):
        request_body = {
            "item_ids": [6, 7, 10, 11, 12, 13, 14, 15, 16],
            "store_id": 10
        }
        self.client.post("api/v1/order/", json=request_body, headers={"Authorization": "Bearer " + self.access_token})
        log.info("created_new_order")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(2, 5)



