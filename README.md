# Fuel Availability / Fuel App / Fuel Check

Fuel App is an innovative solution inspired by the fuel crisis that occurred in Sri Lanka from late 2021 to mid 2022. Fuel App was developed to provide an effective solution that simplifies the management of fuel usage and availability of fuel in filling stations.

Fuel App is a web-based platform that enables fuel stations to manage their fuel availability in a simple and user-friendly way. Designed with the needs of fuel stations in mind, this app provides a seamless experience for station owners, allowing them to manage their fuel stock with ease and efficiency once the station has been approved by the Administrator.


- Account registration: Fuel stations can register an account on the app, providing them with access to a range of features and functionalities.

- Interactive user interface: With an intuitive and user-friendly interface, Fuel App makes it easy for station owners to manage their fuel availability and make updates as required.

- Station approval: All stations must be approved by an administrator before they can use the app, ensuring that the platform is used only by authorized fuel stations.

- When users view the map on Fuel App, they have the option to give permissions to the app to access their geolocation. If permissions are granted, the app will automatically highlight fuel stations around the user's location, making it easy for them to find the nearest station.

-  To ensure the security of our users' data, we've implemented strict measures to protect their geolocation information. Specifically, we never send this data to the backend for any monitoring purposes. Instead, the data is processed locally on the user's device, ensuring that their geolocation information remains private and secure.

- Admin Panel Features:

   - The Fuel App admin panel is an interactive and user-friendly web interface that provides administrators with a range of features and functionalities. These features include:
   - User management: The admin panel allows administrators to manage user accounts, including adding, editing, and deleting accounts as required.
   - Station management: Administrators can also manage approved and pending fuel stations, ensuring that only authorized stations are allowed to use the app.
   - Analytics: The admin panel provides a range of analytics tools, allowing administrators to monitor usage, track trends, and make informed decisions about fuel stock management.
   - Logs: Administrators can access and review logs related to user activity and system events, providing valuable insight into app usage and performance.
   - Security: The admin panel is designed with security in mind, providing administrators with the tools they need to manage access and protect user data.
# How to setup on Ubuntu Server

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
   ```

7. Create a new user (in this example, the username is `AdminUserName` and the password is `SuperSecretPassword`)

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

4. Install requirements

   ```bash
   python3 -m pip instal -r requirements.txt
   ```

5. Edit the main config file
   
   - rename the `.env.example.` to `.env` and edit the .env file. (This file will be renamed as `.env.old` once everything has been loaded to the `settings.json` file)
   ```bash
   mv .env.example .env
   nano .env
   ```
   
   - or, edit the `database/settings.json` directly
   
   ```bash
   nano database/settings.json
   ```

   - `adminkey`: Password to access admin panel
   - `flaskSecret`: Flask Secret Key. Learn more [here](https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY)
   - `JawgToken`: Token for the Map's Dark Theme. You can get it from [here](https://www.jawg.io/lab/access-tokens)
   - `mongodb` _and Others_: Your Mongo DB Server IP, Username and Password
   - The admin user settings are to be filled once you create your account visiting the `/login` route. Once its updated, the web server should be restarted

<br>

6. Start the web server

   ```bash
   python3 app.py
   ```

# Images (Outdated)

![image](https://user-images.githubusercontent.com/36286877/221196517-8425670e-6f88-4e61-bc49-36981048105a.png)

![image](https://user-images.githubusercontent.com/36286877/221198338-87532d43-56c8-4c60-b8a4-1a224b778767.png)

![image](https://user-images.githubusercontent.com/36286877/221196578-13e93fd0-e0c6-4e3f-b82f-30c957dcb51f.png)

![image](https://user-images.githubusercontent.com/36286877/221196648-f0d8fb9a-71aa-43fa-a6c3-dd2893796338.png)

![image](https://user-images.githubusercontent.com/36286877/221196716-25d292e2-db86-4da3-8a75-956bc72bf91a.png)

![image](https://user-images.githubusercontent.com/36286877/221196788-0b60525f-0e1e-45e5-af5b-846437e772c4.png)

![image](https://user-images.githubusercontent.com/36286877/221197490-5ee7f8d5-5c2e-48dd-930c-ca68c27545cf.png)

![image](https://user-images.githubusercontent.com/36286877/221197938-dd269128-3b9f-45e2-97a4-45741cc2ff93.png)

![image](https://user-images.githubusercontent.com/36286877/221196848-95727425-650a-4f15-a9f8-4c4154fa2b50.png)

![image](https://user-images.githubusercontent.com/36286877/221196971-d8772293-5efc-40c4-af93-86f43311856d.png)

![image](https://user-images.githubusercontent.com/36286877/221197086-133dff36-5879-40a3-bbc9-6110b35de4e3.png)

![image](https://user-images.githubusercontent.com/36286877/221197205-5ee693d7-3535-422c-89eb-b2f14ed6ab97.png)

![image](https://user-images.githubusercontent.com/36286877/221197244-3eb5bca4-065a-4639-81e0-bac5322190e4.png)

![image](https://user-images.githubusercontent.com/36286877/221197289-850599b2-2ab4-43c9-a14a-7ecc6b508129.png)

![image](https://user-images.githubusercontent.com/36286877/221198238-d7e65033-eafe-4339-9540-f3c3395fe857.png)
