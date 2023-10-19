#!/usr/bin/env python3
'''
Log stats
'''
from pymongo import MongoClient


def run():
    '''provides some stats about Nginx logs stored in MongoDB
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    print('{} logs'.format(logs_collection.count_documents({})))
    print('Methods:')
    method = {
        "GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0,
    }
    query = logs_collection.aggregate([
        {'$group': {'_id': '$method', 'count': {'$sum': 1}}}
    ])
    result = list(query)
    for x in result:
        if method.get(x['_id']) is not None:
            method[x['_id']] = x['count']
    for m in method:
        print(f'\tmethod {m}: {method[m]}')

    check_logs = list(
        logs_collection.find({'method': 'GET', 'path': '/status'}))
    print('{} status check'.format(len(check_logs)))
    print('IPs:')
    query = logs_collection.aggregate([
        {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ])
    result = list(query)
    for x in result:
        print('\t{}: {}'.format(x['_id'], x['count']))


if __name__ == '__main__':
    run()
