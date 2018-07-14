from mod import Mod
import requests
import os
from datetime import datetime


class Habitica(Mod):
    def __init__(self):
        super(Habitica, self).__init__()
        self.env_path = os.path.join('./', '.hab')
        self.load_env()
        self.uuid = os.getenv("HABITICA_UUID")
        self.token = os.getenv("HABITICA_TOKEN")
        assert type(self.uuid) == str and type(
            self.token) == str, "Habitica id or token env not set!"

        self.prefix = "habitica_tasks_"

    def get_tasks(self, time_start):
        time_last_look_up = self.update_look_up_time(
            "HABITICA_LAST_LOOK_UP")[0]
        time_start_str = time_start.strftime("%Y-%m-%dT%H:%M:%SZ")
        response = requests.get("https://habitica.com/api/v3/tasks/user",
                                params={
                                    # "type": "todos",
                                    # "dueDate": "7"
                                },
                                headers={
                                    "Content-Type": "application/json",
                                    "x-api-user": self.uuid,
                                    "x-api-key": self.token
                                })
        # print(type(response.json()))
        assert response.status_code == 200, response.text
        response = response.json()
        assert response["success"]
        return time_start_str, response, time_last_look_up

    def score_task(self, _id):
        response = requests.post(
            "https://habitica.com/api/v3/tasks/%s/score/up"
            % _id,
            headers={
                "Content-Type": "application/json",
                "x-api-user": self.uuid,
                "x-api-key": self.token
            })
        # print(type(response.json()))
        # assert response.status_code == 200, response.text
        response = response.json()

        return response

    def score_checklist_item(self, taskid, itemid):
        response = requests.post(
            "https://habitica.com/api/v3/tasks/%s/checklist/%s/score" % (
                taskid, itemid),
            headers={
                "Content-Type": "application/json",
                "x-api-user": self.uuid,
                "x-api-key": self.token
            })
        assert response.status_code == 200, response.text
        response = response.json()

        return response

    def filter_todos_due_in(self, data, time_start, days=14):
        todos = self.filter_tasks(data, ("todos"))
        todos_due_in = []
        for todo in todos:
            try:
                time_due_str = todo["date"]
            except KeyError:
                # that means it's an todo without due time,
                # therefore no need to add to pomotodo
                continue
            try:
                time_due = datetime.strptime(time_due_str, self.timeformat)
            except:
                time_due = datetime.strptime(time_due_str, self.timeformat_hab)

            time_to_due = time_due - time_start
            if time_to_due.days < days:
                todos_due_in.append(todo)
        return tuple(todos_due_in)

    def filter_tasks(self, data, types, *discriminants):
        tasks = data["data"]
        tasks_of_type = [task for task in tasks if task["type"] in types]

        for discriminant in discriminants:
            field, condition = discriminant
            for task in tasks_of_type:
                try:
                    value = task[field]
                    discriminant = '"'+value+'"'+condition
                    if not eval(discriminant):
                        tasks_of_type.remove(task)
                except KeyError:
                    print("Invalid filed '%s" % field,
                          "' given in condition filter")
                    continue

        return tuple(tasks_of_type)


def main():
    pass

if __name__ == '__main__':
    main()
