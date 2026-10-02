import test from 'node:test';
import assert from 'node:assert/strict';
import {
  captionMediaCandidates,
  captionTranscriptionAttempts,
  detectTranslationSource,
  normalizeLanguageCode,
} from '../src/content_tools.js';

test('legacy content language detection keeps explicit language', () => {
  assert.equal(detectTranslationSource('Testing', 'tr-TR'), 'tr');
  assert.equal(normalizeLanguageCode('English'), 'en');
});

test('legacy content language detection handles supported scripts', () => {
  assert.equal(detectTranslationSource('Testing a video', ''), 'en');
  assert.equal(detectTranslationSource('Bu dünya çok güzel', ''), 'tr');
  assert.equal(detectTranslationSource('Das ist für dich', ''), 'de');
  assert.equal(detectTranslationSource('Привет мир', ''), 'ru');
  assert.equal(detectTranslationSource('مرحبا بالعالم', ''), 'ar');
});

test('caption media candidates are ordered, unique and bounded', () => {
  const urls = captionMediaCandidates({
    mediaUrl: 'https://ngelx-media.example/video.mp4',
    mediaUrls: [
      'https://ngelx-media.example/video.mp4',
      'https://ngelx-upload.example/video.mp4',
      '',
    ],
  });
  assert.deepEqual(urls, [
    'https://ngelx-media.example/video.mp4',
    'https://ngelx-upload.example/video.mp4',
  ]);
});


test('caption transcription retries with a relaxed second pass', () => {
  const attempts = captionTranscriptionAttempts('tr-TR');
  assert.equal(attempts.length, 2);
  assert.equal(attempts[0].language, 'tr');
  assert.equal(attempts[0].vad_filter, true);
  assert.equal(attempts[0].no_speech_threshold, 0.80);
  assert.equal('language' in attempts[1], false);
  assert.equal(attempts[1].vad_filter, false);
  assert.equal(attempts[1].no_speech_threshold, 0.95);
});
