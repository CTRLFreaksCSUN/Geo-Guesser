import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

void main() {
  runApp(const GeoVision());
}

class GeoVision extends StatelessWidget {
  const GeoVision({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.teal,
      ),
      home: const GeoVisionHome(),
    );
  }
}

class GeoVisionHome extends StatefulWidget {
  const GeoVisionHome({Key? key}) : super(key: key);

  @override
  State<GeoVisionHome> createState() => _GeoVisionHomeState();
}

class _GeoVisionHomeState extends State<GeoVisionHome> {
  PlatformFile? _imagePicked;
  Uint8List? _imageData;

  Future<void> _pickImage() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        dialogTitle: 'Select a photo to find the location',
        type: FileType.image,
      );

      if (result == null) return;

      setState(() {
        _imagePicked = result.files.first;
      });

      // Try to load the image data from bytes or read from the file path
      if (_imagePicked!.bytes != null) {
        setState(() {
          _imageData = _imagePicked!.bytes;
        });
      } else if (_imagePicked!.path != null) {
        // Read the file as bytes if the path is available
        final file = File(_imagePicked!.path!);
        setState(() {
          _imageData = file.readAsBytesSync();
        });
      } else {
        // Show an error if neither bytes nor path is available
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Failed to load image data.")),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (_imageData != null)
              Image.memory(
                _imageData!,
                width: 300,
                height: 300,
              )
            else if (_imagePicked != null)
              const Text("Image data could not be loaded."),
            ElevatedButton(
              child: const Text('Choose a picture'),
              onPressed: _pickImage,
            ),
          ],
        ),
      ),
    );
  }
}

