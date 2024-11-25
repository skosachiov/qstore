import json, sys, random

categories = ["AudioVideo", "Audio", "Video", "Development",
    "Education", "Game", "Graphics", "Network", "Office", "Science",
    "Settings", "System", "Utility" ]

# ... <image dir list file> <desc file> <type>

desc = []

with open(sys.argv[2], "r") as f:
    for line in f.readlines():
        desc.append(line)

d = {}

with open(sys.argv[1], "r") as f:
    for line in f.readlines():
        line = line.split('.')[0]
        # print(line)
        for e in desc:
            if line.lower() in e.lower():
                d[line] = {
                    "name": line,
                    "category": random.choice(categories),
                    "approve": random.choice([False, True]),
                    "size": random.randint(1, 100) * 1000000,
                    "image": "images/" + line + ".png",
                    "type": sys.argv[3],
                    "description": e.replace("\t", " ").replace("\n", "")
                    }


s = json.dumps(d, indent=4) 
print(s)
