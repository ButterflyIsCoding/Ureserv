import 'package:flutter/material.dart';

class Authentification extends StatefulWidget {
  const Authentification({super.key});

  @override
  State<Authentification> createState() => _Authentification();
}

class _Authentification extends State<Authentification> {
  bool isHoveredLogin = false;
  bool isHoveredSignup = false;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Center(
          child: AspectRatio(
            aspectRatio: 2 / 3, // Proportion respectant l'image fournie
            child: Container(
              decoration: const BoxDecoration(
                image: DecorationImage(
                  image: AssetImage("assets/images/Rectangle.jpg"),
                  fit: BoxFit.cover, // Le fond orange
                ),
                borderRadius: BorderRadius.all(Radius.circular(30)),
              ),
              child: Stack(
                children: [
                  // Bande bleue (image)
                  Align(
                    alignment: Alignment.center,
                    child: AspectRatio(
                      aspectRatio: 1 / 3,
                      child: Container(
                        decoration: const BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage("assets/images/bandebleue.png"),
                            fit: BoxFit.fill,
                          ),
                        ),
                      ),
                    ),
                  ),
                  // Cercles semi-transparents
                  Positioned(
                    top: 200,
                    right: 50,
                    child: CircleAvatar(
                      radius: 60,
                      backgroundColor: const Color.fromARGB(255, 65, 63, 60).withOpacity(0.7),
                    ),
                  ),
                  Positioned(
                    top: 100,
                    left: 60,
                    child: CircleAvatar(
                      radius: 50,
                      backgroundColor: const Color.fromARGB(255, 65, 63, 60).withOpacity(0.7),
                    ),
                  ),
                  Positioned(
                    top: 150,
                    left: 30,
                    child: CircleAvatar(
                      radius: 30,
                      backgroundColor: const Color.fromARGB(255, 65, 63, 60).withOpacity(0.7),
                    ),
                  ),
                  
                  Positioned(
                    bottom: 100,
                    right: 80,
                    child: CircleAvatar(
                      radius: 60,
                      backgroundColor: const Color.fromARGB(255, 65, 63, 60).withOpacity(0.7),
                    ),
                  ),
                  // Logo U-Reserv
                  Align(
                    alignment: Alignment.topCenter,
                    child: Padding(
                      padding: const EdgeInsets.only(top: 50),
                      child: Image.asset(
                        "assets/images/petit_logo.png",
                        width: 90, // Ajustez la taille selon vos besoins
                      ),
                    ),
                  ),
                  Positioned(
                    top: 20,
                    right: 20,
                    child: MouseRegion(
                      onEnter: (_) => setState(() => isHoveredSignup = true),
                      onExit: (_) => setState(() => isHoveredSignup = false),
                      child: GestureDetector(
                        onTap: () => Navigator.pushNamed(context, '/signup'),
                        child: Text(
                          'Sign Up',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.normal,
                            color: isHoveredSignup ? Colors.white : Colors.black,
                          )
                        ),
                      ),
                    ),
                  ),
                  Positioned(
                    top: 20,
                    left: 20,
                    child: MouseRegion(
                      onEnter: (_) => setState(() => isHoveredLogin = true),
                      onExit: (_) => setState(() => isHoveredLogin = false),
                      child: GestureDetector(
                        onTap: () => Navigator.pushNamed(context, '/login'),
                        child: Text(
                          'Log In',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.normal,
                            color: isHoveredSignup ? Colors.white : Colors.black,
                          )
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
