import yaml

class DatabaseController:
    
    def __init__(self):
        pass


    def readFile(self):

        with open("database.yaml", "r") as yamlFile:
            database = yaml.load_all(yamlFile, Loader=yaml.FullLoader)
            for user in database:
                for k, v in user.items():
                    return " ".join(v).encode()


    def writeFile(self, message):

        # userMessage = {'message': [message.decode('utf-8')]}
        userMessage = {'message': {'name': message}}
        with open("database.yaml", "w") as yamlFile:
            yaml.dump(userMessage, yamlFile)


    def updateFile(self, new_yaml_data_dict):

        with open('database.yaml','r') as yamlfile:
            databaseUpdate = yaml.safe_load(yamlfile) # Note the safe_load
            databaseUpdate['User'].update(new_yaml_data_dict)

        if databaseUpdate:
            with open('database.yaml','w') as yamlfile:
                yaml.safe_dump(databaseUpdate, yamlfile) # Also note the safe_dump


    def checkExistUser(self, name):

        with open('database.yaml','r') as yamlfile:
            database = yaml.safe_load(yamlfile) 
            for k, v in database["User"].items():

                # name not exist in the database
                if name != database["User"][k]["Client_Name"]:
                    return False
        # name exist
        return True