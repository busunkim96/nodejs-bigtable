import json

path = sys.argv[1]
os.chdir(path)

with open('package.json') as f:
    package = json.load(f)
    print(package['version'])
