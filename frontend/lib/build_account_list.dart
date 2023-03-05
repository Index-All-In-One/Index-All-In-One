import 'package:flutter/material.dart';
import 'utils.dart';
import 'apis.dart';

List<String> accountsFieldKeys = [
  "op", //special field
  "plugin_name",
  "source_name",
  "update_interval",
  "enabled",
  "active",
];

Map<String, String> accountsFieldDisplayNames = {
  "op": "Operation", //special field
  "plugin_name": "Application Name",
  "source_name": "Source Title",
  "update_interval": "Update Interval",
  "enabled": "Enable",
  "active": "Active",
};

Widget buildAccountList() {
  return BuildFromHttpRequest(
    httpRequest: sendListAccountRequest,
    apiErrorMessageName: "list_account",
    builderUsingResponseBody: (responseBody) {
      List<dynamic> queryResults = responseBody.cast<dynamic>();
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
                                  child: Text(accountsFieldDisplayNames[key]!)),
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
                  case 'op':
                    returnWidget = Expanded(
                        child: Center(
                      child: IconButtonWithDialog(
                        icon: const Icon(Icons.delete),
                        operationShort: "Delete",
                        operationPhrase: "delete this Account/Application",
                        operationExecution: () {
                          sendDelPIRequest(singleQueryResult['id'].toString());
                        },
                      ),
                    ));
                    break;
                  default:
                    String queryValueString =
                        ifIntOrBoolToString(singleQueryResult[key]!);
                    returnWidget = Expanded(
                      child:
                          Center(child: TextWithHover(text: queryValueString)),
                    );
                    break;
                }
                return returnWidget;
              }).toList()),
            ),
          );
        },
      );
    },
  );
}
