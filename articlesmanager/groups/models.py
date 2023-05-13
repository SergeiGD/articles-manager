from django.db import models
from django.contrib.auth.models import Group, Permission
from django.urls import reverse


class UserGroup(Group):
    def get_update_url(self):
        return reverse('update_groups', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('detail_groups', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('detail_groups', kwargs={'pk': self.pk})

    def get_select_permission_url(self):
        return reverse('select_permission', kwargs={'pk': self.pk})

    def get_select_user_url(self):
        return reverse('select_user_for_group', kwargs={'pk': self.pk})

    class Meta:
        proxy = True


class GroupPermission(Permission):
    class Meta:
        proxy = True
