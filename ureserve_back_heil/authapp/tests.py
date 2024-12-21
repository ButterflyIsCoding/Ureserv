from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser

class UserAPITests(APITestCase):

    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
                email='admin@example.com',
                password='adminpass',
                role='administrateur',
                is_approved=True
            )
            
        # Création d'un utilisateur étudiant
        self.student_user = CustomUser.objects.create_user(
            email='student@example.com',
            password='studentpass',
            role='etudiant'
        )
        
        # Création d'un utilisateur délégué non approuvé
        self.delegate_user = CustomUser.objects.create_user(
            email='delegate@example.com',
            password='delegatepass',
            role='delegue'
        )

    def test_register_student(self):
        url = reverse('signup')
        data = {
            'nom': 'Étudiant Test',
            'email': 'new_student@example.com',
            'role': 'etudiant',
            'niveau': '1',  # Ajoutez un niveau valide si nécessaire
            'matricule': '123456',
            'password': 'newstudentpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_register_delegate(self):
        url = reverse('signup')
        data = {
            'nom': 'Délégué Test',
            'email': 'new_delegate@example.com',
            'role': 'delegue',
            'niveau': '2',  # Ajoutez un niveau valide si nécessaire
            'matricule': '654321',
            'password': 'newdelegatepass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_login_success(self):
        url = reverse('login')
        data = {
            'email': 'student@example.com',
            'password': 'studentpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_delegate_not_approved(self):
        url = reverse('login')
        data = {
            'email': 'delegate@example.com',
            'password': 'delegatepass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_pending_delegates(self):
        url = reverse('pending-delegates')
        
        # Authentification en tant qu'administrateur
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Vérifie qu'il y a des délégués en attente

    def test_approve_delegate(self):
        # Authentification en tant qu'administrateur
        self.client.force_authenticate(user=self.admin_user)
        
        # Récupération de l'URL (pas de kwargs car l'ID est dans le corps de la requête)
        url = reverse('approve-delegate')
        
        # Envoyer une requête POST avec user_id dans le corps
        response = self.client.post(url, data={'user_id': self.delegate_user.id})
        
        # Vérifiez le code de statut
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Récupérer les données mises à jour
        self.delegate_user.refresh_from_db()
        self.assertTrue(self.delegate_user.is_approved)

