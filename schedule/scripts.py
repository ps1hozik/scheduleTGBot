import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../database"))
from config import get_database


dbname = get_database()
collection_user = dbname["users"]


def get_one_day(user_id: int, date: str):
    user = collection_user.find_one({"user_id": user_id})
    group = user["group"]
    facultie = user["facultie"]
    collection_schedule = dbname[f"ТЕСТ Расписание {facultie}"]
    schedule = collection_schedule.find_one({"group_name": group})["schedule"]
    for item in schedule:
        if item["date"] == date:
            return print_lessons(item["lessons"], item["day"], item["date"])
    return None


def get_all(user_id: int):
    user = collection_user.find_one({"user_id": user_id})
    group = user["group"]
    facultie = user["facultie"]
    collection_schedule = dbname[f"ТЕСТ Расписание {facultie}"]
    schedule: list = collection_schedule.find_one({"group_name": group})["schedule"]
    sch = []
    if schedule:
        if schedule[0]["day"] == "Суббота":
            del schedule[0]
        for item in schedule:
            sch.append(print_lessons(item["lessons"], item["day"], item["date"]))
    return sch


def print_lessons(lessons: list, day: str, date: str):
    while lessons and lessons[-1]["lesson"] is None:
        lessons.pop()
    space = "⠀" * 2
    date = date[5:][3:] + "." + date[5:][:2]
    f_lessons = f"<b><u>{day} ({date})</u></b>\n\n"
    for i, v in enumerate(lessons):
        lesson_name = v["lesson"]["name"] if v["lesson"] else " "
        lesson_teacher = v["lesson"]["teacher"] if v["lesson"] else " "
        lesson_auditorium = v["lesson"]["auditorium"] if v["lesson"] else " "
        time = v["time"]
        num = v["number"]
        f_lessons += f"<i>№{num} {time}</i>\n\n"
        f_lessons += "<b>"
        f_lessons += f"{space}{lesson_name}\n" if lesson_name != " " else f"{space}\n"
        f_lessons += f"{space*2}{lesson_teacher}\n" if lesson_teacher != " " else ""
        f_lessons += (
            f"{space*2}{lesson_auditorium}\n\n"
            if lesson_auditorium != " "
            else f"{space}\n"
        )
        f_lessons += "\n</b>"
    if f_lessons != f"{day} ({date})\n\n":
        return f_lessons


def get_groups(facultie: str, course: int):
    collection_group = dbname[f"ТЕСТ Группы {facultie}"]
    cursor = collection_group.find({"course": str(course)}).sort("_id", 1)
    return [doc["group_name"] for doc in cursor]


def get_subgroups(facultie: str, group: str):
    collection_group = dbname[f"ТЕСТ Группы {facultie}"]
    return collection_group.find_one({"group_name": group})["sub_groups"]
