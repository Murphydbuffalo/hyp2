from rq import Retry


def retries(max=5, interval=[4, 16, 64, 256, 1028]):
     return Retry(max=max, interval=interval)
