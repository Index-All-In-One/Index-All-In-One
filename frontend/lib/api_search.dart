import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import 'dart:convert';
import 'globals.dart';

Future<http.Response> sendSearchRequest(String query) async {
  var url = Uri.parse('$baseUrl/search');

  var response =
      await http.post(url, body: {'keywords': query, 'foo': 'flutter'});
  return response;
}

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

Widget buildSearchResults(String query) {
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
                  case 'created_date':
                  case 'modified_date':
                    DateTime time = DateTime.parse(singleQueryResult[key]!);
                    var formatter = DateFormat('yyyy/MM/dd HH:mm');
                    String formattedTime = formatter.format(time.toLocal());
                    print(formattedTime);
                    returnWidget = Expanded(
                      child: Text(
                        formattedTime,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    );
                    break;
                  default:
                    final queryValue = singleQueryResult[key]!;
                    final String queryValueString = (queryValue is int)
                        ? queryValue.toString()
                        : queryValue;
                    returnWidget = Expanded(
                      child: Tooltip(
                        message: queryValueString,
                        child: Text(
                          queryValueString,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
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
