import 'package:http/http.dart' as http;
import 'dart:convert';
import 'globals.dart';

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
    'plugin_init_info': jsonEncode(formData),
  };

  var response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode(requestData),
  );
  return response;
}
