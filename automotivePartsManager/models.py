from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role='user'):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Usuário Comum'),
        ('admin', 'Administrador'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"

class Part(models.Model):
    part_number = models.CharField(max_length=50, blank=False)
    name = models.CharField(max_length=100, blank=False)
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    quantity = models.IntegerField(blank=False, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.part_number})"
    
class CarModel(models.Model):
    name = models.CharField(max_length=255, blank=False)
    manufacturer = models.CharField(max_length=255, blank=False)
    year = models.IntegerField(blank=False)

    class Meta:
        ordering = ['manufacturer', 'name', 'year']

    def __str__(self):
        return f"{self.manufacturer} {self.name} ({self.year})"
    
class PartCarModel(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("part", "car_model")

    def __str__(self):
        return f"{self.part.name} - {self.car_model.name}"