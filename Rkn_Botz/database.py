import motor.motor_asyncio
from config import Rkn_Botz


class Database:
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(Rkn_Botz.DB_URL)
        self._database = self._client[Rkn_Botz.DB_NAME]

        self._users_collection = self._database.get_collection("users_data")
        self._channels_collection = self._database.get_collection("channels_data")

        # 🔒 Ensure unique users (IMPORTANT)
        self._users_collection.create_index(
            "userId",
            unique=True
        )

    # ─────────────────────────────
    # 👤 USERS
    # ─────────────────────────────
    async def register_user(self, user_id: int) -> bool:
        """
        Register user only if not exists.
        Returns True if new user inserted, False if already existed.
        """
        result = await self._users_collection.update_one(
            {"userId": user_id},
            {"$setOnInsert": {"userId": user_id}},
            upsert=True
        )
        return result.upserted_id is not None

    async def fetch_total_users(self) -> int:
        """
        Returns total number of unique users.
        """
        return await self._users_collection.count_documents({})

    async def list_all_users(self) -> list[int]:
        """
        Returns list of all unique user IDs.
        """
        cursor = self._users_collection.find(
            {},
            {"_id": 0, "userId": 1}
        )

        users = []
        async for doc in cursor:
            users.append(doc["userId"])
        return users

    async def remove_user(self, user_id: int) -> int:
        """
        Remove user by ID.
        Returns deleted count (0 or 1).
        """
        result = await self._users_collection.delete_one({"userId": user_id})
        return result.deleted_count

    # ─────────────────────────────
    # 📢 CHANNEL CAPTIONS
    # ─────────────────────────────
    async def add_channel_caption(self, channel_id: int, caption: str):
        """
        Add new channel caption.
        """
        await self._channels_collection.insert_one(
            {
                "channelId": channel_id,
                "caption": caption
            }
        )

    async def update_channel_caption(self, channel_id: int, caption: str) -> bool:
        """
        Update existing channel caption.
        """
        result = await self._channels_collection.update_one(
            {"channelId": channel_id},
            {"$set": {"caption": caption}},
            upsert=False
        )
        return result.modified_count > 0


# 🔥 Single DB instance
rkn_botz = Database()