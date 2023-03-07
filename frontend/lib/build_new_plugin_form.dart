import 'package:flutter/material.dart';
import 'utils.dart';
import 'apis.dart';

Widget buildNewAccountForm(String pluginName) {
  return BuildFromHttpRequest(
      httpRequest: () => sendPluginInfoFieldsRequest(pluginName),
      apiErrorMessageName: "plugin_info_field_type",
      builderUsingResponseBody: (responseBody) {
        Map<String, dynamic> pluginInfoWithHint =
            responseBody.cast<String, dynamic>();

        //TODO: error handling for type conversion
        String hint = pluginInfoWithHint["hint"]!;
        Map<String, String> pluginInfoFieldTypes =
            pluginInfoWithHint["field_type"].cast<String, String>();

        FormSegment basicSegment = {
          "title": "Basic Information",
          "hint": null,
          "field_info": [
            Map.fromEntries([
              const MapEntry("field_name", "source_name"),
              const MapEntry("display_name", "source name"),
              const MapEntry("type", "text"),
            ]),
            Map.fromEntries([
              const MapEntry("field_name", "interval"),
              const MapEntry("display_name", "interval"),
              const MapEntry("type", "int"),
            ]),
          ],
        };

        FormSegment pluginSegment = {
          "title": "Account/Application Information",
          "hint": hint,
          "field_info": pluginInfoFieldTypes.entries
              .map((entry) => Map.fromEntries([
                    MapEntry("field_name", entry.key),
                    MapEntry("display_name", entry.key),
                    MapEntry("type", entry.value),
                  ]))
              .toList(),
        };

        return FormWithSubmit(
          formSegments: [basicSegment, pluginSegment],
          successMessage: "Successfully linked $pluginName!",
          onSubmit: (Map<String, String> formData) async => onlyCareStatus(
              () => sendAddPIRequest(pluginName, formData), "del_PI"),
        );
      });
}
