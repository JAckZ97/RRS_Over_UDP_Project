import yaml

class DatabaseController:
    
    def __init__(self):
        pass

    def readFile(self):

        with open("user_message.yaml") as f:
            docs = yaml.load_all(f, Loader=yaml.FullLoader)
            for doc in docs:
                for k, v in doc.items():
                    print(" ".join(v).encode())

    def writeFile(self, message):

        userMessage = {'message': [message.decode('utf-8')]}
        with open("user_message.yaml", "w") as f:
            data = yaml.dump(userMessage, f)