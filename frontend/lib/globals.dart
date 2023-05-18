library my_project.globals;

const String apiBaseUrl =
    String.fromEnvironment('BASE_URL', defaultValue: "https://localhost:5235");

// set --dart-define=GOAUTH_CLIENT_ID=xxx in flutter run or build web --release
const String gOAuthClientId =
    String.fromEnvironment('GOAUTH_CLIENT_ID', defaultValue: "");
