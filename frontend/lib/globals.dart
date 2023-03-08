library my_project.globals;

import 'package:flutter_dotenv/flutter_dotenv.dart';

final String baseUrl = dotenv.env['BASE_URL'] ?? 'http://127.0.0.1:5000';
