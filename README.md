# AUTOPEON-V1

# AutoPeonv1.0

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/4690e751-1831-4a8f-8960-62f12a9bff79" />


**AutoPeon** is a comprehensive Python-based reconnaissance automation toolkit for bug bounty hunters and penetration testers. It streamlines subdomain discovery, vulnerability scanning, historical URL gathering, OSINT dork generation, and integrations with platforms like Shodan, ZoomEye, Hunter.io, and PublicWWW.

> Coded by: **Subir Sutradhar**  
> Inspired by original bash workflow from: **Riya Nair**


## 🎯 Features

- Subdomain enumeration using [Subfinder](https://github.com/projectdiscovery/subfinder)
- Live host detection using [HTTPX](https://github.com/projectdiscovery/httpx)
- Vulnerability scanning via [Nuclei](https://github.com/projectdiscovery/nuclei)
- DAST scans with custom templates
- Passive recon with [WaybackURLs](https://github.com/tomnomnom/waybackurls)
- OSINT footprinting via:
  - ✅ Google & GitHub dorks
  - ✅ Shodan IP discovery
  - 🔜 ZoomEye, Hunter.io, PublicWWW (to be added in next versions)
- Clean CLI output with [Colorama](https://pypi.org/project/colorama)

---

## ⚙️ Requirements

Install the required Python packages: like colorama, subprocess, httpx, subfinder, nuclei, waybackURLS, Shodan (will require API Key), if you have specific DAST templates add to it -t or --templates

For Shodan API: shodan init <your_api_key>


# Will develop with more power in next version

**Usage**: python3 recon-v1.py -u example.com
**Usage 2**: (if you have nuclei DAST templates) python3 autorecon.py -u example.com -t ~/nuclei-templates/


#Credits
Thanks Riya Nair – Original bash workflow inspiration

Subir Sutradhar – Python version, automation, formatting

