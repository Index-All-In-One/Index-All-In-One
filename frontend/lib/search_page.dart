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
  Widget _searchResultsCountWidget = const ListTile();
  Widget _searchResultsWidget = ListView();
  bool _displayAsList = false;
  Widget _searchResultsWidgetAsList = const ListTile();
  Widget _searchResultsFieldNameWidget = const ListTile();
  Widget _searchResultsWidgetAsTile = const ListTile();

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
      floatingActionButton: FloatingActionButton(
        onPressed: _toggleView,
        child: Icon(_displayAsList ? Icons.view_list : Icons.grid_view),
      ),
    );
  }

  void _toggleView() {
    setState(() {
      _displayAsList = !_displayAsList;
      if (_displayAsList) {
        _searchResultsWidget = _searchResultsWidgetAsList;
      } else {
        _searchResultsWidget = _searchResultsWidgetAsTile;
      }
    });
  }

  void onSearchFunction(String query) {
    if (query.isNotEmpty) {
      _searchResultsWidgetAsList = buildSearchResults(query);
      _searchResultsWidgetAsTile = buildSearchResultsAsTiles(query);
      setState(() {
        _searchResultsCountWidget = buildSearchResultCountFromRequest(query);
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
        if (_displayAsList) {
          _searchResultsWidget = _searchResultsWidgetAsList;
        } else {
          _searchResultsWidget = _searchResultsWidgetAsTile;
        }
      });
    }
  }
}
