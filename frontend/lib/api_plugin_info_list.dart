import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'globals.dart';

Future<http.Response> sendPluginInfoListRequest(String pluginName) async {
  var url = Uri.parse('$baseUrl/plugin_info_list');

  var response = await http.get(url);
  return response;
}

Widget buildPluginInfoList(String pluginName) {
  return FutureBuilder(
    future: sendPluginInfoListRequest(pluginName),
    builder: (BuildContext context, AsyncSnapshot snapshot) {
      if (snapshot.hasData) {
        var response = snapshot.data;
        Map<String, dynamic> pluginInfoWithHint = {};
        if (response.statusCode == 200) {
          //TODO error handling for type conversion
          pluginInfoWithHint = jsonDecode(response.body);
        } else {
          //TODO alert user
          print("Plugin Info List API return unsuccessful response");
        }
        String hint = pluginInfoWithHint["hint"] as String;
        List<String> pluginInfoFields =
            pluginInfoWithHint["info_list"] as List<String>;
        return ListView.builder(
          itemCount: pluginInfoWithHint.length,
          itemBuilder: (BuildContext context, int index) {
            String infoField = pluginInfoFields[index];

            return ListTile(
              title: Container(
                padding: const EdgeInsets.symmetric(vertical: 10),
                color: Colors.grey[100],
                child: Row(children: [
                  Text(infoField),
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
