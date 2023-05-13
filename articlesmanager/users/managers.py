from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Менеджер для аутентификации по эл. почте
    """

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Создание пользователя с паролем и эл. почтой
        """
        if not email:
            raise ValueError(_('Необходимо указать электронную почту'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создание супер-пользователя с паролем и эл. почтой
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен быть членом персонала'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен быть отмечен как суперпользователь'))

        return self.create_user(email, password, **extra_fields)
