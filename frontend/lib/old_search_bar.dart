import 'package:flutter/material.dart';
import 'build_search_results.dart';

class OldSearchPage extends StatefulWidget {
  const OldSearchPage({Key? key}) : super(key: key);

  @override
  State<OldSearchPage> createState() => _OldSearchPageState();
}

class _OldSearchPageState extends State<OldSearchPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Index All In One",
        ),
        leading: IconButton(
          onPressed: () {
            // method to show the search bar
            showSearch(
              context: context,
              // delegate to customize the search bar
              delegate: CustomSearchDelegate(),
            );
            // Navigator.pushNamed(context, '/search');
          },
          icon: const Icon(Icons.search),
        ),
      ),
    );
  }
}

class CustomSearchDelegate extends SearchDelegate {
  // first overwrite to
  // clear the search text
  @override
  List<Widget>? buildActions(BuildContext context) {
    return [
      IconButton(
        onPressed: () {
          query = '';
        },
        icon: const Icon(Icons.clear),
      ),
    ];
  }

  // second overwrite to pop out of search menu
  @override
  Widget? buildLeading(BuildContext context) {
    return IconButton(
      onPressed: () {
        close(context, null);
      },
      icon: const Icon(Icons.arrow_back),
    );
  }

  // third overwrite to show query result
  @override
  Widget buildResults(BuildContext context) {
    return buildSearchResults(query);
  }

  // last overwrite to show the
  // querying process at the runtime
  @override
  Widget buildSuggestions(BuildContext context) {
    List<String> matchQuery = [];
    // for (var fruit in searchTerms) {
    //   if (fruit.toLowerCase().contains(query.toLowerCase())) {
    //     matchQuery.add(fruit);
    //   }
    // }
    return ListView.builder(
      itemCount: matchQuery.length,
      itemBuilder: (context, index) {
        var result = matchQuery[index];
        return ListTile(
          title: Text(result),
        );
      },
    );
  }
}
