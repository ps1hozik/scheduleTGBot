import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../database"))
from config import get_database
from datetime import date, timedelta, datetime

dbname = get_database()
collection_user = dbname["users"]


def match_date(lessons_date: date):
    now = date.today()
    weekday = now.weekday()
    new_weekday = lessons_date.weekday()
    if 0 <= weekday <= 3:
        monday = now - timedelta(days=weekday)
    else:
        monday = now + timedelta(days=(7 - weekday))

    new_monday = lessons_date - timedelta(days=new_weekday)
    return monday == new_monday


def get_one_day(user_id: int, date: str):
    user = collection_user.find_one({"user_id": user_id})
    group = user["group"]
    facultie = user["facultie"]
    collection_schedule = dbname[f"Расписание {facultie}"]
    schedule = collection_schedule.find_one({"group_name": group})["schedule"]
    for item in schedule:
        if item["date"] == date:
            return formatting_lessons(item["lessons"], item["day"], item["date"])
    return None


def get_all(user_id: int):
    user = collection_user.find_one({"user_id": user_id})
    group = user["group"]
    facultie = user["facultie"]
    collection_schedule = dbname[f"Расписание {facultie}"]
    schedule: list = collection_schedule.find_one({"group_name": group})["schedule"]
    sch = []
    if schedule:
        lessons_date = schedule[-1]["date"]
        if match_date(datetime.strptime(lessons_date, "%Y-%m-%d").date()):
            if schedule[0]["day"] == "Суббота":
                del schedule[0]
            for item in schedule:
                sch.append(
                    formatting_lessons(item["lessons"], item["day"], item["date"])
                )
    return sch


def formatting_lessons(lessons: list, day: str, date: str):
    while lessons and lessons[-1]["lesson"] is None:
        lessons.pop()
    space = "⠀" * 2
    date = date[5:][3:] + "." + date[5:][:2]
    f_lessons = f"<b><u>{day} ({date})</u></b>\n\n"
    for _, v in enumerate(lessons):
        lesson_name = v["lesson"]["name"] if v["lesson"] else " "
        lesson_teacher = v["lesson"]["teacher"] if v["lesson"] else " "
        lesson_auditorium = v["lesson"]["auditorium"] if v["lesson"] else " "
        lesson_group = ": " + v["group"] if "group" in v else ""
        time = v["time"]
        num = v["number"]
        f_lessons += f"<i>№{num} {time} {lesson_group} </i> \n\n"
        f_lessons += "<b>"
        f_lessons += f"{space}{lesson_name}\n" if lesson_name != " " else ""
        f_lessons += f"{space*2}{lesson_teacher}\n" if lesson_teacher != " " else ""
        f_lessons += (
            f"{space*2}{lesson_auditorium}\n\n</b>"
            if lesson_auditorium != " "
            else "</b>"
        )
    if f_lessons != f"{day} ({date})\n\n":
        return f_lessons


def get_groups(facultie: str, course: int):
    collection_group = dbname[f"Группы {facultie}"]
    cursor = collection_group.find({"course": str(course)}).sort("_id", 1)
    return [doc["group_name"] for doc in cursor]


def get_subgroups(facultie: str, group: str):
    collection_group = dbname[f"Группы {facultie}"]
    return collection_group.find_one({"group_name": group})["sub_groups"]


def find_teacher(teacher_name: str):
    teacher_name_check = teacher_name.lower().replace(".", "").split()
    if len(teacher_name_check) > 1:
        teacher_name_check[1:] = [s[0] for s in teacher_name_check[1:]]

    teacher_name = " ".join(teacher_name_check[:3])

    db = get_database()
    collections = db.list_collection_names()
    lst = []

    for collection in collections:
        if "расписание" in collection.lower():
            collection_data = db[collection].find()

            for group in collection_data:
                for sch in group["schedule"]:
                    dt = None
                    for lesson in sch["lessons"]:
                        if lesson["lesson"] and teacher_name in " ".join(
                            lesson["lesson"]["teacher"].lower().replace(".", "").split()
                        ):
                            if dt is None:
                                dt = {
                                    "day": sch["day"],
                                    "date": sch["date"],
                                    "lessons": [],
                                }
                            if lesson not in dt["lessons"]:
                                lesson["group"] = group["group_name"]
                                dt["lessons"].append(lesson)

                    if dt:
                        found_date = False
                        for item in lst:
                            if item["date"] == dt["date"]:
                                for lesson in dt["lessons"]:
                                    found_lesson = False
                                    for existing_lesson in item["lessons"]:
                                        if (
                                            existing_lesson["lesson"]["name"]
                                            == lesson["lesson"]["name"]
                                            and existing_lesson["number"]
                                            == lesson["number"]
                                        ):

                                            existing_lesson["group"] = ", ".join(
                                                [
                                                    existing_lesson["group"],
                                                    lesson["group"],
                                                ]
                                            )
                                            found_lesson = True
                                            break
                                    if not found_lesson:
                                        item["lessons"].append(lesson)
                                found_date = True
                                break
                        if not found_date:
                            lst.append(dt)
    for item in lst:
        item["lessons"].sort(key=lambda x: x["number"])
    lst.sort(key=lambda x: x["date"])

    sch = []
    for item in lst:
        sch.append(formatting_lessons(item["lessons"], item["day"], item["date"]))
    return sch
