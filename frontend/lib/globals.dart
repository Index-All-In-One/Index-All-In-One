library my_project.globals;

import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';

final String baseUrl = Platform.environment['BASE_URL'] ??
    (dotenv.env['BASE_URL'] ?? 'http://127.0.0.1:5000');
