from rq import Retry


def retries():
     return Retry(max=5, interval=[4, 16, 64, 256, 1028])
