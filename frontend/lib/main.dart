import 'package:flutter/material.dart';
import 'search_page.dart';
import 'old_search_bar.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Index All In One App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      // home: const GFG(),
      initialRoute: '/',
      routes: {
        '/old': (context) => const OldSearchPage(),
        '/': (context) => const SearchPage(),
      },
    );
  }
}
