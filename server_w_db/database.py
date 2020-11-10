import yaml

class DatabaseController:
    
    def __init__(self):
        self.dbFile = "database.yaml"

    # read the yaml file
    def readFile(self):

        with open(self.dbFile, "r") as yamlFile:
            database = yaml.load_all(yamlFile, Loader=yaml.FullLoader)
            for user in database:
                for k, v in user.items():
                    return " ".join(v).encode()


    # reload the entire yaml file with message (NOT plan to use for now)
    def writeFile(self, message):

        # userMessage = {'message': [message.decode('utf-8')]}
        userMessage = {'message': {'name': message}}
        with open(self.dbFile, "w") as yamlFile:
            yaml.dump(userMessage, yamlFile)


    # update the yaml file by adding the newest registered user
    def updateFile(self, new_yaml_data_dict, msgCount):

        with open(self.dbFile,'r') as yamlfile:
            databaseUpdate = yaml.safe_load(yamlfile) # Note the safe_load
            databaseUpdate['User'].update({"user " + str(msgCount): new_yaml_data_dict})
            # databaseUpdate['User'].update({"user " : {new_yaml_data_dict}})

        if databaseUpdate:
            with open(self.dbFile,'w') as yamlfile:
                yaml.safe_dump(databaseUpdate, yamlfile) # Also note the safe_dump


    # check the exist user by user name
    def checkExistUser(self, name):

        with open(self.dbFile,'r') as yamlfile:
            database = yaml.safe_load(yamlfile) 
            for k, v in database["User"].items():
                # name not exist in the database
                if name != database["User"][k]["Client_Name"]:
                    return False
                else:
                    # name exist
                    return True
                    

class Count:
    def __init__(self):
        self.dbFile = "database.yaml"

    # count the number of user + 1
    def yaml_count(self):
        with open(self.dbFile,'r') as yamlfile:
            database = yaml.safe_load(yamlfile)
            countNext = sum([len(database["User"])]) + 1 
        return countNext
