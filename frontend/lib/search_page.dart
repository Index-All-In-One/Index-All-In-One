import 'package:flutter/material.dart';
import 'search_bar.dart';
import 'api_search.dart';

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
