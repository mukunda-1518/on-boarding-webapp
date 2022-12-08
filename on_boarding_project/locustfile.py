from locust import Locust, HttpLocust, TaskSet, task, between
import json

class UserBehavior(TaskSet):
    access_token = ""

    def on_start(self):
        response = self.client.post("api/v1/user/login/", json={"username":"Merchant", "password":"admin1234"})
        response = response.json()
        self.access_token = response['access_token']


    @task
    def create_store(self):
        store = {
            "name": "Store",
            "city": "City",
            "address": "Address",
            "lat": 2.345,
            "lon": 45.678
        }
        response = self.client.post("api/v1/create_store/", json=store, headers={"Authorization": "Bearer " + self.access_token})
        print("New store created")
        
    
    @task
    def get_stores(self):
        response = self.client.get("api/v1/get_stores/", headers={"Authorization": "Bearer " + self.access_token})
        print("Got all store details")
        # response = response.json()
        # print(response['stores'])

    
    @task
    def get_store_details(self):
        for i in range(20, 30):
            response = self.client.get("api/v1/get_stores/{}/".format(i), headers={"Authorization": "Bearer " + self.access_token})
            print("Fetched deatils of store_id:{}".format(i))

    
    @task
    def create_order(self):
        request_body = {
            "item_ids": [6, 7, 10, 11, 12, 13, 14, 15, 16],
            "store_id": 10
        }
        response = self.client.post("api/v1/order/", json=request_body, headers={"Authorization": "Bearer " + self.access_token})
        print("order_created id")
    

    @task
    def get_order_details(self):

        for i in range(30, 40):
            response = self.client.get("api/v1/order/{}/".format(i), headers={"Authorization": "Bearer " + self.access_token})
            # print(response.json())
            print("Fetched deatils of order_id:{}".format(i))

    @task
    def get_orders(self):
        response = self.client.get("api/v1/order/", headers={"Authorization": "Bearer " + self.access_token})
        print("Fetched all order details")

    

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(2, 5)



