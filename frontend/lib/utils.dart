import 'package:flutter/material.dart';
import 'package:clipboard/clipboard.dart';
import 'package:intl/intl.dart';
import 'package:url_launcher/url_launcher.dart';

class CopyLinkIcon extends StatelessWidget {
  final String link;

  const CopyLinkIcon({super.key, required this.link});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.content_copy),
      onPressed: () {
        FlutterClipboard.copy(link).then((value) => {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Link copied to clipboard')),
              )
            });
      },
    );
  }
}

class LinkIconWithHover extends StatelessWidget {
  final String link;

  const LinkIconWithHover({super.key, required this.link});

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: link,
      child: IconButton(
        icon: const Icon(Icons.link),
        onPressed: () =>
            launchUrl(Uri.parse(link), webOnlyWindowName: '_blank'),
      ),
    );
  }
}

String formatTimeMinute(String timeString) {
  DateTime time = DateTime.parse(timeString);
  var formatter = DateFormat('yyyy/MM/dd HH:mm');
  String formattedTime = formatter.format(time.toLocal());
  return formattedTime;
}

String ifIntToString(queryValue) {
  final String queryValueString =
      (queryValue is int) ? queryValue.toString() : queryValue;
  return queryValueString;
}

String formatFileSize(int fileSizeInt) {
  String fileSizeString;
  final double fileSizeDouble = fileSizeInt.toDouble();
  if (fileSizeInt < 1024) {
    fileSizeString = '${fileSizeInt}B';
  } else if (fileSizeInt < 1024 * 1024) {
    fileSizeString = '${(fileSizeDouble / 1024).toStringAsFixed(1)}K';
  } else if (fileSizeInt < 1024 * 1024 * 1024) {
    fileSizeString = '${(fileSizeDouble / 1024 / 1024).toStringAsFixed(1)}M';
  } else {
    fileSizeString =
        '${(fileSizeDouble / 1024 / 1024 / 1024).toStringAsFixed(1)}G';
  }
  return fileSizeString;
}

class LinkText extends StatelessWidget {
  final String link;

  const LinkText({super.key, required this.link});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => launchUrl(Uri.parse(link), webOnlyWindowName: '_blank'),
      child: Tooltip(
        message: link,
        child: const Text(
          'link',
          style: TextStyle(
            color: Colors.blue,
            decoration: TextDecoration.underline,
          ),
        ),
      ),
    );
  }
}

class TextWithHover extends StatelessWidget {
  final String text;
  final int maxLines;
  final TextStyle? style;
  final TextStyle? hoverStyle;

  const TextWithHover({
    super.key,
    required this.text,
    this.maxLines = 1,
    this.style,
    this.hoverStyle,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: text,
      child: Text(
        text,
        maxLines: maxLines,
        overflow: TextOverflow.ellipsis,
      ),
    );
  }
}

class TextWithDifferentHover extends StatelessWidget {
  final String hoverText;
  final String text;
  final int maxLines;
  final TextStyle? style;
  final TextStyle? hoverStyle;

  const TextWithDifferentHover({
    super.key,
    required this.hoverText,
    required this.text,
    this.maxLines = 1,
    this.style,
    this.hoverStyle,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: hoverText,
      child: Text(
        text,
        maxLines: maxLines,
        overflow: TextOverflow.ellipsis,
      ),
    );
  }
}
