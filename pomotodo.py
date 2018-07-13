from mod import Mod
import os
import requests


class Pomotodo(Mod):
    def __init__(self):
        super(Pomotodo, self).__init__()
        self.env_path = self.env_path / ".pt"
        self.load_env()
        self.token = os.getenv("POMOTODO_TOKEN")
        assert type(self.token) == str, "POMOTODO_TOKEN env not set!"

        self.prefix = "pomotodos_completed_"

    def add_todo(self, description, notice=None, frequency=None):
        repeat_dict = {
            "daily": "each_day",
            'weekly': "each_week"
        }
        try:
            repeat_type = repeat_dict[frequency]
            repeat_tag = '#'+frequency+' '
            remind_time = 0
        except:
            repeat_type = "none"
            repeat_tag = ''
            remind_time = None

        description = repeat_tag+description
        # I don't need it, but pomotodo requires it for repeated todos

        response = requests.post("https://api.pomotodo.com/1/todos",
                                 headers={
                                     'Authorization': 'token ' + self.token
                                 },
                                 json={
                                     "description": description,
                                     'notice': notice,
                                     'repeat_type': repeat_type,
                                     'remind_time': remind_time
                                 }
                                 )
        response = response.json()
        return response

    def add_subtodo(self, parent_uuid, description):
        response = requests.post(
            "https://api.pomotodo.com/1/todos/%s/sub_todos" % parent_uuid,
            headers={
                'Authorization': 'token ' + self.token
            },
            json={
                "description": description,
            }
        )
        response = response.json()
        return response

    def edit_todo(self, uuid, description):
        # todo: eidt an todo in pomotodo if related habitica task are updated
        response = requests.patch(
            "https://api.pomotodo.com/1/todos/%s" % uuid,
            headers={
                'Authorization': 'token ' + self.token
            },
            json={
                "description": description,
            }
        )
        response = response.json()
        return response

    def edit_subtodo(self, parent_uuid, uuid, description):
        # todo: eidt an subtodo in pomotodo
        # if related habitica checklist item are updated
        response = requests.patch(
            "https://api.pomotodo.com/1/todos/%s/sub_todos/%s" % (
                parent_uuid, uuid),
            headers={
                'Authorization': 'token ' + self.token
            },
            json={
                "description": description,
                # "uuid": uuid,
                # "parent_uuid": parent_uuid
            }
        )
        response = response.json()
        return response

    def get_subtodos(self, parent_uuid, uuid=''):
        response = requests.get(
            "https://api.pomotodo.com/1/todos/%s/sub_todos/%s" % (
                parent_uuid, uuid),
            headers={'Authorization': 'token ' + self.token},
        )

        response = response.json()
        return response

    def get_todos(self, completed=True, completed_after=False):
        completed = completed_after or completed

        if completed_after:
            time_start_str = self.update_look_up_time(
                "POMOTODO_LAST_LOOK_UP")[1]
        else:
            from random import randint
            time_start_str = "1970-01-01T00:%s:%sZ" % (
                randint(0, 59), randint(0, 59))

        params = {
            'limit': 100,
            'completed_later_than': time_start_str,
            'completed': completed
        }
        if not completed_after:
            params.pop("completed_later_than")

        response = requests.get("https://api.pomotodo.com/1/todos",
                                headers={
                                    'Authorization': 'token ' + self.token},
                                params=params
                                )
        response = response.json()

        return time_start_str, response


def main():
    pass

if __name__ == '__main__':
    main()
