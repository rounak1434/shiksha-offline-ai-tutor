import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'services/shiksha_tutor_service.dart';
import 'screens/chat_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Mobile Android portrait orientation lock
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  // System bar styling
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      systemNavigationBarColor: Color(0xFF0F172A),
      systemNavigationBarIconBrightness: Brightness.light,
    ),
  );

  final tutorService = ShikshaPlatformTutorService();

  runApp(ShikshaApp(tutorService: tutorService));
}

class ShikshaApp extends StatelessWidget {
  final IShikshaTutorService tutorService;

  const ShikshaApp({
    super.key,
    required this.tutorService,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SHIKSHA',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        primaryColor: const Color(0xFF38BDF8),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF38BDF8),
          surface: Color(0xFF111C2A),
        ),
      ),
      home: ChatScreen(tutorService: tutorService),
    );
  }
}
