import 'package:flutter/material.dart';

class MySearchBar extends StatefulWidget {
  final String hintText;
  final Function(String) onSearch;

  const MySearchBar(
      {super.key, required this.hintText, required this.onSearch});

  @override
  State<MySearchBar> createState() => _MySearchBarState();
}

class _MySearchBarState extends State<MySearchBar> {
  final _searchController = TextEditingController();
  final _focusNode = FocusNode();

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: TextField(
        focusNode: _focusNode,
        autofocus: true,
        controller: _searchController,
        decoration: InputDecoration(
          hintText: widget.hintText,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          suffixIcon: IconButton(
            icon: const Icon(Icons.search),
            onPressed: () {
              widget.onSearch(_searchController.text);
            },
          ),
        ),
        onSubmitted: (String value) {
          widget.onSearch(value);
        },
        // onTap: () {
        //   showSearch(context: context, delegate: CustomSearchDelegate());
        // },
      ),
    );
  }
}
