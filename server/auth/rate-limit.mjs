import {createHmac} from 'node:crypto';
import {isIP} from 'node:net';
import {LoginFailure, parseIdentifier} from './identifier-login.mjs';

function networkIdentity(raw) {
  if (typeof raw !== 'string' || !isIP(raw)) throw new LoginFailure('unavailable');
  if (isIP(raw) === 6) {
    const canonical = new URL('http://[' + raw + ']').hostname;
    // Collapse IPv4-mapped IPv6 so one IPv4 address cannot use two counters.
    const mapped = canonical.match(/^\[::ffff:([0-9a-f]+):([0-9a-f]+)\]$/);
    if (mapped) {
      const n = (BigInt('0x' + mapped[1]) << 16n) + BigInt('0x' + mapped[2]);
      return [24n,16n,8n,0n].map(b => Number((n >> b) & 255n)).join('.');
    }
    return canonical;
  }
  return raw;
}

export function createFirestoreRateLimiter({db, secret, now = Date.now,
    windowMs = 60000, identifierLimit = 5, networkLimit = 30}) {
  if (typeof db?.runTransaction !== 'function' || typeof secret !== 'string' ||
      Buffer.byteLength(secret) < 32 || typeof now !== 'function' ||
      !Number.isSafeInteger(windowMs) || windowMs < 1000 || windowMs > 3600000 ||
      !Number.isSafeInteger(identifierLimit) || identifierLimit < 1 ||
      !Number.isSafeInteger(networkLimit) || networkLimit < 1) {
    throw new LoginFailure('unavailable');
  }
  const key = (scope, value) => scope + '-' +
    createHmac('sha256', secret).update(scope + '\0' + value).digest('hex');
  return async (identifier, context) => {
    const parsed = parseIdentifier(identifier?.value);
    if (parsed.kind !== identifier?.kind || parsed.value !== identifier?.value) {
      throw new LoginFailure();
    }
    // This field MUST be supplied by the deployment's trusted request adapter,
    // never a body value or an unvalidated X-Forwarded-For header.
    const network = networkIdentity(context?.trustedRemoteAddress);
    const instant = now();
    if (!Number.isSafeInteger(instant) || instant < 0) throw new LoginFailure('unavailable');
    const refs = [
      db.collection('login_attempt_limits').doc(key('identifier', parsed.kind + ':' + parsed.value)),
      db.collection('login_attempt_limits').doc(key('network', network)),
    ];
    try {
      await db.runTransaction(async tx => {
        const records = [];
        // All reads precede any writes; retry callbacks have no external effect.
        for (const ref of refs) records.push(await tx.get(ref));
        const counts = records.map(record => {
          if (!record.exists) return {count:0, startedAtMs:instant};
          const data = record.data();
          if (!Number.isSafeInteger(data?.count) || data.count < 0 ||
              !Number.isSafeInteger(data?.startedAtMs) || data.startedAtMs < 0 ||
              data.startedAtMs > instant) throw new LoginFailure('unavailable');
          return instant - data.startedAtMs >= windowMs
            ? {count:0, startedAtMs:instant} : data;
        });
        if (counts[0].count >= identifierLimit || counts[1].count >= networkLimit) {
          throw new LoginFailure('too-many-requests');
        }
        counts.forEach((data, i) => tx.set(refs[i], {
          count:data.count + 1, startedAtMs:data.startedAtMs,
          // TTL deletion is optional housekeeping, never the enforcement clock.
          expiresAt:new Date(data.startedAtMs + windowMs * 2),
        }));
      });
    } catch (error) {
      if (error instanceof LoginFailure) throw error;
      // A failed counter write cannot grant an uncounted authentication attempt.
      throw new LoginFailure('unavailable');
    }
  };
}
