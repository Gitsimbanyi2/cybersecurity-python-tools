# cybersecurity-python-tools

Small **defensive** Python tools: log analysis, IOC extraction, security reporting.

Run against the synthetic files in `samples/`. Do not pipe production SOC exports into a public clone.

```bash
python -m pip install -r requirements.txt
python tools/log_analyzer.py samples/synthetic_auth.log
python tools/ioc_extractor.py samples/synthetic_alert.txt
python tools/security_report.py samples/synthetic_auth.log --out /tmp/lab-report.md
```

| Tool | Job |
|------|-----|
| `tools/log_analyzer.py` | Count failed SSH lines by source IP |
| `tools/ioc_extractor.py` | Pull IPv4, domains, SHA256 from text |
| `tools/security_report.py` | Write a short markdown summary |

Lab IPs in samples are RFC 5737 (`203.0.113.88`, `192.0.2.20`).
