from dataBase.models.UserModel import UserModel
from dataBase.repositories.base import BaseRepository
from dataBase.schemas.user import UserCreateSchema


class UserRepository(BaseRepository):
    def create(self, data: dict) -> UserModel:
        with self.db.atomic():
            user = UserModel.create(
                chat_id=data.get('chat_id'),
                first_name=data.get('first_name'),
                phone_number=data.get('phone')
            )
            return user

    def get_by_chat_id(self, chat_id: int) -> UserModel:
        user = UserModel.select().where(UserModel.chat_id == chat_id)
        return user.first()
