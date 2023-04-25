import 'package:flutter/material.dart';
import 'search_page.dart';
import 'old_search_bar.dart';
import 'settings_page.dart';
import 'link_new_page.dart';
import 'edit_account_page.dart';

Future<void> main() async {
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
        '/settings': (context) => const SettingsPage(),
        '/link_new': (context) => const LinkNewPage(),
      },
    );
  }
}
