import 'package:flutter/material.dart';
import 'search_bar.dart';
import 'build_search_results.dart';
import 'utils.dart';
import 'apis.dart';
import 'filter_utils.dart';

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
  Widget _searchResultsWidgetAsTile = const ListTile();
  List<dynamic>? _queryResults;
  Map<String, bool> _sourceFilters = {};

  final Widget _searchResultsFieldNameWidget = ListTile(
      title: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          color: Colors.grey[200],
          child: Row(
              children: documentFieldKeys
                  .map((key) => Expanded(
                      child: Center(
                          child: TextWithHover(
                              text: documentFieldDisplayNames[key]!,
                              maxLines: 1))))
                  .toList())));
  Widget _searchResultsFieldNameWidgetDisplay = const ListTile();

  double screenWidth = 0;
  double maxWidth = 500;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    screenWidth = MediaQuery.of(context).size.width;
    maxWidth = (screenWidth >= 1250) ? screenWidth * 0.5 : 625;
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
      body: SizedBox(
        width: _displayAsList ? screenWidth : maxWidth,
        child: Column(
          children: [
            MySearchBar(
              hintText: 'Search...',
              onSearch: _onSearchFunction,
            ),
            _searchResultsCountWidget,
            if (_displayAsList) _searchResultsFieldNameWidgetDisplay,
            Expanded(
                child: Container(
              alignment: Alignment.topLeft,
              child: _searchResultsWidget,
            )),
          ],
        ),
      ),
      floatingActionButton: Stack(
        children: [
          Positioned(
            bottom: 80.0,
            right: 16.0,
            child: FloatingActionButton(
              heroTag: 'fab-view-toggle',
              onPressed: _toggleView,
              child: Icon(_displayAsList ? Icons.view_list : Icons.grid_view),
            ),
          ),
          Positioned(
              bottom: 16.0,
              right: 16.0,
              child: FloatingActionButton(
                heroTag: 'fab-filter',
                onPressed: () => _showFilterDialog(context),
                child: const Icon(Icons.filter_list),
              )),
        ],
      ),
    );
  }

  void _showFilterDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: Column(
            mainAxisSize: MainAxisSize.min,
            //align left
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text("Filter by source:"),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Wrap(children: [
                  ..._sourceFilters.entries
                      .map((entry) => Padding(
                            padding: const EdgeInsets.fromLTRB(0, 4, 8, 4),
                            child: TextButtonWithToggle(
                              isSelected: entry.value,
                              onPressed: () => setState(() {
                                _sourceFilters[entry.key] =
                                    !(_sourceFilters[entry.key]!);
                              }),
                              label: entry.key,
                            ),
                          ))
                      .toList(),
                ]),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: ElevatedButton(
                  onPressed: () {
                    _updateSearchResultWithFilter(_sourceFilters);
                    Navigator.pop(context);
                  },
                  child: const Text("Apply"),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _updateSearchResultWithFilter(Map<String, bool>? sourceFilter) {
    _searchResultsWidgetAsList =
        buildSearchResultsAsListUseQueryResults(_queryResults, sourceFilter);
    _searchResultsWidgetAsTile = Container(
      constraints: BoxConstraints(maxWidth: maxWidth),
      child:
          buildSearchResultsAsTileUseQueryResults(_queryResults, sourceFilter),
    );

    setState(() {
      _searchResultsCountWidget =
          buildSearchResultCountFromQueryResults(_queryResults, sourceFilter);
      _searchResultsWidget = _displayAsList
          ? _searchResultsWidgetAsList
          : _searchResultsWidgetAsTile;
    });
  }

  void _onSearchFunction(String query) async {
    if (query.isNotEmpty) {
      _queryResults = await getQueryResults(query);
      _updateSearchResultWithFilter(null);

      setState(() {
        _searchResultsFieldNameWidgetDisplay = _searchResultsFieldNameWidget;
        _sourceFilters = getSourceFilters(_queryResults);
      });
    }
  }

  void _toggleView() {
    setState(() {
      _displayAsList = !_displayAsList;
      _searchResultsWidget = _displayAsList
          ? _searchResultsWidgetAsList
          : _searchResultsWidgetAsTile;
    });
  }
}
