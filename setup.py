import yaml

with open("config.yaml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

with open("config.yaml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    data["username"] = username
    data["password"] = password
    with open("config.yaml", 'w') as f:
        yaml.dump(data, f)
