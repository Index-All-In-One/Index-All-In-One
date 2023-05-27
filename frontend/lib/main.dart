import 'package:flutter/material.dart';
import 'search_page.dart';
import 'settings_page.dart';
import 'link_new_page.dart';

Future<void> main() async {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Your all-in-one Search Engine!',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const SearchPage(),
        '/settings': (context) => const SettingsPage(),
        '/link_new': (context) => const LinkNewPage(),
      },
    );
  }
}
