from pomotodo import Pomotodo
from habitica import Habitica
import sys
import json
from datetime import datetime


def habitica_to_pomotodo(hab, pt, start_hour=6, days=14,
                         store=True, delete=True, keep=7):
    time_start_str, response, time_last_look_up = hab.get_tasks(
        datetime.utcnow())
    assert response["success"], "Retriving data from habitica failed: " + \
        response["message"]

    time_start = datetime.utcnow()
    time_start_str = time_start.strftime(hab.timeformat)

    if delete:
        hab.delete_old_files(time_start_str, keep)
    if store:
        hab.store_json(time_start_str, response)

    tasks = (
        hab.filter_tasks(response, ("daily"),
                         ('frequency', "in ('daily', 'weekly')")
                         ) +
        hab.filter_todos_due_in(response, time_start, days))

    habitodos = pt.load_habitodos()

    for task in tasks:

        time_create = datetime.strptime(task["createdAt"], hab.timeformat_hab)
        time_update = datetime.strptime(task["updatedAt"], hab.timeformat_hab)

        try:
            frequency = task["frequency"]
        except:
            frequency = None

        if time_update > time_last_look_up:
            checklist = task["checklist"]
            taskid = task["id"]

            # * transport new tasks
            if time_create > time_last_look_up:
                # add todo to pomotodo service
                todo_added = pt.add_todo(
                    description=task["text"],
                    notice=task["notes"],
                    frequency=frequency)

                todoid = todo_added["uuid"]
                # print(todoid)
                habitodo = {
                    "taskid": taskid,
                    "todoid": todoid,
                    "subs": [
                    ]
                }

                for item in checklist:
                    # create subtodo in pomotodo
                    subtodo_added = pt.add_subtodo(
                        todoid, item["text"])

                    itemid = item["id"]
                    subtodoid = subtodo_added["uuid"]

                    habitodo_sub = {
                        "itemid": itemid,
                        "subtodoid": subtodoid
                    }
                    habitodo["subs"].append(habitodo_sub)

            # * update existing tasks
            else:
                # pop the original habitodo from list for updating later
                for habitodo in habitodos:
                    if habitodo["taskid"] == taskid:
                        habitodos.remove(habitodo)
                        break

                todoid = habitodo["todoid"]
                subs = habitodo["subs"]

                response = pt.edit_todo(todoid, task["text"])
                try:
                    todoid = response["uuid"]
                except KeyError:
                    print("task '%s" % task["text"],
                          "' not found in local file, ",
                          "try to add/update it manually")

                for item in checklist:
                    found = False
                    for sub in subs:
                        if item["id"] == sub["itemid"]:
                            # that's an existing subtodo, update it anyhow
                            found = True
                            subtodoid = sub["subtodoid"]
                            response = pt.edit_subtodo(
                                todoid, subtodoid, item["text"])
                            try:
                                todoid = response["uuid"]
                            except KeyError:
                                print("checklist item '%s" % item["text"],
                                      "' not found in local file, ",
                                      "try to add/update it manually")
                            break
                    if found:
                        continue

                    # that's a new subtodo, add it to pomotodo
                    subtodo_added = pt.add_subtodo(
                        todoid, item["text"])

                    itemid = item["id"]
                    subtodoid = subtodo_added["uuid"]
                    habitodo_sub_new = {
                        "itemid": itemid, "subtodoid": subtodoid}
                    habitodo["subs"].append(habitodo_sub_new)

            habitodos.append(habitodo)

    pt.dump_habitodos(habitodos)


def pomotodo_to_habitica(pt, hab, start_hour=3,
                         store=True, delete=True, keep=7):
    time_start_str, c_todos = pt.get_todos(completed_after=True)
    assert 'errors' not in c_todos, c_todos['description']
    if store:
        pt.store_json(time_start_str, c_todos)

    time_start_str, u_todos = pt.get_todos(completed=False)
    assert 'errors' not in u_todos, u_todos['description']
    if store:
        pt.store_json(time_start_str, u_todos)

    if delete:
        pt.delete_old_files(time_start_str, keep)

    habitodos = pt.load_habitodos()

    todos = c_todos + u_todos
    for todo in todos:
        todoid = todo["uuid"]
        found = False
        for habitodo in habitodos:
            if habitodo["todoid"] == todoid:
                found = True
                break

        if not found:
            if todo["completed"]:
                print("Comepleted todo: ", todo["description"],
                      " didn't get scored in habitica automatically")
            else:
                print("Completed subtodos under todo: ", todo["description"],
                      " didn't get scored in habitica automatically")
            continue

        taskid = habitodo["taskid"]
        repeat_type = todo["repeat_type"]
        if todo["completed"]:
            hab.score_task(taskid)
            if repeat_type == "none":
                habitodos.remove(habitodo)
        else:
            subs = habitodo["subs"]
            subtodos = pt.get_subtodos(todoid)
            for subtodo in (s for s in subtodos if s["completed"]):
                subtodoid = subtodo["uuid"]
                for sub in subs:
                    if sub["subtodoid"] == subtodoid:
                        itemid = sub["itemid"]
                        hab.score_checklist_item(taskid, itemid)
                        if repeat_type == "none":
                            subs.remove(sub)

    pt.dump_habitodos(habitodos)


def main():
    pt = Pomotodo()
    hab = Habitica()

    action = sys.argv[1]
    if action == "htp":
        habitica_to_pomotodo(hab, pt)
    elif action == "pth":
        pomotodo_to_habitica(pt, hab)
    else:
        print("action '%s" % action, "' not supported")
        exit()

if __name__ == '__main__':
    main()
