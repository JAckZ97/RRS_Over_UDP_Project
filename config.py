import yaml

configFile = "config.yaml"

def read_data(serverName, datatype):
    with open(configFile) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        return config["server"][serverName][datatype]

def write_data(serverName, datatype, data):
    with open(configFile) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        config["server"][serverName][datatype] = data

    if config:
        with open(configFile,'w') as yamlfile:
            yaml.safe_dump(config, yamlfile)