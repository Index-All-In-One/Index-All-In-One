import 'package:flutter/material.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  Widget _currentAccountsWidget = ListView();
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
          // Row(
          //   mainAxisAlignment: MainAxisAlignment.center,
          //   children: [
          //     _currentAccountsWidget,
          //     ElevatedButton(
          //       child: const Text('Link New Account/Application'),
          //       onPressed: () {},
          //     ),
          //   ],
          // ),
        ],
      ),
    );
  }
}
