import requests
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("API_NLP")


def get_status(task_id):
    return requests.get(f"{URL}nlp/{task_id}/status").json()['status']


def get_result(task_id):
    return requests.get(f"{URL}nlp/{task_id}/result").json()['result']


def post_lemmas(text):
    return requests.post(f"{URL}nlp/lemmas", json={"text": text}).json()


def post_nlp(text):
    return requests.post(f"{URL}nlp/", json={"text": text}).json()
