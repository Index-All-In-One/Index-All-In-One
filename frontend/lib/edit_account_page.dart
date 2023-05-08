import 'package:flutter/material.dart';
import 'build_edit_account_form.dart';

class EditAccountInfoPage extends StatefulWidget {
  final String pluginInstanceID;
  const EditAccountInfoPage({super.key, required this.pluginInstanceID});

  @override
  State<EditAccountInfoPage> createState() => _EditAccountInfoPageState();
}

class _EditAccountInfoPageState extends State<EditAccountInfoPage> {
  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final double maxWidth = (screenWidth >= 1250) ? screenWidth * 0.4 : 500;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Account/Application'),
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
            constraints: BoxConstraints(maxWidth: maxWidth),
            child: buildEditAccountForm(widget.pluginInstanceID),
          ),
        ),
      ),
    );
  }
}
