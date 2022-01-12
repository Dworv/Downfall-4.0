import toml

def load_secret(filename, botname):
    parsed_toml = toml.load(filename)
    return (parsed_toml[botname]['secret'])
    