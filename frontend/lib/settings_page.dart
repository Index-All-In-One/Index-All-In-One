import 'package:flutter/material.dart';
import 'api_list_accounts.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: Column(
        // mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Center(
          //   child: Container(
          //     padding: const EdgeInsets.symmetric(vertical: 10),
          //     child: const Text(
          //       'Settings Page',
          //       style: TextStyle(fontWeight: FontWeight.bold),
          //     ),
          //   ),
          // ),
          // const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(vertical: 15),
            child: ElevatedButton(
              child: const Text('Link New Account/Application'),
              onPressed: () {},
            ),
          ),
          buildAccountList(),
        ],
      ),
    );
  }
}