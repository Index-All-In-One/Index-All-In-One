import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'globals.dart';
import 'link_new_page.dart';

Future<http.Response> sendPluginListRequest() async {
  var url = Uri.parse('$baseUrl/plugin_list');

  var response = await http.get(url);
  return response;
}

Widget buildPluginList() {
  return FutureBuilder(
    future: sendPluginListRequest(),
    builder: (BuildContext context, AsyncSnapshot snapshot) {
      if (snapshot.hasData) {
        var response = snapshot.data;
        if (response.statusCode != 200) {
          //TODO alert user
          print("Plugin List API return unsuccessful response");
        }

        //TODD: error handling for type conversion
        final Map<String, dynamic> pluginNameMap = jsonDecode(response.body);
        return ListView.builder(
          itemCount: pluginNameMap.length,
          itemBuilder: (BuildContext context, int index) {
            String pluginName = pluginNameMap.keys.elementAt(index);
            //TODD: error handling for type conversion
            String pluginDisplayName = pluginNameMap[pluginName]!;

            return ListTile(
              title: Container(
                padding:
                    const EdgeInsets.symmetric(vertical: 10, horizontal: 10),
                color: Colors.grey[100],
                child: Row(children: [
                  Expanded(
                    child: Text(pluginDisplayName),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) =>
                                LinkNewInfoPage(pluginName: pluginName)),
                      );
                    },
                    child: const Text(
                      "Link New",
                      style: TextStyle(
                        color: Colors.blue,
                      ),
                    ),
                  ),
                ]),
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
