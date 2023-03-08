#!/bin/bash

# set up environment variables
FLUTTER_BASE_URL=${FLUTTER_BASE_URL:-"http://127.0.0.1:5235"}

# run this script from the root of frontend
flutter build web --release --dart-define=BASE_URL=$FLUTTER_BASE_URL
