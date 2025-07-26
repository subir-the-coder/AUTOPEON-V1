#!/usr/bin/env python3

import os
import subprocess
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

# ──────────────────────────────
# AutoRecon (Python Version)
# Coder: Subir Sutradhar
# Bash Script Inspiration: Riya Nair
# ──────────────────────────────

def banner():
    print(Fore.GREEN + r"""
     █████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗
    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝██╔═══██╗████╗  ██║
    ███████║██║   ██║   ██║   ██║   ██║██████╔╝█████╗  ██║   ██║██╔██╗ ██║
    ██╔══██║██║   ██║   ██║   ██║   ██║██╔═══╝ ██╔══╝  ██║   ██║██║╚██╗██║
    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║     ███████╗╚██████╔╝██║ ╚████║
    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝

                AutoRecon - A Bug Bounty Recon Toolkit | v1.0
                Coder: Subir Sutradhar | Credits: Riya Nair
    """ + Style.RESET_ALL)

def run_command(description, command, output_path=None, check_file=None):
    print(f"{Fore.CYAN}[+] {description}{Style.RESET_ALL}")
    try:
        if check_file and (not os.path.exists(check_file) or os.path.getsize(check_file) == 0):
            print(Fore.YELLOW + f"[!] Skipped: {description} (missing or empty file: {check_file})")
            return
        if output_path:
            with open(output_path, "w") as f:
                subprocess.run(command, shell=True, check=True, stdout=f, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(Fore.RED + f"[!] Failed: {description}")

def main():
    parser = argparse.ArgumentParser(description="AutoRecon - Subdomain + Vuln + OSINT Recon Tool")
    parser.add_argument("-u", "--url", help="Target domain", required=True)
    parser.add_argument("-t", "--templates", help="Path to Nuclei templates for DAST scan", default="")
    args = parser.parse_args()
    domain = args.url
    templates_path = args.templates.rstrip("/")

    output_dir = f"{domain}-recon"
    os.makedirs(output_dir, exist_ok=True)

    banner()

    print(f"{Fore.GREEN}[+] Target: {domain}{Style.RESET_ALL}")

    # Recon steps
    run_command("Running Subfinder...", f"subfinder -d {domain}", output_path=f"{output_dir}/subdomains.txt")
    run_command("Running HTTPX...", f"cat {output_dir}/subdomains.txt | httpx -silent", output_path=f"{output_dir}/httpx.txt", check_file=f"{output_dir}/subdomains.txt")
    run_command("Running Nuclei (main scan)...", f"nuclei -l {output_dir}/httpx.txt -o {output_dir}/nuclei-output.txt", check_file=f"{output_dir}/httpx.txt")
    run_command("Fetching Wayback URLs...", f"waybackurls {domain}", output_path=f"{output_dir}/wayback.txt")

    # DAST Templates must be provided if user wants DAST scan
    if templates_path and os.path.exists(templates_path):
        run_command("Running Nuclei DAST on Wayback URLs...",
                    f"nuclei -l {output_dir}/wayback.txt -t {templates_path} -o {output_dir}/dast-result.txt",
                    check_file=f"{output_dir}/wayback.txt")
    else:
        print(Fore.YELLOW + "[!] Skipping DAST scan — template path not found.")

    # SHODAN Step (API Key will be required)
    shodan_out = f"{output_dir}/shodan.txt"
    try:
        run_command("Searching Shodan for domain IPs...",
                    f"shodan search \"ssl:'{domain}'\" --fields ip_str --limit 1000",
                    output_path=shodan_out)
    except Exception as e:
        print(Fore.RED + f"[!] Failed: Shodan search ({e})")

    run_command("Running Nuclei on Shodan IPs...",
                f"nuclei -l {shodan_out} -o {output_dir}/ip-nuclei.txt", check_file=shodan_out)

    # Dork Links
    print(f"{Fore.YELLOW}[+] Google Dorking Links:{Style.RESET_ALL}")
    google_dorks = [
        f"https://www.google.com/search?q=site:{domain}+ext:env+OR+ext:log+OR+ext:bak+OR+ext:sql",
        f"https://www.google.com/search?q=site:{domain}+inurl:admin+OR+inurl:login",
        f"https://www.google.com/search?q=site:{domain}+intitle:index.of",
        f"https://www.google.com/search?q=site:{domain}+ext:xml+OR+ext:json+OR+ext:conf",
        f"https://www.google.com/search?q=site:{domain}+inurl:wp-content+OR+inurl:wp-admin",
        f"https://www.google.com/search?q=site:{domain}+ext:git+OR+ext:svn"
    ]
    with open(f"{output_dir}/google-dorks.txt", "w") as f:
        f.write("\n".join(google_dorks))
    print("\n".join(google_dorks))

    print(f"{Fore.YELLOW}[+] GitHub Dorking Links:{Style.RESET_ALL}")
    github_dorks = [
        f"https://github.com/search?q={domain}",
        f"https://github.com/search?q={domain}+password",
        f"https://github.com/search?q={domain}+secret",
        f"https://github.com/search?q={domain}+api_key"
    ]
    with open(f"{output_dir}/github-dorks.txt", "w") as f:
        f.write("\n".join(github_dorks))
    print("\n".join(github_dorks))

    print(f"{Fore.GREEN}[✓] Recon complete! All results saved in: {output_dir}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
