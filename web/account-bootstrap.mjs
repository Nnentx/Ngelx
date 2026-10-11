try {
  await import('./account-pages.mjs');
} catch (_) {
  const status=document.getElementById('status');
  status.hidden=false;status.className='status error';
  status.textContent='Hesap hizmeti yüklenemedi. İnternet bağlantını kontrol edip sayfayı yenile.';
}
