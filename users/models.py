from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
# Create your models here.


class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="images/%Y/%m", default=u"images/default.jpg", max_length=100, blank = True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if self.password.find("pbkdf2_sha256$") ==-1:
            self.password = make_password(self.password)
        return super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.username





