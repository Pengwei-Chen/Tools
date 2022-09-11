payload = open("Payload.txt", "r", encoding = "utf-8")
keys = {}
values = {}
for line in payload:
    line = line.rstrip("\n")
    if line != "":
        key = line.split(":")[0]
        if key in keys:
            keys[key] = keys[key] + 1
        else:
            keys[key] = 1
        if key in values:
            if values[key] != line.split(":")[1]:
                print(key, values[key][:10], line.split(":")[1][:10])
        else:
            values[key] = line.split(":")[1]
print()
for item in keys.items():
    if item[1] != 2:
        print(item[0])
payload.close()