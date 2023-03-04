import 'package:http/http.dart' as http;
import 'globals.dart';

Future<http.Response> sendAddPIRequest(String query) async {
  var url = Uri.parse('$baseUrl/addPI');

  var response =
      await http.post(url, body: {'keywords': query, 'foo': 'flutter'});
  return response;
}
