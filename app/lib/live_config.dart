// The endpoint is public configuration, never a LiveKit API secret.
bool validLiveEndpoint(String value) {
  final uri = Uri.tryParse(value);
  return uri != null && uri.scheme == 'https' && uri.host.isNotEmpty &&
      uri.userInfo.isEmpty && !uri.hasQuery && !uri.hasFragment;
}
