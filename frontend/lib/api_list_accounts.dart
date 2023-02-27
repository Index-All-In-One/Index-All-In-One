import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'utils.dart';
import 'globals.dart';

Future<http.Response> sendListAccountRequest() async {
  var url = Uri.parse('$baseUrl/list_accounts');

  var response = await http.get(url);
  return response;
}

List<String> accountsFieldKeys = [
  "plugin_name",
  "source_name",
  "update_interval",
  "enabled",
  "active",
];

Map<String, String> accountsFieldDisplayNames = {
  "plugin_name": "Application Name",
  "source_name": "Source Title",
  "update_interval": "Update Interval",
  "enabled": "Enable",
  "active": "Active",
};

Widget buildAccountList() {
  return FutureBuilder(
    future: sendListAccountRequest(),
    builder: (BuildContext context, AsyncSnapshot snapshot) {
      if (snapshot.hasData) {
        var response = snapshot.data;
        List<dynamic> queryResults = [];
        if (response.statusCode == 200) {
          //TODO error handling for type conversion
          queryResults = jsonDecode(response.body);
        } else {
          //TODO alert user
          print("List Account API return unsuccessful response");
        }
        return ListView.builder(
          itemCount: queryResults.length + 2,
          itemBuilder: (BuildContext context, int index) {
            if (index == 0) {
              // return the header
              return ListTile(
                title: Text(
                    "You have ${queryResults.length} Account/Application(s)"),
              );
            }
            if (index == 1) {
              // return the header
              return ListTile(
                title: Container(
                  padding: const EdgeInsets.symmetric(vertical: 10),
                  color: Colors.grey[200],
                  child: Row(
                      children: accountsFieldKeys
                          .map((key) => Expanded(
                                child: Center(
                                    child:
                                        Text(accountsFieldDisplayNames[key]!)),
                              ))
                          .toList()),
                ),
              );
            }

            //TODO type conversion error handling
            Map<String, dynamic> singleQueryResult =
                queryResults[index - 2] as Map<String, dynamic>;
            return ListTile(
              title: Container(
                padding: const EdgeInsets.symmetric(vertical: 10),
                color: Colors.grey[100],
                child: Row(
                    children: accountsFieldKeys.map((key) {
                  Expanded returnWidget;
                  switch (key) {
                    default:
                      String queryValueString =
                          ifIntOrBoolToString(singleQueryResult[key]!);
                      returnWidget = Expanded(
                        child: Center(
                            child: TextWithHover(text: queryValueString)),
                      );
                      break;
                  }
                  return returnWidget;
                }).toList()),
              ),
            );
          },
        );
      } else {
        // Data hasn't been received yet, show a progress indicator
        return const Center(
          child: CircularProgressIndicator(),
          // child: Text("Loading..."),
        );
      }
    },
  );
}
