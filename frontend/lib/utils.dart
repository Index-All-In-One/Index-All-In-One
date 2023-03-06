import 'package:flutter/material.dart';
import 'package:clipboard/clipboard.dart';
import 'package:intl/intl.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class IconButtonWithHover extends StatelessWidget {
  final String hoverText;
  final Icon icon;
  final Function() onPressed;

  const IconButtonWithHover({
    super.key,
    required this.hoverText,
    required this.icon,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: hoverText,
      child: IconButton(
        icon: icon,
        onPressed: onPressed,
      ),
    );
  }
}

class CopyLinkIconWithHover extends StatelessWidget {
  final String link;

  const CopyLinkIconWithHover({super.key, required this.link});

  @override
  Widget build(BuildContext context) {
    return IconButtonWithHover(
      hoverText: 'Copy link to clipboard',
      icon: const Icon(Icons.content_copy),
      onPressed: () {
        FlutterClipboard.copy(link).then((value) {
          clearAndShowSnackBarMsg(context, 'Link copied to clipboard');
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
    return IconButtonWithHover(
      hoverText: link,
      icon: const Icon(Icons.link),
      onPressed: () => launchUrl(Uri.parse(link), webOnlyWindowName: '_blank'),
    );
  }
}

class RefreshIconWithHover extends StatelessWidget {
  final Function() onPressed;

  const RefreshIconWithHover({super.key, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return IconButtonWithHover(
      hoverText: 'Refresh',
      icon: const Icon(Icons.refresh),
      onPressed: onPressed,
    );
  }
}

class RefreshIcon extends StatelessWidget {
  final Function() onPressed;

  const RefreshIcon({super.key, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.refresh),
      onPressed: onPressed,
    );
  }
}

String formatTimeMinute(String? timeString) {
  if (timeString == null) {
    return 'empty time';
  } else {
    DateTime time = DateTime.parse(timeString);
    var formatter = DateFormat('yyyy/MM/dd HH:mm');
    String formattedTime = formatter.format(time.toLocal());
    return formattedTime;
  }
}

String ifIntOrBoolToString(queryValue) {
  final String queryValueString = (queryValue is int)
      ? queryValue.toString()
      : ((queryValue is bool) ? queryValue.toString() : queryValue);
  return queryValueString;
}

String boolToYesNo(bool value) {
  return value ? 'Yes' : 'No';
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

String? pluginInfoFieldTypeValidator(value, type, field) {
  switch (type) {
    case 'int':
      if (int.tryParse(value) == null) {
        return 'Please enter a valid integer for $field';
      }
      break;
    default:
  }
  return null;
}

class FormWithSubmit extends StatefulWidget {
  final List<String> fieldNames;
  final Map<String, String> fieldTypes;
  final String hint;
  final Future<bool> Function(Map<String, String> formData)? onSubmit;
  final String? successMessage;

  const FormWithSubmit({
    super.key,
    required this.fieldNames,
    required this.fieldTypes,
    this.hint = "",
    this.onSubmit,
    this.successMessage,
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
          for (var fieldName in widget.fieldNames) ...[
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(
                fieldName,
                style: const TextStyle(fontSize: 16),
              ),
            ),
            TextFormFieldWithStyle(
              fieldName: fieldName,
              formData: _formData,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter $fieldName';
                }
                return pluginInfoFieldTypeValidator(
                    value, widget.fieldTypes[fieldName]!, fieldName);
              },
              isCredential: widget.fieldTypes[fieldName] == 'secret',
            ),
          ],
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () async {
              if (_formKey.currentState!.validate()) {
                _formKey.currentState!.save();
                waitAndShowSnackBarMsg(
                  context,
                  () async {
                    final success =
                        await widget.onSubmit?.call(_formData) ?? true;
                    return success;
                  },
                  widget.successMessage ?? 'Form submitted successfully',
                  'An error occurred while submitting the form',
                  true,
                );
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

class TextFormFieldWithStyle extends StatefulWidget {
  final String fieldName;
  final String? Function(String?)? validator;
  final Map<String, String> _formData;
  final bool isCredential;

  const TextFormFieldWithStyle({
    super.key,
    required this.fieldName,
    this.validator,
    required Map<String, String> formData,
    this.isCredential = false,
  }) : _formData = formData;

  @override
  State<TextFormFieldWithStyle> createState() => _TextFormFieldWithStyleState();
}

class _TextFormFieldWithStyleState extends State<TextFormFieldWithStyle> {
  late bool _showField;

  @override
  void initState() {
    super.initState();
    _showField = !widget.isCredential;
  }

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      obscureText: !_showField,
      cursorColor: Colors.blue,
      decoration: InputDecoration(
        suffixIcon: widget.isCredential
            ? IconButton(
                icon: Icon(
                  _showField ? Icons.visibility : Icons.visibility_off,
                ),
                onPressed: () {
                  setState(() {
                    _showField = !_showField; // toggle _showPassword value
                  });
                },
              )
            : null,
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
      validator: widget.validator ??
          (value) {
            if (value == null || value.isEmpty) {
              return 'Please enter ${widget.fieldName}';
            }
            return null;
          },
      onSaved: (value) {
        widget._formData[widget.fieldName] = value!;
      },
    );
  }
}

class BuildFromHttpRequest extends StatefulWidget {
  final Future<http.Response> Function() httpRequest;
  final String? apiErrorMessageName;
  final Widget Function(dynamic) builderUsingResponseBody;

  const BuildFromHttpRequest({
    super.key,
    required this.httpRequest,
    this.apiErrorMessageName,
    required this.builderUsingResponseBody,
  });

  @override
  State<BuildFromHttpRequest> createState() => _BuildFromHttpRequestState();
}

class _BuildFromHttpRequestState extends State<BuildFromHttpRequest> {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: widget.httpRequest(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          if (snapshot.hasError) {
            return const Center(
              child: Text('An error occurred'),
            );
          }

          final response = snapshot.data as http.Response;
          if (response.statusCode != 200) {
            showErrorAlert(
                widget.apiErrorMessageName ??
                    " API return unsuccessful response",
                context);
          }
          return widget.builderUsingResponseBody(jsonDecode(response.body));
        } else {
          return const Center(
            child: CircularProgressIndicator(),
          );
        }
      },
    );
  }
}

class IconButtonWithConfirm extends StatelessWidget {
  final String operationShort;
  final String operationPhrase;
  final Icon? icon;
  final Function()? operationExecution;

  const IconButtonWithConfirm({
    super.key,
    required this.operationShort,
    required this.operationPhrase,
    this.icon,
    this.operationExecution,
  });

  @override
  Widget build(BuildContext context) {
    return IconButtonWithHover(
      hoverText: operationShort,
      icon: icon ?? const Icon(Icons.delete),
      onPressed: () {
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text(operationShort),
              content: Text("Are you sure you want to $operationPhrase?"),
              actions: <Widget>[
                TextButton(
                  child: Text(operationShort),
                  onPressed: () {
                    Navigator.of(context).pop();
                    operationExecution?.call();
                  },
                ),
                TextButton(
                  child: const Text("Cancel"),
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
              ],
            );
          },
        );
      },
    );
  }
}

void clearAndShowSnackBarMsg(context, String message,
    {Color? bgColor, int duration = 3}) {
  ScaffoldMessenger.of(context).removeCurrentSnackBar();
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text(message),
      duration: Duration(seconds: duration),
      backgroundColor: bgColor,
    ),
  );
}

void waitAndShowSnackBarMsg(context, Future<bool> Function()? requestFunction,
    String successMessage, String errorMessage, bool successBack,
    {Function()? refreshFuncion}) async {
  showDialog(
    context: context,
    barrierDismissible: false,
    builder: (context) => const Center(
      child: CircularProgressIndicator(),
    ),
  );
  final success = await requestFunction?.call() ?? true;
  Navigator.pop(context);

  if (success) {
    clearAndShowSnackBarMsg(context, successMessage, bgColor: Colors.green);
    if (successBack) {
      Navigator.pop(context);
    }
    refreshFuncion?.call();
  } else {
    clearAndShowSnackBarMsg(context, errorMessage, bgColor: Colors.red);
  }
}

class ToggleSwitch extends StatefulWidget {
  final bool initialValue;
  final Function(bool) onToggle;

  const ToggleSwitch(
      {super.key, required this.initialValue, required this.onToggle});

  @override
  State<ToggleSwitch> createState() => _ToggleSwitchState();
}

class _ToggleSwitchState extends State<ToggleSwitch> {
  late bool _value;
  bool isToggling = false;

  @override
  void initState() {
    super.initState();
    _value = widget.initialValue;
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () async {
        if (!isToggling) {
          setState(() {
            isToggling = true;
          });
          widget.onToggle(!_value);
          setState(() {
            _value = !_value;
          });
          setState(() {
            isToggling = false;
          });
          // try {
          //   await widget.onToggle(!_value);
          //   setState(() {
          //     _value = !_value;
          //   });
          // } finally {
          //   setState(() {
          //     isToggling = false;
          //   });
          // }
        }
      },
      child: Container(
        width: 50.0,
        height: 30.0,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(15.0),
          color: _value ? Colors.green : Colors.grey,
        ),
        child: Stack(
          children: [
            Align(
              alignment: _value ? Alignment.centerRight : Alignment.centerLeft,
              child: Container(
                margin: const EdgeInsets.all(2.0),
                width: 25.0,
                height: 25.0,
                decoration: const BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.white,
                ),
              ),
            ),
            if (isToggling)
              Center(
                child: CircularProgressIndicator(),
              ),
            Positioned.fill(
              child: IgnorePointer(
                ignoring: !isToggling,
                child: Container(
                  color: Colors.transparent,
                ),
              ),
            ),
          ],
        ),

        // child: Align(
        //   alignment: _value ? Alignment.centerRight : Alignment.centerLeft,
        //   child: Container(
        //     margin: const EdgeInsets.all(2.0),
        //     width: 25.0,
        //     height: 25.0,
        //     decoration: const BoxDecoration(
        //       shape: BoxShape.circle,
        //       color: Colors.white,
        //     ),
        //   ),
        // ),
      ),
    );
  }
}
