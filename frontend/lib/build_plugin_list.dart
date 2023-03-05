import 'package:flutter/material.dart';
import 'link_new_page.dart';
import 'apis.dart';
import 'utils.dart';

Widget buildPluginList() {
  return BuildFromHttpRequest(
    httpRequest: sendPluginListRequest,
    builderUsingResponseBody: (responseBody) {
      final Map<String, dynamic> pluginNameMap =
          responseBody.cast<String, dynamic>();
      return ListView.builder(
        itemCount: pluginNameMap.length,
        itemBuilder: (BuildContext context, int index) {
          String pluginName = pluginNameMap.keys.elementAt(index);
          //TODD: error handling for type conversion
          String pluginDisplayName = pluginNameMap[pluginName]!;

          return ListTile(
            title: Container(
              padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 10),
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
    },
  ); //TODD: error handling for type conversion
}
