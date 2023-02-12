from django.db import models

# Create your models here.

class users_model(models.Model):
    email = models.EmailField(max_length=50,primary_key=True)
    password = models.CharField(max_length=25)

    def __str__(self):
        return self.email + " " + self.password