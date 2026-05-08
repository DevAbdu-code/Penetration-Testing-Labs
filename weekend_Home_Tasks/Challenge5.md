# Advanced Reconnaissance CTF — Complete Notes & Documentation
> Comprehensive OSINT, DNS, Enumeration, Fingerprinting & Attack Surface Mapping Notes  
> Prepared by Abdu  
> Platform: Kali Linux  
> Targets: bugcrowd.com, scanme.nmap.org, zonetransfer.me, testphp.vulnweb.com

---

#  Table of Contents

1. Introduction
2. What is Reconnaissance?
3. Passive vs Active Recon
4. Important Definitions
5. Tools Used
6. Challenge 01 — Certificate Transparency Recon
7. Challenge 02 — Passive DNS & WHOIS Recon
8. Challenge 03 — OSINT, Archives & ASN Mapping
9. Challenge 04 — Subdomain Takeover Analysis
10. Challenge 05 — Full Port Scan & Service Fingerprinting
11. Challenge 06 — Web Fingerprinting & Directory Enumeration
12. Challenge 07 — DNS Enumeration & Zone Transfer
13. Challenge 08 — Full Attack Surface Mapping
14. Important Lessons Learned
15. Common Mistakes
16. Professional Recon Workflow
17. Final Conclusion

---

#  1. Introduction

Reconnaissance (Recon) is the process of gathering information about a target before performing deeper security testing.

The main goal is:
- Discover assets
- Understand infrastructure
- Identify technologies
- Detect exposures
- Map attack surface

Recon is the foundation of:
- Penetration Testing
- Bug Bounty Hunting
- Red Teaming
- Threat Intelligence
- Security Auditing

---

#  2. What is Reconnaissance?

Reconnaissance is divided into two major categories:

| Type | Description |
|---|---|
| Passive Recon | Collecting information WITHOUT directly interacting with target infrastructure |
| Active Recon | Direct interaction with target systems |

---

#  Passive Recon

Passive recon avoids direct communication with the target.

Examples:
- CT logs
- WHOIS
- Shodan
- Wayback Machine
- GitHub leaks
- ASN lookup
- Passive DNS

Advantages:
- Stealthy
- Hard to detect
- Safe

Disadvantages:
- Limited data
- Sometimes outdated

---

#  Active Recon

Active recon directly touches the target.

Examples:
- Nmap scans
- DNS brute force
- Gobuster
- FFUF
- Nikto
- Dirsearch

Advantages:
- Real-time results
- More accurate
- Finds live services

Disadvantages:
- Detectable
- Can trigger IDS/IPS
- Must be authorized

---

#  3. Important Definitions

##  Subdomain
A subdivision of a domain.

Examples:
api.bugcrowd.com
docs.bugcrowd.com
login.bugcrowd.com
---

##  Certificate Transparency (CT)
Public logs of SSL/TLS certificates.

Used to discover:
- Hidden subdomains
- Historical infrastructure
- Wildcard certificates

---

##  Wildcard Certificate
A certificate valid for all subdomains.

Example:
*.bugcrowd.com
Meaning:
api.bugcrowd.com
mail.bugcrowd.com
test.bugcrowd.com
can all use the same certificate.

---

##  ASN (Autonomous System Number)
A unique identifier assigned to networks on the internet.

Example:
AS54113 = Fastly, Inc.
Used for:
- Infrastructure mapping
- IP range analysis
- CDN identification

---

##  CNAME Record
A DNS alias pointing one domain to another.

Example:
blog.bugcrowd.com → j.sni.global.fastly.net
Used for:
- CDN hosting
- Cloud services
- Third-party integrations

---

##  MX Record
Mail Exchange records.

Used to identify:
- Email providers
- Mail infrastructure

Example:
aspmx.l.google.com
→ Google Workspace

---

##  DNS Zone Transfer (AXFR)
A DNS server transferring all zone records.

Misconfigured AXFR can expose:
- Internal hosts
- VPNs
- Test systems
- Mail servers

---

##  Fingerprinting
Identifying:
- Server software
- Operating system
- Frameworks
- Technologies

---

#  4. Tools Used

| Tool | Purpose |
|---|---|
| curl | HTTP requests |
| jq | JSON parsing |
| grep | Filtering text |
| sed | Stream editing |
| awk | Text processing |
| sort | Deduplication |
| uniq | Remove duplicates |
| subfinder | Passive subdomain enumeration |
| dig | DNS querying |
| host | DNS resolution |
| whois | Domain registration info |
| dnsrecon | DNS enumeration |
| ffuf | Fuzzing |
| gobuster | Enumeration |
| nmap | Port scanning |
| crt.sh | CT logs |
| Wayback Machine | Historical archives |
| bgp.he.net | ASN mapping |
| Shodan | Internet device search |

---

#  CHALLENGE 01 — Certificate Transparency Recon

##  Goal
Use CT logs to enumerate subdomains.

---

# 🔍 Why CT Logs?

Certificates publicly expose:
- Internal assets
- Forgotten systems
- Wildcard domains

---

#  Tools Used
- crt.sh
- subfinder
- grep
- sed
- sort

---

#  Main Commands

## Extract CT Subdomains
curl -s -A "Mozilla/5.0" "https://crt.sh/?q=%25.bugcrowd.com&output=json" \
| sed 's/},{/}\n{/g' \
| grep -o '"name_value":"[^"]*"' \
| cut -d'"' -f4 \
| tr '\\n' '\n' \
| sort -u
---

## Passive Enumeration with Subfinder
subfinder -d bugcrowd.com -silent -all | sort -u > subfinder.txt
---

## Merge & Deduplicate
cat crt_clean.txt subfinder.txt \
| sed 's/\*\.//g' \
| sort -u > final_subdomains.txt
---

#  Findings
- 84 unique subdomains
- Wildcard certificates discovered
- Multiple CDN-backed assets

---

#  Lessons Learned
- CT logs can expose hidden infrastructure
- Wildcards may indicate large environments
- Deduplication is critical

---

#  CHALLENGE 02 — Passive DNS & WHOIS Recon

##  Goal
Map DNS infrastructure without active interaction.

---

#  Tools Used
- dig
- whois
- dns.google
- subfinder

---

#  MX Record Lookup
curl -s "https://dns.google/resolve?name=bugcrowd.com&type=MX"
---

#  WHOIS Lookup
whois bugcrowd.com
---

#  Findings

## Email Provider
Google Workspace
## Registrar
Gandi SAS
## Expiration
2029-09-01
## Nameservers
NS-1430.AWSDNS-50.ORG
NS-2026.AWSDNS-61.CO.UK
NS-204.AWSDNS-25.COM
NS-945.AWSDNS-54.NET
---

#  Lessons Learned
- MX records reveal email providers
- WHOIS reveals ownership details
- CNAMEs identify third-party dependencies

---

#  CHALLENGE 03 — OSINT, Archives & ASN

##  Goal
Map infrastructure through:
- Archives
- ASN data
- Historical exposure

---

#  Tools Used
- Wayback Machine
- bgp.he.net
- dig
- curl

---

#  ASN Discovery

## Result
AS54113 — Fastly, Inc.
---

#  Historical Endpoint Discovery
curl -s "https://web.archive.org/cdx/search/cdx?url=bugcrowd.com/*&output=txt&collapse=urlkey" \
| grep -E "/login|/dashboard|/user|/account|/api"
---

#  Historical Endpoint Found
/api/v1/authn
---

#  Lessons Learned
- Archives expose historical attack surfaces
- ASN mapping reveals CDN usage
- Historical APIs may leak old logic

---

#  CHALLENGE 04 — Subdomain Takeover Analysis

##  Goal
Identify takeover opportunities.

---

#  What is Subdomain Takeover?

Occurs when:
- A DNS record points to an unclaimed service

Example:
sub.example.com → github.io
If unclaimed:
- Attackers can register the resource
- Hijack the subdomain

---

#  Tools Used
- dig
- grep
- CNAME analysis

---

#  Example CNAME Targets
cloudfront.net
fastly.net
okta.com
sendgrid.net
---

#  Risk Levels

| Level | Meaning |
|---|---|
| HIGH | Unclaimed service |
| MEDIUM | Claimable with authentication |
| LOW | Verified active ownership |

---

#  Lessons Learned
- Third-party integrations increase attack surface
- Continuous DNS auditing is critical

---

#  CHALLENGE 05 — Full Port Scan & Fingerprinting

##  Goal
Enumerate services and detect operating systems.

---

#  Tools Used
- nmap

---

#  TCP Scan
nmap -sS -sV -O scanme.nmap.org -T5
---

#  Open Ports Found
22/tcp
80/tcp
3333/tcp
9929/tcp
31337/tcp
---

#  SSH Version
OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13
---

#  Web Server
Apache httpd 2.4.7
---

#  OS Detection
Linux
---
#  UDP Scan
sudo nmap -sU --top-ports 100 scanme.nmap.org
---

#  Lessons Learned
- Full scans take time
- UDP scans are slower
- OS detection depends on response quality

---

#  CHALLENGE 06 — Web Fingerprinting

##  Goal
Identify:
- Web technologies
- Directories
- Missing headers

---

#  Tools Used
- curl
- gobuster
- ffuf
- nikto

---

#  Important Security Headers

| Header | Purpose |
|---|---|
| CSP | Prevent XSS |
| HSTS | Force HTTPS |
| X-Frame-Options | Prevent clickjacking |
| X-Content-Type-Options | Prevent MIME confusion |

---

#  Lessons Learned
- Missing headers increase attack surface
- Fingerprinting reveals backend stack

---

#  CHALLENGE 07 — DNS Enumeration & AXFR

##  Goal
Perform active DNS enumeration.

---

#  Tools Used
- dig
- dnsrecon
- ffuf
- gobuster

---

#  Zone Transfer
dig axfr zonetransfer.me @nsztm1.digi.ninja
---

#  Records Found
52 records
---

#  SOA Administrator
robin.digi.ninja
---

#  DNS Brute Force
dnsrecon -d zonetransfer.me -t brt -D subdomains-top1million-5000.txt
---

#  Lessons Learned
- Misconfigured AXFR leaks internal infrastructure
- DNS brute force reveals hidden hosts

---

#  CHALLENGE 08 — Full Attack Surface Mapping

##  Goal
Combine all findings into one structured report.

---

#  Top Findings

## 1. Large Attack Surface
Many public subdomains discovered.

Risk:
- Increased exposure
- Forgotten systems

---

## 2. Third-Party Dependencies
Fastly, Okta, CloudFront, Outreach, SendGrid.

Risk:
- Supply-chain exposure
- Misconfiguration risk

---

## 3. Historical API Exposure
Historical endpoints indexed publicly.

Risk:
- Legacy functionality exposure
- Authentication weaknesses

---

#  Recommended Mitigations

## 1. Continuous Asset Inventory
Track all subdomains continuously.

---

## 2. Remove Legacy Endpoints
Delete unused APIs and historical systems.

---

## 3. DNS Auditing
Review:
- CNAMEs
- Wildcards
- Third-party integrations

---

#  Common Mistakes

| Mistake | Problem |
|---|---|
| Using browser instead of DNS checks | 404 ≠ dead |
| Not deduplicating | Incorrect counts |
| Dirty parsing | False subdomains |
| Aggressive scanning | IDS alerts |

---

#  Professional Recon Workflow

1. Passive Recon
2. Data Cleaning
3. Deduplication
4. Validation
5. Active Enumeration
6. Fingerprinting
7. Risk Analysis
8. Reporting
---

#  Final Conclusion

This project demonstrated how reconnaissance combines:
- OSINT
- DNS analysis
- Enumeration
- Fingerprinting
- Historical analysis
- Infrastructure mapping

Key understanding:
> Reconnaissance is not only collecting data —
> it is understanding relationships between assets,
> technologies, risks, and exposure.

The most important lesson:
Clean data + correct interpretation
is more valuable than massive data volume.
---

# 🏁 End of Notes
