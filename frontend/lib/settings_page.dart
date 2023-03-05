import 'package:flutter/material.dart';
import 'build_account_list.dart';
import 'apis.dart';
import 'utils.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  Widget _accountListWidget = const Center(child: CircularProgressIndicator());

  void refreshAccountList() {
    setState(() {
      _accountListWidget = buildAccountList(refreshAccountList);
    });
  }

  @override
  void initState() {
    super.initState();
    _accountListWidget = buildAccountList(refreshAccountList);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: Column(
        // mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(vertical: 20),
            child: ElevatedButton(
              child: const Text('Link New Account/Application',
                  style: TextStyle(fontSize: 16)),
              onPressed: () {
                Navigator.pushNamed(context, '/link_new');
              },
            ),
          ),
          Expanded(child: _accountListWidget),
        ],
      ),
    );
  }
}
