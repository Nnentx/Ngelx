import test from 'node:test';
import assert from 'node:assert/strict';
import {
  captionMediaCandidates,
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
