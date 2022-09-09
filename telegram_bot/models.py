from django.conf import settings
from django.db import models
import datetime



# Telegram_bot
class Telebot_Users(models.Model):
    status_types = (
        ('A', 'Approved'),
        ('P', 'Pending'),
        ('R', 'Removed')
    )
    Name = models.CharField(max_length=250)
    Family_Name = models.CharField(max_length=250)
    Mobile_Number = models.CharField(max_length=250, unique=True)
    Education = models.CharField(max_length=250)
    Field = models.CharField(max_length=250)
    Location = models.CharField(max_length=250)
    Date_Added = models.DateTimeField('date published',auto_now=True)
    Status = models.CharField(max_length=1, choices=status_types)

    class Meta:
        ordering = ('Date_Added', 'Status')


    def __str__(self):
        return self.Mobile_Number