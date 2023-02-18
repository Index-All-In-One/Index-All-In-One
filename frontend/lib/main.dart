import 'package:flutter/material.dart';
import 'search_bar.dart';
import 'api_search.dart';
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
    setState(() {
      _searchResultsWidget = buildSearchResults(query);
    });
  }
}
