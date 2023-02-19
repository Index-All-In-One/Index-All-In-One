import 'package:flutter/material.dart';
import 'package:clipboard/clipboard.dart';

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
