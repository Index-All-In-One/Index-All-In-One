import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

String baseUrl = 'http://127.0.0.1:5000';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const GFG(),
    );
  }
}

// This is the widget that will be shown
// as the homepage of your application.

class GFG extends StatefulWidget {
  const GFG({Key? key}) : super(key: key);

  @override
  State<GFG> createState() => _GFGState();
}

class _GFGState extends State<GFG> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Index All In One",
        ),
        actions: [
          IconButton(
            onPressed: () {
              // method to show the search bar
              showSearch(
                  context: context,
                  // delegate to customize the search bar
                  delegate: CustomSearchDelegate());
            },
            icon: const Icon(Icons.search),
          )
        ],
      ),
    );
  }
}

class CustomSearchDelegate extends SearchDelegate {
  // Demo list to show querying
  List<String> docNameList = [
    "A very loooooooooooooooooong file name",
    "Apple",
    "Banana",
    "Mango",
    "Pear",
    "Watermelons",
    "Blueberries",
    "Pineapples",
    "Strawberries"
  ];

  List<String> documentFieldKeys = [
    "source",
    "doc_name",
    "link",
    "doc_type",
    "file_size",
    "created_date",
    "modified_date",
    "summary",
  ];

  Map<String, String> documentFieldDisplayNames = {
    "doc_name": "Name/Title",
    "doc_type": "Type",
    "link": "Link",
    "source": "Source",
    "created_date": "Created Date",
    "modified_date": "Modified Date",
    "summary": "Summary",
    "file_size": "Size",
  };

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

  Future<http.Response> sendSearchRequest(String query) async {
    var url = Uri.parse('$baseUrl/search');

    var response =
        await http.post(url, body: {'keywords': query, 'foo': 'flutter'});
    return response;
  }

  // third overwrite to show query result
  @override
  Widget buildResults(BuildContext context) {
    return FutureBuilder(
      future: sendSearchRequest(query),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData) {
          var response = snapshot.data;

          List<dynamic> queryResults = [];
          if (response.statusCode == 200) {
            //TODO error handling for type conversion
            queryResults = jsonDecode(response.body);
          } else {
            //TODO alert user
            print("Search API return unsuccessful response");
          }
          return ListView.builder(
            itemCount: queryResults.length + 1,
            itemBuilder: (BuildContext context, int index) {
              if (index == 0) {
                // return the header
                return ListTile(
                  title: Row(
                      children: documentFieldKeys
                          .map((key) => Expanded(
                                child: Text(documentFieldDisplayNames[key]!),
                              ))
                          .toList()),
                );
              }

              //TODO type conversion error handling
              Map<String, dynamic> singleQueryResult =
                  queryResults[index - 1] as Map<String, dynamic>;
              return ListTile(
                title: Row(
                    children: documentFieldKeys.map((key) {
                  Expanded returnWidget;
                  switch (key) {
                    case 'doc_name':
                      returnWidget = Expanded(
                        child: Tooltip(
                          message: singleQueryResult[key]!,
                          child: Text(
                            singleQueryResult[key]!,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      );
                      break;
                    case 'summary':
                      returnWidget = Expanded(
                        child: Text(
                          singleQueryResult[key]!,
                          softWrap: false,
                          maxLines: 3,
                          overflow: TextOverflow.ellipsis,
                        ),
                      );
                      break;
                    default:
                      returnWidget = Expanded(
                        child: Text(singleQueryResult[key]!),
                      );
                      break;
                  }
                  return returnWidget;
                }).toList()),
              );
            },
          );
        } else {
          // Data hasn't been received yet, show a progress indicator
          return const Center(
            child: CircularProgressIndicator(),
          );
        }
      },
    );
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
