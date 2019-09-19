from django.db import models


class MemberQuerySet(models.QuerySet):
    def descendants(self, member):
        return self.filter(sponsor = member.username)


class MemberManager(models.Manager):
    def get_queryset(self):
        return MemberQuerySet(self.model, using = self._db)  # Important!

    def descendants(self, member):
        return self.get_queryset().descendants(member)
