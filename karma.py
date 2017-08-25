import os
import pickle

import time

user_data = {}
_karma_file = 'karma.pkl'
_file_loaded = False
_last_karma_time = {}
_time_between_karma = 60 * 30  # half an hour, in seconds


def add_karma_cmd(client, message, args):
    if not _file_loaded:
        load_karma()
    try:
        user_id = message.mentions[0].id
        user_nick = message.mentions[0].nick
        if user_nick is None:
            user_nick = message.mentions[0].name
    except:
        return ' No user specified!'
    if user_id == message.author.id:
        return "4ril??"
    if not _eligible_to_give(user_id):
        return
    _add_karma(user_id)
    return '%s has %s karma' % (user_nick, _get_karma(user_id))

def take_karma_cmd(client, message, args):
    if message.author.server.owner.top_role in message.author.roles:
        if not _file_loaded:
            load_karma()
        try:
            user_id = message.mentions[0].id
            user_nick = message.mentions[0].nick
            if user_nick is None:
                user_nick = message.mentions[0].name
        except:
            return ' No user specified!'
        if user_id == message.author.id:
            return "4ril??"
        if not _eligible_to_give(user_id):
            return
        _take_karma(user_id)
    return '%s has %s karma' % (user_nick, _get_karma(user_id))


def get_karma_cmd(client, message, args):
    if not _file_loaded:
        load_karma()
    try:
        user_id = message.mentions[0].id
        user_nick = message.mentions[0].nick
        if user_nick is None:
            user_nick = message.mentions[0].name
    except:
        return ' No user specified!'
    return '%s has %s karma' % (user_nick, _get_karma(user_id))


def _set_karma_time(user_id):
    t = int(time.time())
    _last_karma_time[user_id] = t


def _eligible_to_give(user_id):
    if user_id not in _last_karma_time:
        return True
    return (int(time.time()) - _last_karma_time[user_id]) > _time_between_karma


def _add_karma(user_id):
    if user_id not in user_data:
        user_data[user_id] = 1
    else:
        user_data[user_id] += 1
    _set_karma_time(user_id)
    save_karma()

def _take_karma(user_id):
    if user_id not in user_data:
        user_data[user_id] = -1
    else:
        user_data[user_id] -= 1
    _set_karma_time(user_id)
    save_karma()


def _dec_karma(user_id):
    if user_id not in user_data:
        user_data[user_id] = 0
    else:
        user_data[user_id] -= 1
        if user_data[user_id] < 0:
            user_data[user_id] = 0
    _set_karma_time(user_id)
    save_karma()


def _get_karma(user_id):
    if user_id not in user_data:
        return 0
    return user_data[user_id]


def load_karma():
    if os.path.isfile(_karma_file):
        with open(_karma_file, 'rb') as handle:
            global user_data
            user_data = pickle.load(handle)
    global _file_loaded
    _file_loaded = True


def save_karma():
    with open(_karma_file, 'wb') as handle:
        pickle.dump(user_data, handle, protocol=pickle.HIGHEST_PROTOCOL)