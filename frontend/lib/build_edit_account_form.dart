import 'package:flutter/material.dart';
import 'utils.dart';
import 'apis.dart';

Widget buildEditAccountForm(String pluginInstanceID) {
  return BuildFromHttpRequest(
      httpRequest: () => sendPIInfoValuesRequest(pluginInstanceID),
      apiErrorMessageName: "PI_info_value",
      builderUsingResponseBody: (responseBody) {
        Map<String, dynamic> pluginInstInfoValueWithHint =
            responseBody.cast<String, dynamic>();

        //TODO: error handling for type conversion
        String hint = pluginInstInfoValueWithHint["hint"]!;
        List<Map<String, String>> pluginInitInfoList =
            List<Map<String, String>>.from(
          pluginInstInfoValueWithHint["info_value"]!
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
              MapEntry(
                  "value",
                  ifIntOrBoolToString(
                      pluginInstInfoValueWithHint["source_name"])),
            ]),
            Map.fromEntries([
              const MapEntry("field_name", "interval"),
              const MapEntry("display_name", "Interval"),
              const MapEntry("type", "int"),
              MapEntry("value",
                  ifIntOrBoolToString(pluginInstInfoValueWithHint["interval"])),
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
                    MapEntry(
                        "value", ifIntOrBoolToString(pluginInitInfo["value"]!)),
                  ]))
              .toList(),
        };

        return FormWithSubmit(
          formSegments: [basicSegment, pluginSegment],
          successMessage: "Successfully modified!",
          onSubmit: (Map<String, String> formData) async => onlyCareStatus(
              () => sendEditPIRequest(pluginInstanceID, formData), "mod_PI"),
          onSendCode: (Map<String, String> formData) async => onlyCareStatus(
              () => send2StepCodeRequest(pluginInstanceID, null, formData),
              "send_2step_code"),
        );
      });
}
