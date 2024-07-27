# Command and Control (C2) Server & Client Project

## Introduction
This project aims to understand C2 servers in depth and expand my defensive skills against such threats.

## Requirements
- Python 3.x
- AWS account for deployment (Free Tier)

## Setup
### AWS Environment
1. Create an EC2 instance on AWS. (Free tier eligible) (Ubuntu Server 22.04 LTS)
2. Configure security groups to allow traffic on the desired port (9999).
   - Custom inbound TCP rule to allow :9999 

### Development Environment
1. Clone the repository:
   ```sh
   git clone https://github.com/cwsecur1ty/C2-Server.git
   cd C2-Server-Project

## Example console output on the C2 Server from receiving connection from the client (victim). 
![test_string_result](https://github.com/user-attachments/assets/d5358548-1954-4e83-a4ae-a85963f2e303)
