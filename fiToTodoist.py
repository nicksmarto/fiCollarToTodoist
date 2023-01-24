#!/usr/bin/python

from pytryfi import PyTryFi
import logging
from datetime import datetime
import time
import config

logpath = "fi-todo-logger.log"
logging.basicConfig(filename=logpath, filemode="a", level=logging.INFO, force=True)

tryfi = PyTryFi(config.fi_username, config.fi_password)


# Retrieve Battery Percent From Fi
batteryPercent = tryfi.pets[0]._device.batteryPercent
logging.info(
    str(datetime.fromtimestamp(time.time(), tz=None))
    + " Battery: "
    + str(batteryPercent)
)

# Updates Task Function
def updateTasks(batteryPercent):

    from todoist_api_python.api import TodoistAPI

    api = TodoistAPI(config.todoist_key)

    taskTitle = config.task_title
    taskDesc = "Current charge = " + str(batteryPercent) + "%"

    try:
        tasks = api.get_tasks()
        for task in tasks:
            if task.content.find(taskTitle) >= 0:
                print("Task Found. ID = " + task.id)
                taskID = task.id

    except Exception as error:
        print(error)

    if "taskID" in locals():
        try:
            is_success = api.update_task(task_id=task.id, description=taskDesc)
            logging.info(
                str(datetime.fromtimestamp(time.time(), tz=None)) + " Task Updated"
            )
        except Exception as error:
            print(error)
    else:
        try:
            task = api.add_task(
                content=taskTitle,
                description=taskDesc,
                due_string=config.due_string,
                due_lang="en",
                priority=config.task_priority,
                project_id=config.project_id,
            )
            logging.info(
                str(datetime.fromtimestamp(time.time(), tz=None)) + " Task Created"
            )
        except Exception as error:
            print(error)


if isinstance(batteryPercent, int):
    print("Collar battery is at " + str(batteryPercent) + "%")

    if batteryPercent < config.batteryThreshold:
        updateTasks(batteryPercent)
    else:
        logging.info(
            str(datetime.fromtimestamp(time.time(), tz=None))
            + " No action. Battery above threshold."
        )
        print("Above threshold, no action taken.")
else:
    print("Battery Percentage isn't an integer")
