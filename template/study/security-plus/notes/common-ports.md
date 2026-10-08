---
name: Common ports
description: Well-known ports worth knowing by heart, with their secure alternatives
metadata:
  type: reference
  tags: [study, security, networking]
  updated: YYYY-MM-DD
---

# Common ports

> Example note: replace with your own.

**Summary:** know the port, the protocol, and the secure replacement.

| Port | Protocol | Secure alternative |
|---|---|---|
| 21 | FTP | SFTP (22) or FTPS (990) |
| 22 | SSH / SFTP | (already encrypted) |
| 23 | Telnet | SSH (22) |
| 25 | SMTP | SMTP with STARTTLS (587) |
| 53 | DNS | DNS over TLS (853) / HTTPS |
| 80 | HTTP | HTTPS (443) |
| 389 | LDAP | LDAPS (636) |
| 3389 | RDP | RDP over a VPN or gateway |
