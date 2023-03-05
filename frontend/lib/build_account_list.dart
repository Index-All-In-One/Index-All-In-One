import 'package:flutter/material.dart';
import 'utils.dart';
import 'apis.dart';

List<String> accountsFieldKeys = [
  "plugin_name",
  "source_name",
  "update_interval",
  "enabled",
  "active",
  "op", //special field
];

Map<String, String> accountsFieldDisplayNames = {
  "op": "Operation", //special field
  "plugin_name": "Application Name",
  "source_name": "Source Title",
  "update_interval": "Update Interval",
  "enabled": "Enabled",
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
                      child: IconButtonWithConfirm(
                        icon: const Icon(Icons.delete),
                        operationShort: "Delete",
                        operationPhrase: "delete this Account/Application",
                        operationExecution: () {
                          waitAndShowSnackBarMsg(
                            context,
                            () async => onlyCareStatus(
                                () => sendDelPIRequest(
                                    singleQueryResult['id'].toString()),
                                "del_PI"),
                            "Deleted successfully!",
                            "Failed to delete.",
                            false,
                          );
                        },
                      ),
                    ));
                    break;

                  case 'enabled':
                    returnWidget = Expanded(
                        child: Center(
                            child: Wrap(
                      children: [
                        // TextWithHover(
                        //     text: ifIntOrBoolToString(singleQueryResult[key]!)),
                        ToggleSwitch(
                          initialValue: singleQueryResult[key]!,
                          onToggle: (value) {
                            if (value) {
                              waitAndShowSnackBarMsg(
                                context,
                                () async => onlyCareStatus(
                                    () => sendEnablePIRequest(
                                        singleQueryResult['id'].toString()),
                                    "enable_PI"),
                                "Enabled successfully!",
                                "Failed to enable.",
                                false,
                              );
                            } else {
                              waitAndShowSnackBarMsg(
                                context,
                                () async => onlyCareStatus(
                                    () => sendDisablePIRequest(
                                        singleQueryResult['id'].toString()),
                                    "disable_PI"),
                                "Disabled successfully!",
                                "Failed to disable.",
                                false,
                              );
                            }
                          },
                        )
                      ],
                    )));
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
