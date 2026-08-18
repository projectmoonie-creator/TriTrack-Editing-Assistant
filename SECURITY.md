# Security Policy

## Supported versions

There is no published release yet. The local `0.1.0a0` scaffold is under
active development and receives security fixes on its current `main` branch.

## Report privately

After the public remote exists, use its private vulnerability-reporting
channel. If private reporting is unavailable, open a metadata-only issue that
asks the maintainers for a secure contact path. Do not include exploit details
or sensitive material in that issue.

Never attach or paste:

- source clips, audio, transcripts, or screenshots containing private media;
- API keys, cookies, signed URLs, model credentials, or environment dumps;
- absolute home, volume, or production paths;
- proprietary Motion templates, fonts, Final Cut libraries, or project files.

Use an invented fixture or the sanitized `doctor` receipt when reproduction
evidence is needed. The maintainer source and archive gates reject private home
paths, credential assignments, private-key headers, forbidden binary surfaces,
and unsafe archive structure without echoing the matching content. Omit
sensitive diagnostic attachments rather than redacting them by hand.

## Scope

Security reports may cover local command execution, unsafe path handling,
credential disclosure, unexpected network behavior, destructive overwrite,
media disclosure, dependency integrity, or generated-file vulnerabilities.
General support and feature requests belong in ordinary issues after the
public remote exists.
