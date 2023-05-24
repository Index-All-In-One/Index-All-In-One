import 'package:http/http.dart' as http;
import 'dart:convert';
import 'globals.dart';

Future<String> fetchThumbnail(String url) async {
  //Extract thumbnail from url
  var response = await http.get(Uri.parse(url));
  if (response.statusCode == 200) {
    var contentType = response.headers['content-type'];
    if (contentType != null && contentType.contains('image')) {
      return url;
    }
  }
  return "";
}

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
  var url = Uri.parse('$apiBaseUrl/search');

  var response = await http
      .post(url, body: {'keywords': query, 'full_text_keywords': query});
  return response;
}

Future<http.Response> sendSearchCountRequest(String query) async {
  var url = Uri.parse('$apiBaseUrl/search_count');

  var response = await http
      .post(url, body: {'keywords': query, 'full_text_keywords': query});
  return response;
}

Future<http.Response> sendListAccountRequest() async {
  var url = Uri.parse('$apiBaseUrl/list_accounts');

  var response = await http.get(url);
  return response;
}

Future<http.Response> sendPluginListRequest() async {
  var url = Uri.parse('$apiBaseUrl/plugin_list');

  var response = await http.get(url);
  return response;
}

Future<http.Response> sendPluginInfoFieldsRequest(String pluginName) async {
  var url = Uri.parse('$apiBaseUrl/plugin_info_field_type');

  var response = await http.post(url, body: {'plugin_name': pluginName});
  return response;
}

Future<http.Response> sendPIInfoValuesRequest(String pluginInstanceID) async {
  var url = Uri.parse('$apiBaseUrl/PI_info_value');

  var response = await http.post(url, body: {'id': pluginInstanceID});
  return response;
}

Future<http.Response> send2StepCodeRequest(String pluginInstanceID,
    String? pluginName, Map<String, String> formData) async {
  final url = Uri.parse('$apiBaseUrl/send_2step_code');

  formData.remove('source_name');
  formData.remove('interval');
  final Map<String, dynamic> requestData = {
    'plugin_init_info': formData,
    'id': pluginInstanceID,
  };
  if (pluginName != null) {
    requestData['plugin_name'] = pluginName;
  }

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

Future<http.Response> sendAddPIRequest(String? pluginInstanceID,
    String pluginName, Map<String, String> formData) async {
  final url = Uri.parse('$apiBaseUrl/add_PI');

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
  if (pluginInstanceID != null) {
    requestData['id'] = pluginInstanceID;
  }

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

Future<http.Response> sendEditPIRequest(
    String pluginInstanceID, Map<String, String> formData) async {
  final url = Uri.parse('$apiBaseUrl/mod_PI');

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

Future<http.Response> sendDelPIRequest(String pluginInstanceID) async {
  final url = Uri.parse('$apiBaseUrl/del_PI');
  try {
    var response = await http.post(url, body: {'id': pluginInstanceID});
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}

Future<http.Response> sendEnablePIRequest(String pluginInstanceID) async {
  final url = Uri.parse('$apiBaseUrl/enable_PI');
  try {
    var response = await http.post(url, body: {'id': pluginInstanceID});
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}

Future<http.Response> sendDisablePIRequest(String pluginInstanceID) async {
  final url = Uri.parse('$apiBaseUrl/disable_PI');
  try {
    var response = await http.post(url, body: {'id': pluginInstanceID});
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}

Future<http.Response> sendRestartPIRequest(String pluginInstanceID) async {
  final url = Uri.parse('$apiBaseUrl/restart_PI');
  try {
    var response = await http.post(url, body: {'id': pluginInstanceID});
    return response;
  } catch (e) {}

  return Future.value(fakeResponse);
}
