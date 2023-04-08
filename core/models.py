from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.utils.translation import gettext_lazy as _


class SurvivorManager(BaseUserManager):
    def create_user(self, username, age, gender, latitude, longitude, inventory, password=None):
        if not username:
            raise ValueError('Username must exist')

        user = self.model(username=username,
                          age=age,
                          gender=gender,
                          latitude=latitude,
                          longitude=longitude,
                          inventory=inventory
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, age, gender, latitude, longitude, inventory, password=None):
        if not username:
            raise ValueError('Username must exist')

        user = self.model(username=username, age=age, gender=gender, latitude=latitude,
                          longitude=longitude, inventory=inventory)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Item(models.Model):
    item = models.CharField(max_length=50)
    points = models.CharField(max_length=255)

    def __str__(self):
        return self.item + self.points


class Inventory(models.Model):
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f"Inventory {self.id}"


class Survivor(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    username = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(5)],
        blank=True,
        null=True,
        unique=True,
        verbose_name='Name',
        help_text='Survivor Name'
    )
    age = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='Age',
        help_text='Survivor Age'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=False,
        null=False
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )
    inventory = models.OneToOneField(
        Inventory,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='survivor_inventory'
    )
    is_infected = models.BooleanField(default=False)
    reported_by = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='reports'
    )
    objects = SurvivorManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username + f'{self.id}'

    def att_is_infected(self):
        reports = self.reported_by.count()
        if reports >= 3:
            self.is_infected = True
            self.save()

    def no_inventory_for_infected(self):
        if self.is_infected:
            self.inventory = []
