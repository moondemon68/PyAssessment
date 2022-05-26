import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
	wait_time = between(5, 30)

	@task(1)
	def infinite_loop(self):
		self.client.post("/grade", json={
						"references": [
								"ZGVmIG1heF8zKGEsIGIsIGMpOgogICAgaWYgYSA+PSBiIGFuZCBhID49IGM6CiAgICAgICAgcmV0dXJuIGEKICAgIGVsaWYgYiA+PSBhIGFuZCBiID49IGM6CiAgICAgICAgcmV0dXJuIGIKICAgIGVsc2U6CiAgICAgICAgcmV0dXJuIGMKCgo="
						],
						"solution": "ZGVmIG1heF8zXzEyKGEsIGIsIGMpOgogICAgd2hpbGUgKFRydWUpOgogICAgICAgIGEgKz0gMQogICAgcmV0dXJuIGEK",
						"referencesFileNames": [
								"max_3.py"
						],
						"solutionFileName": "max_3_12.py",
						"timeLimit": 1000
				})
		
	@task(10)
	def compile_error(self):
		self.client.post("/grade", json={
				"references": [
						"ZGVmIG1heF8zKGEsIGIsIGMpOgogICAgaWYgYSA+PSBiIGFuZCBhID49IGM6CiAgICAgICAgcmV0dXJuIGEKICAgIGVsaWYgYiA+PSBhIGFuZCBiID49IGM6CiAgICAgICAgcmV0dXJuIGIKICAgIGVsc2U6CiAgICAgICAgcmV0dXJuIGMKCgo="
				],
				"solution": "ZGVmIG1heF8zXzEyKGEsIGIsIGMpOgogICAgd2hpbGUgKFRyc3VlKToKICAgICAgICBhICs9IDEKICAgIHJldHVybiBhCg==",
				"referencesFileNames": [
						"max_3.py"
				],
				"solutionFileName": "max_3_12.py",
				"timeLimit": 1000
		})

	@task(20)
	def normal_code(self):
		self.client.post("/grade", json={
						"references": [
								"ZGVmIG1heF8zKGEsIGIsIGMpOgogICAgaWYgYSA+PSBiIGFuZCBhID49IGM6CiAgICAgICAgcmV0dXJuIGEKICAgIGVsaWYgYiA+PSBhIGFuZCBiID49IGM6CiAgICAgICAgcmV0dXJuIGIKICAgIGVsc2U6CiAgICAgICAgcmV0dXJuIGMKCgo="
						],
						"solution": "ZGVmIG1heF8zXzEoYSwgYiwgYyk6CiAgICBpZiBhID4gYiBhbmQgYSA+IGM6CiAgICAgICAgcmV0dXJuIGEKICAgIGVsaWYgYiA+IGEgYW5kIGIgPiBjOgogICAgICAgIHJldHVybiBiCiAgICBlbHNlOgogICAgICAgIHJldHVybiBjCgo=",
						"referencesFileNames": [
								"max_3.py"
						],
						"solutionFileName": "max_3_1.py",
						"timeLimit": 1000
				})
