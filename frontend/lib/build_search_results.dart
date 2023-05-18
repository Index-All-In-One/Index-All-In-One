import 'package:flutter/material.dart';
import 'package:index_all_in_one/utils.dart';
import 'apis.dart';

List<String> documentFieldKeys = [
  "source",
  "doc_name",
  "link",
  "doc_type",
  "file_size",
  "created_date",
  "modified_date",
  "summary",
];

Map<String, String> documentFieldDisplayNames = {
  "doc_name": "Name/Subject",
  "doc_type": "Type",
  "link": "Link",
  "source": "Source",
  "created_date": "Creation Date",
  "modified_date": "Modification Date",
  "summary": "Summary",
  "file_size": "Size",
};

Widget buildSearchResultCount(int count) {
  return ListTile(
    title: Text("Find $count result(s)"),
  );
}

Widget buildSearchResultCountFromRequest(String query) {
  return BuildFromHttpRequest(
    httpRequest: () => sendSearchCountRequest(query),
    apiErrorMessageName: "search",
    builderUsingResponseBody: (responseBody) {
      var queryResultCount = responseBody["count"] as int;
      return buildSearchResultCount(queryResultCount);
    },
    loadingWidget: buildSearchResultCount(0),
  );
}

Widget buildSearchResults(String query) {
  return BuildFromHttpRequest(
      httpRequest: () => sendSearchRequest(query),
      apiErrorMessageName: "search",
      builderUsingResponseBody: (responseBody) {
        List<dynamic> queryResults = responseBody.cast<dynamic>();

        return ListView.builder(
          itemCount: queryResults.length,
          itemBuilder: (BuildContext context, int index) {
            //TODO type conversion error handling
            Map<String, dynamic> singleQueryResult =
                queryResults[index] as Map<String, dynamic>;
            return ListTile(
              title: Container(
                padding: const EdgeInsets.symmetric(vertical: 10),
                color: Colors.grey[100],
                child: Row(
                    children: documentFieldKeys.map((key) {
                  Expanded returnWidget;
                  switch (key) {
                    case 'source':
                      returnWidget = Expanded(
                        child: Center(
                          child: TextWithHover(
                            text: singleQueryResult[key]!,
                            maxLines: 2,
                          ),
                        ),
                      );
                      break;
                    case 'doc_name':
                      returnWidget = Expanded(
                        child: Center(
                          child: TextWithHover(
                            text: singleQueryResult[key]!,
                            maxLines: 2,
                          ),
                        ),
                      );
                      break;
                    case 'summary':
                      final summaryText = singleQueryResult[key]!;
                      returnWidget = Expanded(
                        child: Center(
                          child: PopUpIconButton(
                            title: "Summary",
                            content: Text(summaryText),
                          ),
                        ),
                      );
                      break;
                    case 'created_date':
                    case 'modified_date':
                      final formattedTime =
                          formatTimeMinute(singleQueryResult[key]);
                      returnWidget = Expanded(
                          child: Center(
                        child: TextWithHover(
                          text: formattedTime,
                          maxLines: 2,
                        ),
                      ));
                      break;
                    case 'link':
                      final queryValue = singleQueryResult[key]!;
                      returnWidget = Expanded(
                        child: Center(
                          child: Wrap(
                            children: [
                              LinkIconWithHover(link: queryValue),
                              CopyLinkIconWithHover(link: queryValue),
                            ],
                          ),
                        ),
                      );
                      break;
                    case 'file_size':
                      final fileSizeOrigin = singleQueryResult[key]!;
                      returnWidget = Expanded(
                        child: Center(
                          child: TextWithDifferentHover(
                            hoverText: fileSizeOrigin,
                            text: formatFileSize(fileSizeOrigin),
                            maxLines: 2,
                          ),
                        ),
                      );
                      break;
                    default:
                      String queryValueString =
                          ifIntOrBoolToString(singleQueryResult[key]!);
                      returnWidget = Expanded(
                        child: Center(
                            child: TextWithHover(text: queryValueString)),
                      );
                      break;
                  }
                  return returnWidget;
                }).toList()),
              ),
            );
          },
        );
      });
}
