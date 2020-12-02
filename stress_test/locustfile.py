import time
from locust import HttpLocust, HttpUser, TaskSet, task


class QuickstartUser(HttpUser):

    @task(1)
    def index(self):
        self.client.get('/')

    @task(3)
    def predict(self):
       self.client.post('/predict',params={'text':'Esto es una simple prueba para evaluar el comportamiento de nuestra API'})

	def on_start(self):
	        pass
class APIUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000


