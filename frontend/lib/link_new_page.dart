import 'package:flutter/material.dart';
import 'api_list_plugins.dart';
import 'api_plugin_info_list.dart';

class LinkNewPage extends StatefulWidget {
  const LinkNewPage({super.key});

  @override
  State<LinkNewPage> createState() => _LinkNewPageState();
}

class _LinkNewPageState extends State<LinkNewPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Link New Account/Application'),
      ),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(vertical: 20),
            child: const Text(
              'Plugin List',
              style: TextStyle(fontSize: 16),
            ),
          ),
          Expanded(child: buildPluginList()),
        ],
      ),
    );
  }
}

class LinkNewInfoPage extends StatefulWidget {
  final String pluginName;
  const LinkNewInfoPage({super.key, required this.pluginName});

  @override
  State<LinkNewInfoPage> createState() => _LinkNewInfoPageState();
}

class _LinkNewInfoPageState extends State<LinkNewInfoPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Link New Account/Application'),
      ),
      body: Column(
        children: [
          Expanded(child: buildPluginInfoList(widget.pluginName)),
        ],
      ),
    );
  }
}
