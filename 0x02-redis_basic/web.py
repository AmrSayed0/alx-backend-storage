#!/usr/bin/env python3
"""Module for implementing a simple Redis caching system"""
from typing import Callable
from functools import wraps
import redis
import requests

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def url_count(method: Callable) -> Callable:
    """Counts how many times a URL is called"""

    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_key = f'count:{url}'
        redis_value = redis_client.get(redis_key)

        if redis_value:
            return redis_value.decode('utf-8')

        response = method(url)
        redis_client.incr(redis_key)
        redis_client.setex(redis_key, 10, response)

        return response

    return wrapper


@url_count
def get_page(url: str) -> str:
    """Gets the HTML content of a web page"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad requests
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk'))
