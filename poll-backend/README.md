# Secure Vita polls backend

Not deployed: publishing to GitHub Pages alone cannot receive votes. This endpoint needs an authenticated Cloudflare Worker deployment and GitHub Issue write access in a server-side secret. The credentials must never be embedded in a VPK or committed to the repository.

To configure: authenticate with wrangler login; copy wrangler.toml.example to wrangler.toml; deploy with wrangler; set GITHUB_TOKEN and VOTER_SALT via wrangler secret put; configure WOLFFS_POLL_API_URL for the site generator; rebuild site and Store catalogs.

The Vita sends only a stable, application-domain SHA-256 derivative of the OpenPSID; it never sends the raw 16-byte console ID. The server stores a separate per-poll HMAC for deduplication. Each accepted vote is durably queued and then written to a GitHub issue comment containing the option and timestamp but no identifier. GitHub audit retries after outage. Poll results are visible only after expiration.

Identity is best-effort: Vita lacks an online cryptographic device attestation that prevents deliberate impersonation. Keep this privacy and anti-abuse limitation visible when creating polls. The app must verify HTTPS certificates for vote POSTs; do not weaken TLS for voting.
