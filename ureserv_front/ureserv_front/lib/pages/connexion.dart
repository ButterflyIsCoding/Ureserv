import 'package:flutter/material.dart';

class Connexion extends StatelessWidget {
  const Connexion({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Connexion'),
        backgroundColor: Colors.blue,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Titre de la page
            const Text(
              'Bienvenue! Connectez-vous',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.blueAccent,
              ),
            ),
            const SizedBox(height: 20),
            
            // Champ de saisie pour l'email
            const TextField(
              decoration: InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.email),
              ),
              keyboardType: TextInputType.emailAddress,
            ),
            const SizedBox(height: 20),
            
            // Champ de saisie pour le mot de passe
            const TextField(
              obscureText: true, // Cacher le mot de passe
              decoration: InputDecoration(
                labelText: 'Mot de passe',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.lock),
              ),
            ),
            const SizedBox(height: 20),
            
            // Bouton de connexion
            ElevatedButton(
              onPressed: () {
                // Logique de connexion à ajouter ici
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Connexion réussie')),
                );
              },
             
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50), // Largeur du bouton
                padding: const EdgeInsets.all(16),
              ),
              child: const Text('Sign In'),
            ),
            const SizedBox(height: 20),
            
            // Lien vers la page d'authentification
            TextButton(
              onPressed: () {
                Navigator.pushNamed(context, '/signup'); // Redirection vers la page d'authentification
              },
              child: const Text(
                'Pas encore de compte? Inscrivez-vous!',
                style: TextStyle(color: Colors.blue),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
