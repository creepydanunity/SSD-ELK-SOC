# Deploying SOC with ELK-based SIEM

## Innopolis University, Secure System Development  
## 06 May 2025  

---

## Introduction

### Objective
The primary goal of this project was to design, deploy, and operate a basic Security Operations Center (SOC) using open-source tools built around an ELK-based SIEM. A secondary goal was to deepen our understanding of log collection and analysis for enhancing organizational security.

### Key Tasks
- Deploy a Security Information and Event Management (SIEM) system to centralize and analyze log data.  
- Integrate threat-intelligence feeds to enrich events with Indicators of Compromise (IOCs).  
- Implement an alerting system to automatically detect and react to threats.  
- Validate the setup via simulated incidents and a vulnerable web app.  
- Document the architecture, configurations, and outcomes.

### Team Responsibilities
- **Daniil Vasilev:** SIEM deployment & configuration, log ingestion pipelines, threat-intel enrichment, incident simulation.  
- **Vika Patrina:** Alert‐generation logic, event–IOC correlation, vulnerable web app development.  
- **Nika Chekhonina:** Docker orchestration, alert integration, vulnerable web app development.

---

## Methods

### Infrastructure Overview
We built a scalable, fully Docker-ized pipeline for collecting, processing, storing, and visualizing log data. All services run in containers and are divided into two isolated Docker networks:

- **soc_network** – hosts the ELK/SOC stack and ElastAlert.  
- **app-network** – hosts the vulnerable application stack (PostgreSQL, backend, frontend).

1. **Log Collection**  
   - **Filebeat** agents on each host collected:
     - **syslog** (system events)  
     - **auth.log** (authentication attempts)  
     - **backend_logs** (vulnerable app output)  
     - **test_logs** (simulated events)

2. **Log Processing**  
   - **Logstash** parsed and normalized incoming logs.  
   - **Threat-intel Enrichment:** Integrated AlienVault IOCs (malicious IPs, domains, hashes).  
   - **GeoIP Enrichment:** Mapped source IPs to physical locations for anomaly detection.

3. **Storage & Analysis**  
   - **Elasticsearch** stored and indexed enriched logs for fast querying.  
   - **Kibana** provided dashboards and visualizations.  
   - **ElastAlert** generated alerts, forwarding them via Telegram/Zammad.

### Infrastructure Diagram
![ELK-SIEM Data Flow](dq.png)

---

## Results

### Proof-of-Concept Tests
- **XSS Exploitation**  
  Simulated a cross-site scripting attack against the vulnerable app. The pipeline detected the injected payload via regex filters in Logstash and triggered a Telegram alert for investigation.

- **SQL Injection**  
  Executed SQL-injection payloads on the login endpoint. Logs containing suspicious SQL patterns were flagged and alerted in near real-time.

- **Suspicious IP/Domain Simulation**  
  Generated test logs using known malicious IPs/domains from AlienVault’s IOC list. The system correctly matched these events, enriched them with IOC metadata, and raised high-priority alerts.

---

## Discussion

### Challenges Encountered
- **Multi-tool Integration:** Harmonizing Filebeat, Logstash, Elasticsearch, and ElastAlert required extensive configuration tuning to handle disparate log formats and enrichment workflows.  
- **Log Parsing & Enrichment:** Extracting the right fields in Logstash and aligning them with external IOC data posed challenges around field mappings and data consistency.  

### Skills Acquired
- **SIEM Deployment:** Hands-on experience in deploying and managing a full ELK stack for security monitoring.  
- **Threat-Intelligence Integration:** Learned to consume and correlate external IOC feeds to augment native log data.  
- **Troubleshooting & Debugging:** Developed systematic approaches to diagnose pipeline failures, misconfigurations, and false positives.

---

## Conclusion

The project successfully demonstrated how an open-source ELK-based SIEM can be deployed to centralize log data, enrich it with threat intelligence, and automate incident detection. Despite integration and parsing hurdles, the proof-of-concept showed reliable detection of XSS, SQLi, and IOC-based events with automated alerting. Moving forward, this SOC could be enhanced with additional endpoint detection tools and advanced correlation rules.

---

## Configuration Files

All project configuration files are available on GitHub:  
[https://github.com/creepydanunity/SSD-ELK-SOC](Link)

---

## Screenshots

#### Indexed Events Overview  
![Alerted Events](observe.png)

#### Indexed Groups by Tag  
![Alert Groups](alerts_groups.png)

#### GeoIP Enrichment Example  
![GeoIP Data](geo.png)

#### Parsed AlienVault IOCs  
![OTX Indicators](AlientVaultParsed.png)  
![OTX Types](AlienVaultParsed2.png)

#### Alerted Events Overview  
![Alerted Events](observe.png)
