from django.db import models



class ThreadManager(models.Manager):
    def get_or_create(self, user_1, user_2):
        # Ensure that the users are ordered by profile.user_id, so there is only one thread between two users
        if user_1.user_id > user_2.user_id:
            user_1, user_2 = user_2, user_1
        thread, created = self.get_queryset().get_or_create(
            user_1=user_1,
            user_2=user_2
        )
        return thread, created