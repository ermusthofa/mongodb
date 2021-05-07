#!/usr/bin/python3

import json
import pymongo
import random
import copy

def mongodb_connect(client_uri):
    try:
        return pymongo.MongoClient(client_uri)
    except pymongo.errors.ConnectionFailure:
        print("Failed to connect to server {}").format(client_uri)

def render_data(data):
    return json.dumps(data)

def construct_members_object(member):
    obj = {}
    obj["id"] = member['_id']
    obj["host"] = member['host'].split('.')[0]
    obj["priority"] = member['priority']
    return obj

def randomize_priority_value(shuffled_members_object, priority_value):
    random.shuffle(priority_value)
    for i in range(len(shuffled_members_object)):
        shuffled_members_object[i]['priority'] = priority_value[i]

def main():

    client = mongodb_connect('mongodb://localhost:27017/')
    
    mongodb_conf = client.admin.command('replSetGetConfig', 1)
    members = mongodb_conf['config']['members']

    members_object = []
    priority_value = []
    for member in members:
        if not member['hidden']:
            obj = construct_members_object(member)
            members_object.append(obj)
            priority_value.append(member['priority'])

    # get the existing highest priority
    currentHighest = max(members_object, key=lambda x:x['priority'])

    # copy the existing priority status to another list
    # to be manipulated
    shuffled_members_object = copy.deepcopy(members_object)

    # keep shuffling if member still in the existing priority status
    is_equal = False
    while not is_equal:
        list_diff = [i for i in shuffled_members_object if i not in members_object]
        if len(list_diff) == 0: # zero len == nodiff
            randomize_priority_value(shuffled_members_object, priority_value)
            shuffledHighest = max(shuffled_members_object, key=lambda x:x['priority'])
            # reshuffle if current highest == shuffled highest
            if shuffledHighest['id'] == currentHighest['id']:
                randomize_priority_value(shuffled_members_object, priority_value)
        else:
            is_equal = True

    # overwrite member priority
    for i, m_val in enumerate(members):
        for s_val in shuffled_members_object:
            if m_val['_id'] == s_val['id']:
                mongodb_conf['config']['members'][i]['priority'] = s_val['priority']
                # print("mongodb_conf['config']['members'][{}]['id = {}'] = s_val[{}]".format(i, mongodb_conf['config']['members'][i]['_id'], s_val['priority']))
                # print("{} {}".format(mongodb_conf['config']['members'][i]['host'], mongodb_conf['config']['members'][i]['priority']))
    
    mongodb_conf['config']['version'] += 1
    mongodb_conf['config']['term'] += 1
    res = client.admin.command({'replSetReconfig': mongodb_conf['config']})
    print(res)

if __name__ == "__main__":
    main()