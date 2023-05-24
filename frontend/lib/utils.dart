import 'package:flutter/material.dart';
import 'package:clipboard/clipboard.dart';
import 'package:intl/intl.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'globals.dart' as globals;

Future<void> googleOAuth(String pluginInstanceID, String? pluginName,
    String scope, Function onError) async {
  if (globals.gOAuthClientId == "") {
    onError("Set a Google Drive Client ID first to use this feature.");
    return;
  }

  const String clientId = globals.gOAuthClientId;
  const String redirectUri = '${globals.apiBaseUrl}/GOAuthCB';

  final String state = jsonEncode({
    'id': pluginInstanceID,
    if (pluginName != null) 'plugin_name': pluginName,
    'redirect_uri': redirectUri,
  });

  final authUrl = Uri.https('accounts.google.com', '/o/oauth2/v2/auth', {
    'client_id': clientId,
    'redirect_uri': redirectUri,
    'scope': scope,
    'response_type': 'code',
    'access_type': 'offline',
    'prompt':
        'consent', // Forces the consent screen to show, thus creating a new refresh token.
    'state': state,
  });

  if (await canLaunchUrl(authUrl)) {
    await launchUrl(authUrl);
  } else {
    onError('Could not launch $authUrl');
  }
}

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

class LinkTextButtonWithHover extends StatelessWidget {
  final String link;

  const LinkTextButtonWithHover({
    super.key,
    required this.link,
  });

  @override
  Widget build(BuildContext context) {
    String truncatedText =
        link.length > 50 ? '${link.substring(0, 50)}...' : link;
    return TextButtonWithHover(
      hoverText: link,
      text: truncatedText,
      onPressed: () => launchUrl(Uri.parse(link), webOnlyWindowName: '_blank'),
    );
  }
}

class TextButtonWithHover extends StatelessWidget {
  final String hoverText;
  final String text;
  final Function() onPressed;

  const TextButtonWithHover({
    super.key,
    required this.hoverText,
    required this.text,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: hoverText,
      child: TextButton(
        onPressed: onPressed,
        child: Text(
          text,
          style:
              const TextStyle(color: Colors.green, fontStyle: FontStyle.italic),
        ),
      ),
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

String formatFileSize(String fileSizeOrigin) {
  int? fileSizeInt = int.tryParse(fileSizeOrigin);
  if (fileSizeInt == null) {
    return fileSizeOrigin;
  } else {
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

String? pluginInfoFieldTypeValidator(value, type, fieldDisplayName) {
  switch (type) {
    case 'int':
      if (value == null || value.isEmpty) {
        return 'Please enter $fieldDisplayName';
      }
      if (int.tryParse(value) == null) {
        return 'Please enter a valid integer for $fieldDisplayName';
      }
      break;
    case 'two_step':
      //TODO: add two_step validation for submit
      break;
    case 'secret_opt':
      // secret_opt can be empty
      break;
    default:
      if (value == null || value.isEmpty) {
        return 'Please enter $fieldDisplayName';
      }
      break;
  }
  return null;
}

typedef FieldMap = Map<String, String>;
typedef FormSegment = Map<String, dynamic>;

class FormWithSubmit extends StatefulWidget {
  final Future<bool> Function(Map<String, String> formData)? onSubmit;
  final Future<bool> Function(Map<String, String> formData)? onSendCode;
  final String? successMessage;
  final List<FormSegment> formSegments;
  final String pluginInstanceID;
  final String? pluginName;

  const FormWithSubmit({
    super.key,
    this.onSubmit,
    this.onSendCode,
    this.successMessage,
    required this.formSegments,
    this.pluginInstanceID = "empty_plugin_instance_id",
    this.pluginName,
  });

  @override
  State<FormWithSubmit> createState() => _FormWithSubmitState();
}

class _FormWithSubmitState extends State<FormWithSubmit> {
  final _formKey = GlobalKey<FormState>();
  final Map<String, String> _formData = {};
  final Map<String, String> _formDataTwoStep = {};

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          for (var segment in widget.formSegments) ...[
            Padding(
                padding: const EdgeInsets.symmetric(vertical: 6),
                child: Text(
                  segment['title'],
                  style: const TextStyle(fontSize: 18),
                )),
            if (segment['hint'] != null)
              Padding(
                  padding: const EdgeInsets.symmetric(vertical: 6),
                  child: Text(
                    "Hint: ${segment['hint']}",
                    style: TextStyle(fontSize: 16, color: Colors.grey[600]),
                  )),
            for (FieldMap field in segment['field_def']!) ...[
              Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Text(
                    field['display_name']!,
                    style: const TextStyle(fontSize: 16),
                  )),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: (field['type'] == 'g_oauth')
                    ? ElevatedButton(
                        child: const Text('Google Sign In'),
                        onPressed: () async {
                          await googleOAuth(widget.pluginInstanceID,
                              widget.pluginName, field['scope']!, (error) {
                            clearAndShowSnackBarMsg(context, error,
                                bgColor: Colors.red);
                          });
                        },
                      )
                    : TextFormFieldWithStyle(
                        fieldName: field['field_name']!,
                        formData: (field['type'] == 'two_step')
                            ? _formDataTwoStep
                            : _formData,
                        validator: (value) {
                          return pluginInfoFieldTypeValidator(
                              value, field['type']!, field['display_name']!);
                        },
                        isCredential: (field['type']! == 'secret') ||
                            (field['type']! == 'secret_opt'),
                        initialValue: field['value'] ?? '',
                        customButton: (field['type'] == 'two_step')
                            ? Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: ElevatedButton(
                                  onPressed: () async {
                                    if (_formKey.currentState!.validate()) {
                                      _formKey.currentState!.save();
                                      waitAndShowSnackBarMsg(
                                        context,
                                        () async {
                                          final success = await widget
                                                  .onSendCode
                                                  ?.call(_formData) ??
                                              true;
                                          return success;
                                        },
                                        'Sent code successfully',
                                        'An error occurred while sending the code',
                                        false,
                                      );
                                    }
                                  },
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.blue,
                                    padding: const EdgeInsets.symmetric(
                                        horizontal: 12, vertical: 6),
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                  ),
                                  child: const Text('Send Code'),
                                ),
                              )
                            : null,
                      ),
              ),
            ],
            const SizedBox(height: 16),
          ],
          const SizedBox(height: 10),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () async {
                if (_formKey.currentState!.validate()) {
                  _formKey.currentState!.save();
                  waitAndShowSnackBarMsg(
                    context,
                    () async {
                      final success = await widget.onSubmit
                              ?.call({..._formData, ..._formDataTwoStep}) ??
                          true;
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
                padding: const EdgeInsets.all(24),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                textStyle: const TextStyle(fontSize: 18),
              ),
              child: const Text('Submit'),
            ),
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
  final String initialValue;
  final Widget? customButton;

  const TextFormFieldWithStyle({
    super.key,
    required this.fieldName,
    this.validator,
    required Map<String, String> formData,
    this.isCredential = false,
    this.initialValue = "",
    this.customButton,
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
      initialValue: widget.initialValue,
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
            : (widget.customButton),
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
  final Widget? loadingWidget;

  const BuildFromHttpRequest({
    super.key,
    required this.httpRequest,
    this.apiErrorMessageName,
    required this.builderUsingResponseBody,
    this.loadingWidget,
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
              child: Text('An error occurred in http request'),
            );
          }

          final response = snapshot.data as http.Response;
          if (response.statusCode != 200) {
            showErrorAlert(
                "${widget.apiErrorMessageName ?? "unknown"} API return unsuccessful response",
                context);
          }
          return widget.builderUsingResponseBody(jsonDecode(response.body));
        } else {
          if (widget.loadingWidget != null) {
            return widget.loadingWidget!;
          } else {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }
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
