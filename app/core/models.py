from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from django.conf import settings
from django.utils.text import slugify


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for clothes"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Material(models.Model):
    """Material to be used in clothes"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Shop from which a user bought a piece of clothing"""
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    """Category for a piece of clothing"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Clothing(models.Model):
    """"Clothing object"""
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=1000)
    materials = models.ManyToManyField('Material')
    tags = models.ManyToManyField('Tag')
    shops = models.ManyToManyField('Shop')
    category = models.ForeignKey(
        Category,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
