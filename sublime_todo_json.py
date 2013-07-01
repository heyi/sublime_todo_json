# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import json
import re
import os

class TodoFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.generate_todo_file();

    def generate_todo_file(self):
        file_name = self.window.active_view().file_name()
        if not ".json" in file_name:
            return

        todo_file = re.sub("\.json", '.todo', file_name)
        fs = open(todo_file, "w+",encoding='utf-8')

        json_data = json.load(open(file_name))
        for k in json_data:
            fs.writelines(k + ":\n")
            for item in json_data[k]:
                fs.writelines(" ☐ " + item["name"] + "\n")
            fs.writelines("\n" + "----" * 9 + "\n" * 2)
        fs.close()

        self.window.open_file(todo_file)

class TodoJsonCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.conver_todo_json();

    def conver_todo_json(self):
        file_name = self.window.active_view().file_name()
        if not ".todo" in file_name:
            return

        rom = '^\s*☐\s*(.*)$'
        rdm = '\s*\✔\s*(.+?)\s*@done?([\(\)\d\w,\.:\-/ ]*)\s*'
        rpm = '([^\b\(]*?)(?=\:)'

        json_data = {}
        json_file = re.sub("\.todo", '.json', file_name)
        project = 'other'

        with open(file_name, "r+", encoding="utf-8") as f:
            for line in f:
                prj = re.match(rpm, line)
                if prj:
                    project = prj.groups()[0]
                    json_data[project] = []
                task_open = re.match(rom, line)
                if task_open:
                    task_item = {"name": task_open.groups()[0] ,"status":0,"finish_time":""}
                    json_data[project].append(task_item)
                task_done = re.match(rdm, line)
                if task_done:
                    task_item = {"name":task_done.groups()[0],"status":1,"finish_time":task_done.groups()[1] }
                    json_data[project].append(task_item)

        with open(json_file, "w+", encoding="utf-8") as f:
            json.dump(json_data, f)

        self.window.open_file(json_file)




