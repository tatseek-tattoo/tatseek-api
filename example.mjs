#!/usr/bin/env node
// One TatSeek request, with attribution and no image downloads. Node.js 18+.
const args = process.argv.slice(2);
const composition = args.includes('--composition');
const query = args.filter(value => value !== '--composition').join(' ') || 'fine line rose';
const params = composition
  ? { style: 'realism', subject: 'portrait', min_share: '50', min_conf: 'high', limit: '2' }
  : { q: query, limit: '2' };
const url = new URL(`https://tatseek.com/api/v1/${composition ? 'tattoos' : 'search'}`);
url.search = new URLSearchParams(params).toString();
function resultLink(value) {
  try {
    const link = new URL(value);
    return link.protocol === 'https:' && link.hostname === 'tatseek.com' ? link.href : null;
  } catch { return null; }
}
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 20_000);
try {
  const response = await fetch(url, {
    signal: controller.signal,
    headers: { Accept: 'application/json', 'User-Agent': 'TatSeek-GitHub-example/1.0' }
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}${response.status === 429
      ? `; slow down; Retry-After: ${response.headers.get('retry-after') || 'not supplied'}` : ''}`);
  }
  const data = await response.json();
  if (!data || !Array.isArray(data.tattoos)) throw new Error('Expected a tattoos array');
  console.log('Source: TatSeek — https://tatseek.com');
  console.log('Query:', url.href);
  console.log('Relaxed constraints:', JSON.stringify(data.understood?.dropped ?? []));
  if (!data.tattoos.length) console.log('No tattoo results; this is not a service error.');
  for (const item of data.tattoos) {
    console.log(`\n${item.title || 'Untitled tattoo'}`);
    console.log('TatSeek page:', resultLink(item.url) || '(not supplied)');
    console.log('Artist:', item.artist?.name || '(not supplied)', resultLink(item.artist?.url) || '');
    console.log('Studio:', item.studio?.name || '(not supplied)', resultLink(item.studio?.url) || '');
    console.log('Composition source:', item.composition?.source || '(unknown)');
    console.log('Lead subject:', item.main_subject?.tier === 'lead'
      ? item.main_subject.slug : '(not established)');
  }
} catch (error) {
  console.error('TatSeek request failed:', error.message);
  process.exitCode = 1;
} finally {
  clearTimeout(timeout);
}
