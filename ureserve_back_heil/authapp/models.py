from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

ROLE_CHOICES = [
    ('etudiant', 'Étudiant'),
    ('delegue', 'Délégué'),
    ('administrateur', 'Administrateur'),
]

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Utilisation de set_password pour hacher le mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
<<<<<<< HEAD
    niveau = models.CharField(max_length=5)
=======
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05
    matricule = models.CharField(max_length=8)
    password = models.CharField(max_length=128)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Pour l'accès à l'admin
    is_superuser = models.BooleanField(default=False)  # Pour le superutilisateur

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'role', 'matricule']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.nom} ({self.role}) - {'Approuvé' if self.is_approved else 'En attente'}"
