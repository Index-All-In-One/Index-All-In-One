import 'package:http/http.dart' as http;
import 'dart:convert';
import 'globals.dart';

var fakeResponse = http.Response(
    '{"message": "Fake response: Encounterd Error when sending Http request"}',
    500);

Future<bool> onlyCareStatus(
    Future<http.Response> Function() requestFunction, String apiName) async {
  var response = await requestFunction();
  if (response.statusCode != 200) {
    //TODO add log
    print("$apiName API return unsuccessful response: ${response.body}");
    return false;
  }
  return true;
}

Future<http.Response> sendSearchRequest(String query) async {
  var url = Uri.parse('$baseUrl/search');

  var response = await http
      .post(url, body: {'keywords': query, 'full_text_keywords': query});
  return response;
}

Future<http.Response> sendSearchCountRequest(String query) async {
  var url = Uri.parse('$baseUrl/search_count');

  var response = await http
      .post(url, body: {'keywords': query, 'full_text_keywords': query});
  return response;
}

Future<http.Response> sendListAccountRequest() async {
  var url = Uri.parse('$baseUrl/list_accounts');

  var response = await http.get(url);
  return response;
}

Future<http.Response> sendPluginListRequest() async {
  var url = Uri.parse('$baseUrl/plugin_list');

  var response = await http.get(url);
  return response;
}

Future<http.Response> sendPluginInfoFieldsRequest(String pluginName) async {
  var url = Uri.parse('$baseUrl/plugin_info_field_type');

  var response = await http.post(url, body: {'plugin_name': pluginName});
  return response;
}

Future<http.Response> sendPIInfoValuesRequest(String pluginInstanceID) async {
  var url = Uri.parse('$baseUrl/PI_info_value');

  var response = await http.post(url, body: {'id': pluginInstanceID});
  return response;
}

Future<http.Response> sendEditPIRequest(
    String pluginInstanceID, Map<String, String> formData) async {
  final url = Uri.parse('$baseUrl/mod_PI');

  final sourceName = formData['source_name']!;
  final interval = int.parse(formData['interval']!);
  formData.remove('source_name');
  formData.remove('interval');
  final Map<String, dynamic> requestData = {
    'source_name': sourceName,
    'interval': interval,
    'plugin_init_info': formData,
    'id': pluginInstanceID,
  };

  try {
    var response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestData),
    );
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}

Future<http.Response> sendAddPIRequest(
    String pluginName, Map<String, String> formData) async {
  final url = Uri.parse('$baseUrl/add_PI');

  final sourceName = formData['source_name']!;
  final interval = int.parse(formData['interval']!);
  formData.remove('source_name');
  formData.remove('interval');
  final Map<String, dynamic> requestData = {
    'plugin_name': pluginName,
    'source_name': sourceName,
    'interval': interval,
    'plugin_init_info': formData,
  };

  try {
    var response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestData),
    );
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}

Future<http.Response> sendDelPIRequest(String pluginInstanceID) async {
  final url = Uri.parse('$baseUrl/del_PI');
  try {
    var response = await http.post(url, body: {'id': pluginInstanceID});
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}

Future<http.Response> sendEnablePIRequest(String pluginInstanceID) async {
  final url = Uri.parse('$baseUrl/enable_PI');
  try {
    var response = await http.post(url, body: {'id': pluginInstanceID});
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}

Future<http.Response> sendDisablePIRequest(String pluginInstanceID) async {
  final url = Uri.parse('$baseUrl/disable_PI');
  try {
    var response = await http.post(url, body: {'id': pluginInstanceID});
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}

Future<http.Response> sendRestartPIRequest(String pluginInstanceID) async {
  final url = Uri.parse('$baseUrl/restart_PI');
  try {
    var response = await http.post(url, body: {'id': pluginInstanceID});
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}
