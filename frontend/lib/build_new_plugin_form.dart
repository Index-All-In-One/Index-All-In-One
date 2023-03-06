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
        List<String> pluginInfoFieldNames =
            ["source name", "interval"] + pluginInfoFieldTypes.keys.toList();
        pluginInfoFieldTypes.addEntries([
          const MapEntry("source name", "text"),
          const MapEntry("interval", "int"),
        ]);

        //TODO: specify field sequence
        return FormWithSubmit(
          fieldNames: pluginInfoFieldNames,
          fieldTypes: pluginInfoFieldTypes,
          hint: hint,
          successMessage: "Successfully linked $pluginName!",
          onSubmit: (Map<String, String> formData) async => onlyCareStatus(
              () => sendAddPIRequest(pluginName, formData), "del_PI"),
        );
      });
}
