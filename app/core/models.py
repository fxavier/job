from django.db import models
from django.db.models.signals import pre_save, post_save

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from app import settings
from core.utils import unique_slug_generator, profile_image_file_path

from PIL import Image


JOB_TYPE = (
    ('TI', 'Tempo Inteiro'),
    ('PT', 'Part Time'),
    ('T', 'Temporario'),
    ('FL', 'Freelance')
)

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles")
    image = models.ImageField(upload_to=profile_image_file_path, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    resume = models.TextField(blank=True)
    company = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self, image)
        if img.height > 200 or img.width > 200:
            new_size = (200, 200)
            img.thumbnail(new_size)
            img.save(self.image.path)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    
    def job_count(self):
        return self.jobs.all().count() * 300


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender=Category)    
class Job(models.Model):
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=255)
    job_type = models.CharField(max_length=2, blank=False, choices=JOB_TYPE)
    location = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=False)
    publishing_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="job_employee")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="jobs")


    def __str__(self):
        return self.title


def job_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(job_pre_save_receiver, sender=Job)
