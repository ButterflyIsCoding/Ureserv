from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
<<<<<<< HEAD
        fields = ['id', 'nom', 'email', 'role', 'niveau', 'matricule', 'password', 'is_approved']
=======
        fields = ['id', 'nom', 'email', 'role', 'matricule', 'password', 'is_approved']
>>>>>>> 346bbacefa667e29d78f773503ee09874ed8cf05
        extra_kwargs = {
            'password': {'write_only': True},  # Ne pas exposer le mot de passe
            'is_approved': {'read_only': True},  # Empêcher les utilisateurs de définir ce champ
        }

    def validate(self, data):
        # Valider que tous les utilisateurs ont un mot de passe
        if not data.get('password'):
            raise serializers.ValidationError("Le champ 'password' est obligatoire.")
        
        # Pour les délégués, forcer `is_approved=False` au début
        if data.get('role') == 'delegue':
            data['is_approved'] = False  # Toujours non approuvé à la création
        else:
            data['is_approved'] = True # Toujours approuver a la creation
        return data

    def create(self, validated_data):
        # Hacher le mot de passe avant de sauvegarder
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
