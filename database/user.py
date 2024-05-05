from config import get_database

dbname = get_database()
collection_user = dbname["users"]


def insert(user_id: int, group: str = None, facultie: str = None):
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "group": group or user["group"],
                    "facultie": facultie or user["facultie"],
                }
            },
        )
    else:
        collection_user.insert_one(
            {
                "user_id": user_id,
                "group": group,
                "facultie": facultie,
            }
        )


def get_user(user_id: int):
    user = collection_user.find_one({"user_id": user_id})
    if user:
        return user["group"]
    return None
