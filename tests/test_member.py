import unittest
from member import Member


class TestMember(unittest.TestCase):
    def test_create_member_instance(self):
        instance = Member()
        member_list_type = type(instance.members)
        member_list_size = len(instance.members)
        assert member_list_type.__name__ == "set"
        assert member_list_size == 0

    def test_add_a_member_to_members_instance_success(self):
        instance = Member()
        instance.add("Marc")
        instance.add("Paul")
        assert instance.all() == set(["Marc", "Paul"])
