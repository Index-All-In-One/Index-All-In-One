import 'package:http/http.dart' as http;
import 'dart:convert';
import 'globals.dart';

Future<http.Response> sendSearchRequest(String query) async {
  var url = Uri.parse('$baseUrl/search');

  var response =
      await http.post(url, body: {'keywords': query, 'foo': 'flutter'});
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

Future<http.Response> sendPluginInfoListRequest(String pluginName) async {
  var url = Uri.parse('$baseUrl/plugin_info_field_type');

  var response = await http.post(url, body: {'plugin_name': pluginName});
  return response;
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

  var response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode(requestData),
  );
  return response;
}
