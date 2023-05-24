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
                      final fileSizeOrigin = singleQueryResult[key]!.toString();
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

Widget buildSearchResultsAsTiles(String query) {
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
            String summary = singleQueryResult["summary"];
            String truncatedSummary = summary.length > 400
                ? '${summary.substring(0, 400)}...'
                : summary;

            //Make tailing text smaller
            var taillingStyle = const TextStyle(
                color: Colors.grey, fontStyle: FontStyle.italic, fontSize: 10);
            return Container(
              margin:
                  const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(8.0),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 5.0,
                    offset: const Offset(0, 3),
                  ),
                ],
              ),
              child: ListTile(
                contentPadding:
                    const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                // leading: TextWithHover(
                //   text: singleQueryResult["source"],
                // ),
                title: TextWithHover(
                  text: singleQueryResult["doc_name"],
                  maxLines: 2,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 4.0),
                    Text(truncatedSummary),
                    LinkTextButtonWithHover(
                      link: singleQueryResult["link"],
                    ),
                    Row(children: [
                      CopyLinkIconWithHover(link: singleQueryResult["link"]),
                      PopUpIconButton(
                        title: "Summary",
                        content: Text(summary),
                      ),
                    ]),
                  ],
                ),
                trailing: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    TextWithHover(
                        text: "${singleQueryResult["source"]}",
                        style: taillingStyle),
                    TextWithHover(
                        text: "${singleQueryResult["doc_type"]}",
                        style: taillingStyle),
                    TextWithDifferentHover(
                        hoverText: singleQueryResult["file_size"].toString(),
                        text: formatFileSize(
                            singleQueryResult["file_size"].toString()),
                        style: taillingStyle),
                    TextWithDifferentHover(
                        hoverText:
                            "Created Date: ${formatTimeMinute(singleQueryResult["created_date"])}\n"
                            "Modified Date: ${formatTimeMinute(singleQueryResult["modified_date"])}",
                        text: formatTimeMinute(
                            singleQueryResult["modified_date"]),
                        style: taillingStyle),
                  ],
                ),
              ),
            );
          },
        );
      });
}
