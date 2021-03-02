import datetime

from django.db import models
from django.utils.timezone import utc

# Create your models here.


class CommonInfo(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, blank=True)

    def __str__(self):
        return '%s' % self.pk

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        utc_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        if not self.pk:
            self.created_at = utc_time
        self.updated_at = utc_time

        if (kwargs.get('update_fields') and
                'updated_at' not in kwargs['update_fields']):
            kwargs['update_fields'].append('updated_at')

        super(CommonInfo, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Person(CommonInfo):
    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100)
    date_of_birth = models.DateField('Date of birth')
    email = models.EmailField(
        "email", blank=True, max_length=255, db_index=True)
    address = models.CharField('Home Address', max_length=255, blank=True)

    class Meta:
        abstract = True


class User(Person):
    """ Patient’s Information """

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.date_of_birth})"

    class Meta:
        unique_together = (
            "first_name", "last_name", "date_of_birth", "address")


class Doctor(Person):
    reg_number = models.CharField(
        'Registration Number', max_length=100, unique=True, db_index=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.reg_number}]"

    class Meta:
        unique_together = ("first_name", "last_name", "reg_number")


class Drug(CommonInfo):
    name = models.CharField('Name', max_length=255)

    def __str__(self):
        return f"{self.name}"


class Pharmacy(CommonInfo):
    name = models.CharField('Name', max_length=255)
    address = models.CharField('Address', max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Pharmacies'


class Booking(CommonInfo):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.PROTECT)
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)

    def __str__(self):
        return (
            f"[{self.doctor.reg_number} | "
            f"{self.user.first_name} {self.user.last_name} | "
            f"{self.pharmacy.name} | {self.drug.name}]")
