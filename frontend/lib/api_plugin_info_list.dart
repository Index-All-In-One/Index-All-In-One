import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:index_all_in_one/apis.dart';
import 'package:index_all_in_one/utils.dart';
import 'dart:convert';
import 'globals.dart';

Future<http.Response> sendPluginInfoListRequest(String pluginName) async {
  var url = Uri.parse('$baseUrl/plugin_info_field_type');

  var response = await http.post(url, body: {'plugin_name': pluginName});
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
        //TODO error handling for type conversion
        String hint = pluginInfoWithHint["hint"]!;
        Map<String, String> pluginInfoFieldTypes =
            pluginInfoWithHint["field_type"].cast<String, String>();
        List<String> pluginInfoFieldNames =
            ["source_name", "interval"] + pluginInfoFieldTypes.keys.toList();
        pluginInfoFieldTypes.addEntries([
          const MapEntry("source_name", "text"),
          const MapEntry("interval", "int"),
        ]);

        return FormWithSubmit(
          fieldNames: pluginInfoFieldNames,
          fieldTypes: pluginInfoFieldTypes,
          hint: hint,
          onSubmit: (Map<String, String> formData) async {
            var response = await sendAddPIRequest(pluginName, formData);
            if (response.statusCode == 200) {
              //TODO alert user
              print("Add PI API return successful response");
            } else {
              //TODO alert user
              print("Add PI API return unsuccessful response");
            }
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
