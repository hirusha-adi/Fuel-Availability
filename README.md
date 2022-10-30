# Fuel-Availability (INCOMPLETE)

NOTE: I'll get back to completing this after OL's in January

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
    
# Images

![image](https://user-images.githubusercontent.com/36286877/182191521-b47fbd96-4c22-4752-b01e-4ad668a080d4.png)

![image](https://user-images.githubusercontent.com/36286877/182191535-ed62cbb3-387f-43ae-add9-c18e19758f99.png)

![image](https://user-images.githubusercontent.com/36286877/182191507-785eab6c-b422-446e-9f9b-d1619ed32bb9.png)

![image](https://user-images.githubusercontent.com/36286877/182191551-bd3f6193-244c-4203-9ce6-9cb83da2b10f.png)

![image](https://user-images.githubusercontent.com/36286877/182191562-ac7218ee-0f69-413e-928d-ff716e45ada0.png)

![image](https://user-images.githubusercontent.com/36286877/182191588-8886bb8c-01b3-473e-b31b-167b3e951f02.png)

![image](https://user-images.githubusercontent.com/36286877/182191626-5bf86c88-b3a2-4f30-b6db-29d7127d96d6.png)

![image](https://user-images.githubusercontent.com/36286877/182191478-06ac7e85-e648-451e-ada0-25b0b0483c69.png)

![image](https://user-images.githubusercontent.com/36286877/182192140-a9676bf4-90ea-47f7-ba32-05689643b003.png)

![image](https://user-images.githubusercontent.com/36286877/182192323-9f4c9231-6fe0-4247-a94c-18f5bfe6f9bc.png)

![image](https://user-images.githubusercontent.com/36286877/182191899-40c2a1e1-ced3-43b0-85f0-33f29042a245.png)
