import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';
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
        List<Map<String, String>> pluginInitInfoList =
            List<Map<String, String>>.from(
          pluginInfoWithHint["field_def"]!
              .map((item) => Map<String, String>.from(item)),
        );

        FormSegment basicSegment = {
          "title": "Basic Information",
          "hint": null,
          "field_def": [
            Map.fromEntries([
              const MapEntry("field_name", "source_name"),
              const MapEntry("display_name", "Source Name"),
              const MapEntry("type", "text"),
            ]),
            Map.fromEntries([
              const MapEntry("field_name", "interval"),
              const MapEntry("display_name", "Interval"),
              const MapEntry("type", "int"),
            ]),
          ],
        };

        FormSegment pluginSegment = {
          "title": "Account/Application Information",
          "hint": hint,
          "field_def": pluginInitInfoList
              .map((pluginInitInfo) => Map.fromEntries([
                    MapEntry("field_name", pluginInitInfo["field_name"]!),
                    MapEntry("display_name", pluginInitInfo["display_name"]!),
                    MapEntry("type", pluginInitInfo["type"]!),
                    if (pluginInitInfo["type"] == "g_oauth")
                      MapEntry("scope", pluginInitInfo["scope"]!),
                  ]))
              .toList(),
        };
        String pluginInstanceID = const Uuid().v4();
        return FormWithSubmit(
          formSegments: [basicSegment, pluginSegment],
          successMessage: "Successfully linked $pluginName!",
          onSubmit: (Map<String, String> formData) async => onlyCareStatus(
              () => sendAddPIRequest(pluginInstanceID, pluginName, formData),
              "del_PI"),
          onSendCode: (Map<String, String> formData) async => onlyCareStatus(
              () =>
                  send2StepCodeRequest(pluginInstanceID, pluginName, formData),
              "send_2step_code"),
          pluginInstanceID: pluginInstanceID,
          pluginName: pluginName,
        );
      });
}
