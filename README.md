
# 🔍 IT Audit Control Simulator  
*A Python-based simulation tool for evaluating IT General Controls (ITGCs)*

## 📌 Overview
The **IT Audit Control Simulator** is a hands-on project designed to simulate the testing of key **IT General Controls (ITGCs)** used in IT audit, SOX compliance, cybersecurity reviews, and internal controls assessments.

The system loads configurable datasets from `config.json` and runs a full suite of automated controls tests covering:

- **Access Control**
- **Privileged Access Monitoring**
- **Segregation of Duties (SoD)**
- **Change Management**
- **Backup & Recovery**

Results are displayed in the terminal and can optionally be exported to CSV for reporting.

This project demonstrates:
- Python programming skills  
- IT audit & cybersecurity knowledge  
- Data validation & control testing logic  
- Config-driven architecture  
- Modular code design  
- Realistic enterprise control scenarios  

---

## 🚀 Features

### ✅ Access Control Tests
- Orphan account detection  
- Admin overuse monitoring  
- Terminated-but-active account detection  

### 🔐 Privileged Access & SoD
- Privileged role validation  
- Segregation of Duties conflict identification  

### 🔧 Change Management Tests
- Unapproved change detection  
- Approval-before-deployment validation  

### 💾 Backup & Recovery Tests
- Backup recency enforcement  
- Backup success rate validation  

### 📁 Optional CSV Export
You can choose whether to export *only failing controls* to a CSV file.

---

## 🗂 Project Structure

<p align="left">
  <img src="https://github.com/ksowu1/it-audit-control-simulator/actions/workflows/ci.yml/badge.svg" alt="CI Status">
  <img src="https://img.shields.io/github/license/ksowu1/it-audit-control-simulator" alt="License">
  <img src="https://img.shields.io/github/last-commit/ksowu1/it-audit-control-simulator" alt="Last Commit">
  <img src="https://img.shields.io/github/repo-size/ksowu1/it-audit-control-simulator" alt="Repo Size">
  <img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python Version">
</p>
