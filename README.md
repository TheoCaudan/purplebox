# Cybersecurity Lab - Purple Box (Management & Orchestration)

**⚠️ WORK IN PROGRESS ⚠️**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

This repository contains the orchestration and integration components for our cybersecurity lab environment. The Purple Box serves as the central management platform that coordinates activities between defensive (Blue) and offensive (Red) environments.

## Overview

The Purple Box fulfills the following primary functions:
- Centralized monitoring and logging of all lab activities
- Cross-environment orchestration and automation
- Integration testing and scenario management
- Comprehensive reporting and visualization dashboards

## Current Status

This repository is currently under active development. Core components are being implemented and tested. Some features may be incomplete or subject to significant changes.

## Key Components

- **Ansible Playbooks**: For automated deployment of all lab environments
- **Docker Containers**: ELK stack, Jenkins, and monitoring dashboards
- **Integration Scripts**: For cross-environment testing and validation
- **CI/CD Pipeline**: Automated testing and deployment workflows

## Network Information

The Purple Box operates on the management network (`192.168.10.0/24`) and coordinates communication between:
- Blue network (`192.168.11.0/24`) - Defensive operations
- Red network (`192.168.12.0/24`) - Offensive operations

## Getting Started

**Note**: Setup instructions will be expanded in future updates.

1. Clone this repository
2. Run the initial setup script: `./scripts/setup-purplebox.sh`
3. Follow the prompts to configure the environment

## Future Enhancements

- Complete dashboard integration
- Enhanced reporting features
- Automated scenario execution
- ML-based attack detection

## Contributors

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About This Project

This is a personal portfolio project I developed on my own to showcase my skills in cybersecurity infrastructure, automation, and DevSecOps. Feel free to use, modify, and learn from this project for your own educational purposes.

The project demonstrates my ability to design and implement complex security environments with proper network segmentation, infrastructure as code, and security monitoring capabilities.

---

**Last Updated**: May 5, 2025  
**Contact**: Please reach out through GitHub issues for questions
