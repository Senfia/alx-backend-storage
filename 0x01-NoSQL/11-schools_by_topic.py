#!/usr/bin/env python3
'''Module to return the list of schools having a specific topic
'''


def schools_by_topic(mongo_collection, topic):
    '''returns the list of schools having a specific topic.
    '''
    filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(filter)]
