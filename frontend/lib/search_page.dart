import 'package:flutter/material.dart';
import 'search_bar.dart';
import 'build_search_results.dart';
import 'utils.dart';

class SearchPage extends StatefulWidget {
  const SearchPage({super.key});

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  Widget _searchResultsWidget = ListView();
  Widget _searchResultsCountWidget = const ListTile();
  // init with empty widget to avoid take up space
  Widget _searchResultsFieldNameWidget = const ListTile();
  bool _displayAsList = false;

  @override
  void initState() {
    super.initState();
  }

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
          MySearchBar(
            hintText: 'Search...',
            onSearch: onSearchFunction,
          ),
          _searchResultsCountWidget,
          if (_displayAsList) _searchResultsFieldNameWidget,
          Expanded(child: Container(child: _searchResultsWidget)),
        ],
      ),
    );
  }

  void onSearchFunction(String query) {
    if (query.isNotEmpty) {
      setState(() {
        _searchResultsCountWidget = buildSearchResultCountFromRequest(query);
        if (_displayAsList) {
          _searchResultsWidget = buildSearchResults(query);
          _searchResultsFieldNameWidget = ListTile(
            title: Container(
              padding: const EdgeInsets.symmetric(vertical: 10),
              color: Colors.grey[200],
              child: Row(
                  children: documentFieldKeys
                      .map((key) => Expanded(
                            child: Center(
                                child: TextWithHover(
                              text: documentFieldDisplayNames[key]!,
                              maxLines: 1,
                            )),
                          ))
                      .toList()),
            ),
          );
        } else {
          _searchResultsWidget = buildSearchResultsAsTiles(query);
        }
      });
    }
  }
}
