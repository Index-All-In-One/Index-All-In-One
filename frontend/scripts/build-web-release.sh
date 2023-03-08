#!/bin/bash

if [ -z "$FLUTTER_BASE_URL" ]; then
  FLUTTER_BASE_URL="http://127.0.0.1:5235"
fi

# run this script from the root of frontend
flutter build web --release --dart-define=BASE_URL=$FLUTTER_BASE_URL
