import json
import os
import sys

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
    def __init__(self, logfile):
        self.logfile = logfile

    def log(self, message:str):
        self.logfile.write("[LOG] " + message + "\n")
        self.logfile.flush()
        print(Colors.OKGREEN + "[LOG] " + message + Colors.ENDC)

    def error(self, message:str):
        self.logfile.write("[ERROR] " + message + "\n")
        self.logfile.flush()
        print(Colors.FAIL + "[ERROR] " + message + Colors.ENDC)

    def warning(self, message:str):
        self.logfile.write("[WARNING] " + message + "\n")
        self.logfile.flush()
        print(Colors.WARNING + "[WARNING] " + message + Colors.ENDC)

    def info(self, message:str):
        self.logfile.write("[INFO] " + message + "\n")
        self.logfile.flush()
        print(Colors.OKBLUE + "[INFO] " + message + Colors.ENDC)

    def debug(self, message:str):
        self.logfile.write("[DEBUG] " + message + "\n")
        self.logfile.flush()
        print(Colors.OKBLUE + "[DEBUG] " + message + Colors.ENDC)

    def success(self, message:str):
        self.logfile.write("[SUCCESS] " + message + "\n")
        self.logfile.flush()
        print(Colors.OKGREEN + "[SUCCESS] " + message + Colors.ENDC)


Logger = Logger(open("log.txt", "a"))

# Check if config file exists
if not os.path.isfile("config.json"):
    Logger.error("Config file not found!")
    Logger.log("Creating config file...")
    data = {
        "firstrun": True,
        "username": "",
        "password": ""
    }
    with open("config.json", "w") as f:
        json.dump(data, f)
        Logger.info("Config file created")

class Config:
    def __init__(self, configfile):
        self.configfile = configfile
        self.config = {}
        self.load()

    def load(self):
        try:
            with open(self.configfile, "r") as f:
                self.config = json.load(f)
        except Exception as e:
            Logger.error("Could not load config file: " + str(e))
            exit(1)

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        self.config[key] = value
        self.save()
        Logger.info("Config value changed!")

    def save(self):
        with open(self.configfile, "w") as f:
            json.dump(self.config, f)
            Logger.info("Config file saved")

Config = Config("config.json")
    
if Config.get("firstrun") == True:
    username = input(Colors.OKBLUE + "Username: " + Colors.ENDC)
    password = input(Colors.OKBLUE + "Password: " + Colors.ENDC)
    Config.set("firstrun", False)
    Config.set("username", username)
    Config.set("password", password)
    Config.save()
    exit(0)
elif Config.get("firstrun") == False:
    username = Config.get("username")
    password = Config.get("password")
    Logger.info("Config loaded")
    os.system("cls")
    print(Colors.OKGREEN + "Welcome " + username + Colors.ENDC)
    print("")
    print(Colors.OKGREEN + "1" + Colors.ENDC + ") " + Colors.BOLD + "Change username")
    print(Colors.OKGREEN + "2" + Colors.ENDC + ") " + Colors.BOLD + "Change password")
    print(Colors.OKGREEN + "3" + Colors.ENDC + ") " + Colors.BOLD + "Exit")
    print("")
    choice = input(Colors.OKGREEN + "Choice: " + Colors.ENDC)
    if choice == "1":
        os.system("cls")
        username = input(Colors.OKGREEN + "Username: " + Colors.ENDC)
        password = input(Colors.OKGREEN + "Password: " + Colors.ENDC)
        Config.set("username", username)
        Config.set("password", password)
        Config.save()
        Logger.info("Account added")
        exit(0)
    elif choice == "2":
        os.system("cls")
        password = input(Colors.OKGREEN + "Password: " + Colors.ENDC)
        Config.set("password", password)
        Config.save()
        Logger.info("Password changed")
        exit(0)
    elif choice == "3":
        exit(0)
    else:
        Logger.error("Invalid choice")
        exit(1)

class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = None
        self.login()

    def login(self):
        Logger.info("Logging in...")
        try:
            Config.load()
            self.session = True
            Logger.success("Login successful")

        except Exception as e:
            Logger.error("Could not login: " + str(e))
            exit(1)

    def get_session(self):
        return self.session

    def get_username(self):
        return self.username

    def get_session(self):
        return self.session

Client = Client(Config.get("username"), Config.get("password"))