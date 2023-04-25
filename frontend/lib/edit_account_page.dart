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
    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Account/Application'),
      ),
      body: SingleChildScrollView(
        child: Column(children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
            child: buildEditAccountForm(widget.pluginInstanceID),
          )
        ]),
      ),
    );
  }
}
