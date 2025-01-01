import 'package:flutter/material.dart';
import 'package:ureserv_front/pages/welcome.dart';
//import 'package:ureserv_front/pages/authentification.dart';
//import 'package:ureserv_front/pages/connexion.dart';
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Welcome(),
      /*
      title: 'Flutter Navigation',
      initialRoute: '/',
      routes: {
        '/signup': (context) => const Authentification(),
        '/login':(context) => const Connexion(),
        '/profile': (context) => const Welcome(),
        }, */
      

    );
  }
}