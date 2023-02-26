import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'search_bar.dart';
import 'old_search_bar.dart';
import 'settings_page.dart';

Future<void> main() async {
  await dotenv.load();
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
      },
    );
  }
}

class SearchPage extends StatefulWidget {
  const SearchPage({super.key});

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  Widget _searchResultsWidget = ListView();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Index All In One'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.pushNamed(context, '/settings');
            },
          ),
        ],
      ),
      body: Column(
        children: [
          SearchBar(
            hintText: 'Search...',
            onSearch: onSearchFunction,
          ),
          Expanded(child: Container(child: _searchResultsWidget)),
        ],
      ),
    );
  }

  void onSearchFunction(String query) {
    if (query.isNotEmpty) {
      setState(() {
        _searchResultsWidget = buildSearchResults(query);
      });
    }
  }
}
