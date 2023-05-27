import 'package:flutter/material.dart';
import 'utils.dart';

Map<String, bool> getSourceFilters(List<dynamic>? queryResults) {
  if (queryResults == null) {
    return {};
  }
  Map<String, bool> sourceFilters = {};
  for (var queryResult in queryResults) {
    Map<String, dynamic> queryResultMap = queryResult as Map<String, dynamic>;
    String source = queryResultMap['source'] as String;
    sourceFilters[source] = true;
  }
  return sourceFilters;
}
