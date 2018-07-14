import os
import json
import dotenv
from datetime import datetime


class Mod(object):

    def __init__(self):

        self.env_path = './'
        self.timeformat = "%Y-%m-%dT%H:%M:%SZ"
        self.timeformat_hab = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.path = "./data/"

    def load_env(self):
        dotenv.load_dotenv(dotenv_path=self.env_path)

    def set_env(self, key_to, value_to):
        dotenv.set_key(self.env_path, key_to, value_to)

    def load_habitodos(self, name='habitodos'):
        try:
            with open(self.path+name+".json", 'r') as f:
                dict_Obj = f.read()
            habitodos = json.loads(dict_Obj)
        except FileNotFoundError:
            with open(self.path+name+".json", 'x') as f:
                pass
            habitodos = []

        return habitodos

    def dump_habitodos(self, jsondata, name='habitodos'):
        try:
            f = open(self.path+name+".json", 'w')
        except FileNotFoundError:
            f = open(self.path+name+".json", 'x')
        dict_Obj = json.dumps(jsondata)
        f.write(dict_Obj)
        f.close()

        return dict_Obj

    def time_today_at(self, hour=3):
        time_now = datetime.now()
        time_today_at = datetime(
            year=time_now.year,
            month=time_now.month,
            day=time_now.day,
            hour=hour,
            minute=0)
        time_today_at_stamp = time_today_at.timestamp()
        time_today_at_utc = datetime.utcfromtimestamp(time_today_at_stamp)
        return time_today_at_utc

    def update_look_up_time(self, env):
        # update the env that record the last look-up time

        time_last_look_up_str = os.getenv(env)
        if not time_last_look_up_str:
            time_last_look_up_str = "1970-01-01T00:00:00Z"

        time_last_look_up = datetime.strptime(
            time_last_look_up_str, self.timeformat)

        # time_start = time_last_look_up

        time_last_look_up_str = time_last_look_up.strftime(self.timeformat)

        time_now = datetime.utcnow()
        time_now_str = time_now.strftime(self.timeformat)
        self.set_env(env, time_now_str)

        time_start_str = time_now_str

        return time_last_look_up, time_last_look_up_str, time_now, time_now_str

    def store_json(self, time_str, todos):
        try:
            with open('%s%s%s.json' % (self.path, self.prefix, time_str),
                      "x") as f:
                # for todo in todos:
                todoObj = json.dumps(todos)
                f.write(todoObj)
        except FileExistsError:
            pass

    def delete_old_files(self, time_start_str, days_keep):
        import re
        files_todo = os.listdir(self.path)

        time_start = datetime.strptime(time_start_str, self.timeformat)

        for file_todo in (f for f in files_todo if self.prefix in f):
            pattern = r"%s(.*)\.json" % re.escape(self.prefix)
            time_str = re.match(pattern, file_todo).group(1)
            time_created = datetime.strptime(time_str, self.timeformat)
            if 7000 > (time_start - time_created).days > days_keep:
                path_file_todo = os.path.join(path, file_todo)
                os.remove(path_file_todo)
                print("Removed %s%s" % (self.path, file_todo))


def main():
    pass

if __name__ == '__main__':
    main()
