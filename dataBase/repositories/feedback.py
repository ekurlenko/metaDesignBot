from datetime import datetime
from typing import List

from dataBase.models.FeedbackModel import FeedbackModel
from dataBase.repositories.base import BaseRepository


class FeedbackRepository(BaseRepository):
    def get_not_done(self) -> List[FeedbackModel]:
        result = FeedbackModel.select().where(FeedbackModel.done_at == None)
        return result

    def update_done_at(self, feedback: FeedbackModel):
        feedback.done_at = datetime.now()
        feedback.save()
