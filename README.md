# Command and Control (C2) Server & Client Project

## Introduction
This project aims to better my understanding of Command and Control (C2) servers and expand my defensive skills against such threats. The project includes a C2 server and client written in Python, demonstrating basic interactions between a server and multiple clients.

## Requirements
- Python 3.x
- Python packages:
   - cryptography
   - requests
- AWS account for deployment (Free Tier)
  
## Setup
### AWS Environment
1. Create an EC2 instance on AWS. (Free tier eligible) (Ubuntu Server 22.04 LTS)
2. Configure security groups to allow traffic on the desired port (9999).
   - Add a custom inbound TCP rule to allow traffic on port 9999.
   - Optionally-SortOfNotOptionally, allow traffic on port 80 for HTTP.

### Development Environment
1. Clone the repository:
   ```sh
   git clone https://github.com/cwsecur1ty/C2-Server.git
   cd C2-Server-Project
   ```
2. Install required Python packages:
   ```sh
   pip install cryptography requests
   ```
3. Configure the server:
   - Update Config/config.json with any needed changes (usually none).
     
## File Structure
   ```sh
      C2-Server/
      │
      ├── c2_server.py
      ├── Stagers/
      │   ├── python_stager.py
      │   └── c2_client.py
      └── Config/
          └── config.json
   ```

## Examples & Test (Photos)

#### Example console command with output, and downloading of a specified file.#
![test_string_result3](https://github.com/user-attachments/assets/db6ca58b-77d7-4913-bdcc-ef936f4bfd07)

#### Example of the client running the python_stager (right-hand side) and then executing c2_client.py, and finally the server receiving the connection (left-hand side).
![test_string_result4](https://github.com/user-attachments/assets/b4e2c6bd-862a-47f6-9154-9580db8de8a6)


