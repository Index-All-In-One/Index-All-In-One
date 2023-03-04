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

String ifIntOrBoolToString(queryValue) {
  final String queryValueString = (queryValue is int)
      ? queryValue.toString()
      : ((queryValue is bool) ? queryValue.toString() : queryValue);
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

class PopUpDialog extends StatelessWidget {
  final String title;
  final Widget content;

  const PopUpDialog({super.key, required this.title, required this.content});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      content: content,
      title: Row(
        children: [
          Expanded(child: Text(title)),
          Align(
            alignment: Alignment.topRight,
            child: IconButton(
              icon: const Icon(Icons.close),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ),
        ],
      ),
    );
  }
}

class PopUpIconButton extends StatelessWidget {
  final String title;
  final Widget content;

  const PopUpIconButton(
      {super.key, required this.title, required this.content});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.info),
      onPressed: () {
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return PopUpDialog(title: title, content: content);
          },
        );
      },
    );
  }
}

void showErrorAlert(String errorMesssage, BuildContext context) {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return PopUpDialog(title: "Error", content: Text(errorMesssage));
    },
  );
}

class FormWithSubmit extends StatefulWidget {
  final Map<String, String> fieldNameWithTypes;
  final String hint;
  final Function(Map<String, String> formData)? onSubmit;

  const FormWithSubmit({
    super.key,
    required this.fieldNameWithTypes,
    this.hint = "",
    this.onSubmit,
  });

  @override
  State<FormWithSubmit> createState() => _FormWithSubmitState();
}

class _FormWithSubmitState extends State<FormWithSubmit> {
  final _formKey = GlobalKey<FormState>();
  final Map<String, String> _formData = {};

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 10),
            child: Text(
              'Please fill in information below',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Text(
              "Hint: ${widget.hint}",
              style: TextStyle(fontSize: 16, color: Colors.grey[600]),
            ),
          ),
          for (var field in widget.fieldNameWithTypes.keys) ...[
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(
                field,
                style: const TextStyle(fontSize: 16),
              ),
            ),
            TextFormField(
              cursorColor: Colors.blue,
              decoration: InputDecoration(
                contentPadding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                  borderSide: const BorderSide(color: Colors.blue),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                  borderSide: const BorderSide(color: Colors.grey),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                  borderSide: const BorderSide(color: Colors.blue),
                ),
                errorBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                  borderSide: const BorderSide(color: Colors.red),
                ),
                focusedErrorBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                  borderSide: const BorderSide(color: Colors.red),
                ),
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter $field';
                }
                switch (widget.fieldNameWithTypes[field]) {
                  case 'int':
                    if (int.tryParse(value) == null) {
                      return 'Please enter a valid integer for $field';
                    }
                    break;
                  default:
                }
                return null;
              },
              onSaved: (value) {
                _formData[field] = value!;
              },
            ),
          ],
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () {
              if (_formKey.currentState!.validate()) {
                _formKey.currentState!.save();
                print(_formData);
                widget.onSubmit?.call(_formData);
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blue,
              padding: const EdgeInsets.symmetric(horizontal: 56, vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            child: const Text('Submit'),
          ),
        ],
      ),
    );
  }
}
