// Build538: isolated offline installation smoke-test entrypoint.
//
// DO NOT import the production main.dart, Firebase, LiveKit, or plugin services.
// This app intentionally tests only Flutter rendering and the Android package
// identity. Production and QA backend operations remain unavailable.
import 'package:flutter/material.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const NgelXQaSmokeApp());
}

class NgelXQaSmokeApp extends StatelessWidget {
  const NgelXQaSmokeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NgelX QA',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: const Color(0xFF7E57C2),
        scaffoldBackgroundColor: const Color(0xFFF8F7FC),
      ),
      home: const NgelXQaHome(),
    );
  }
}

class NgelXQaHome extends StatefulWidget {
  const NgelXQaHome({super.key});

  @override
  State<NgelXQaHome> createState() => _NgelXQaHomeState();
}

class _NgelXQaHomeState extends State<NgelXQaHome> {
  int _tapCount = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('NgelX QA'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 26, vertical: 20),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 450),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Icon(Icons.verified_user_outlined,
                      color: Color(0xFF6D3BBB), size: 74),
                  const SizedBox(height: 18),
                  const Text(
                    'NgelX QA açıldı',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Bu ayrı uygulama yalnızca kurulum ve açılış testidir. '
                    'Telefonundaki normal NgelX uygulaması korunur.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16, height: 1.4),
                  ),
                  const SizedBox(height: 22),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(18),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text('ÇEVRİMDIŞI GÜVENLİ TEST',
                              style: TextStyle(fontWeight: FontWeight.bold)),
                          SizedBox(height: 10),
                          Text('Giriş, mesajlaşma, Firebase ve canlı '
                              'görüşmeler henüz etkin değil.'),
                          SizedBox(height: 10),
                          Text('Sadece Android kurulumu, Flutter açılışı '
                              've ekrana dokunma davranışı kontrol edilir.'),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 18),
                  FilledButton.icon(
                    onPressed: () => setState(() => _tapCount++),
                    icon: const Icon(Icons.touch_app_outlined),
                    label: const Text('Ekran tepki testini çalıştır'),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _tapCount == 0
                        ? 'Düğmeye dokunarak ekranın çalıştığını doğrula.'
                        : 'Ekran tepki testi başarılı: $_tapCount',
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontWeight: FontWeight.w600),
                  ),
                  const SizedBox(height: 14),
                  const Text(
                    'QA Build538 • ARM64 • Çevrimdışı',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.black54),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
