# coding=utf-8
from .fetch import Session
from .groups import Group
from .users import _get_user, _get_users


class Api(object):
    def __init__(self, access_token=None):
        self.session = Session(access_token)

    def get_user(self, user_id):
        return _get_user(self.session, user_id)

    def get_users(self, user_ids):
        return _get_users(self.session, user_ids)

    def get_group(self, group_id):
        return Group._get_group(self.session, group_id)

    def get_groups(self, group_ids):
        return Group._get_groups(self.session, group_ids)
