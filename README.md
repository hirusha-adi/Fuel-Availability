# Fuel-Availability

A simple responsive web app made as a solution for the current fuel crisis in Sri Lanka

# How to setup the Server on Ubuntu Server

## Install and Setup MongoDB

1. Install

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install mongodb -y
    sudo systemctl enable mongodb --now
    ```

2. Run this command and open the config file

    ```bash
    sudo nano /etc/mongodb.conf
    ```

3. Change bind_ip from 127.0.0.1 to 0.0.0.0

    ```bash
    bind_ip = 0.0.0.0
    ```

4. run this command to restart mongo

    ```bash
    sudo systemctl restart mongodb
    ```

MongoDB is now publicly accessible by the default Port and the Server IP. Now, create an account and enable authorization for security

5. Start MongoDB CLI

    ```bash
    mongo
    ```

6. Switch to the default pre-made admin database

    ```
    use admin
    ````

7. Create a new user

    ```
    db.createUser(
    {
    user: "AdminUserName",
    pwd: "SuperSecretPassword",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
    }
    )
    ```

The new user is created, Now, You have to make logging-in required

8. Open the config file

    ```bash
    sudo nano /etc/mongodb.conf
    ```

9. Edit the file content `Ctrl+W` to search

    ```
    authorization: enabled
    ```

10. Restart MongoDB Service

    ```bash
    sudo systemctl restart mongod
    ```

## Install and Setup the Web App

1. Install main dependencies

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip git nano -y
    ```

2. Create a seperate folder (Optional)

    ```bash
    mkdir FuelApp && cd ./FuelApp
    ```

3. Clone the repo and cd into it

    ```bash
    git clone "https://github.com/hirusha-adi/Fuel-Availability.git" && cd ./Fuel-Availability
    ```

4. Edit the main config file

    ```bash
    nano database/settings.json
    ```

5. start the web server

    ```bash
    python3 app.py
    ```
