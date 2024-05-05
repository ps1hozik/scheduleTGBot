import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import logging
import shutil


def print_error(error):
    print(error)
    logging.error(error)


def get_start_of_weekday():
    now = datetime.now()
    weekday = now.weekday()
    if 0 <= weekday <= 3:
        monday = now - timedelta(days=weekday)
    else:
        monday = now + timedelta(days=(7 - weekday))

    return monday.date().strftime("%d.%m").split(".")


def find_faculties():
    try:
        url = "https://vsu.by/studentam/raspisanie-zanyatij.html"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        links = []
        links_text = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if (
                href
                and "/universitet/fakultety" in href
                and "/raspisanie.html" in href
                and "obucheniya-inostrannykh-grazhdan" not in href
            ):
                links_text.append(link.text)
                links.append(href)
        return links, links_text
    except Exception as exc:
        error = f"find_faculties: {exc}"
        print_error(error)
        exit(0)


def find_schedules(faculty_url, monday):
    try:
        url = f"https://vsu.by{faculty_url}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        links = []
        links_text = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if (
                href
                and (".xls" in link.text or ".xls" in href)
                and "Расписание" in link.text
                and (
                    ".".join(monday) in link.text
                    or f"{monday[0]}.{monday[1]}" in link.text
                    or f"{monday[0]}.{monday[1][1]}" in link.text
                    or f"{monday[0][1]}.{monday[1][1]}" in link.text
                    or f"{monday[0][1]}.{monday[1]}" in link.text
                )
                and "ЗФПО" not in href
                and "ЗФО" not in href
                and "зф" not in href
                and "зач" not in link.text
                and "экзаменов" not in link.text
                and " к " not in link.text
            ):
                links_text.append(link.text)
                links.append(href)
        logging.info(links)
        return links, links_text
    except Exception as exc:
        error = f"find_schedules: {exc}"
        print_error(error)
        exit(0)


def download_schedule(link, faculty_name, schedule_name):
    try:
        url = f"https://vsu.by{link}"
        response = requests.get(url, allow_redirects=True)
        with open(f"data\\{faculty_name}\\{schedule_name}.xlsx", "wb") as f:
            f.write(response.content)
    except Exception as exc:
        error = f"download_schedule: {exc}"
        print_error(error)


def download():
    try:
        shutil.rmtree("data")
        os.mkdir("data")
        monday = get_start_of_weekday()
        faculties_links, faculties_name = find_faculties()

        for faculty_url, faculty_name in zip(faculties_links, faculties_name):
            faculty_name: str = faculty_name.replace("\n", "").replace("\t", "")
            if not os.path.exists(f"data\\{faculty_name}"):
                os.makedirs(f"data\\{faculty_name}")

            schedules_links, schedules_name = find_schedules(faculty_url, monday)
            for schedule_link, schedule_name in zip(schedules_links, schedules_name):
                download_schedule(schedule_link, faculty_name, schedule_name)
    except Exception as exc:
        error = f"download: {exc}"
        print_error(error)


if __name__ == "__main__":
    download()
