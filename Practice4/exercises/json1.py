import json
import os

cur_dir = os.path.dirname(__file__)
file_path = os.path.join(cur_dir, 'sample-data.json')

with open(file_path, "r") as file:
    data = json.load(file)

print("Interface Status")
print("="*80)
print(f"{"DN":<50} {"Description":<20} {"Speed":<6} {"MTU":<6}")
print("-"*50, "-"*20, "-"*6, "-"*6)

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    print(f"{dn:<50} {descr:<20} {speed:<7} {mtu:<6}")

with open("Practice4\parsed_output.json", "w") as outfile:
    json.dump(data, outfile, indent=4)