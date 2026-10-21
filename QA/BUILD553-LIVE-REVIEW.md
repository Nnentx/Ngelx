# Build553 live review

Baseline: Build552 / 1.0.322, commit 8686e01dc84d66e0e117b54c35f915a6600cb93d.

49910.mp4 (161 seconds) and 49917.mp4 (230 seconds) successfully decode. Sampled frames show comments over the main video, a large guest status panel, and a crowded composer/action row. Live screen has no keepScreenOn lifecycle handling, unlike the call screen.

Changes: live-specific screen ownership on Android, release on pause/exit/end, preserve RTC across inactive system overlays, adaptive action wrapping, scrollable bounded footer, smaller comments viewport, hide guest panel behind keyboard.

Audio stream presence and signal levels were inspected; audio has NOT been listened to or transcribed. Echo/dropouts and two-device audio remain unverified. No speculative audio routing changes.

Validation required: Flutter layout tests, existing Build552 regression suite, full analysis, release compilation and signer/version verification. Physical-device idle timeout, volume keys, host/guest audio, keyboard and landscape remain pending.

LOSTRA and Firebase deployments are excluded.
