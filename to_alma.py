import json
import os
import pandas as pd

os.makedirs("alma", exist_ok=True)


def mentioned_orgs(value):
    item = ", ".join([x["value"] for x in value["mentioned_orgs"]])
    return item


def mentioned_places(value):
    item = ", ".join([x["value"] for x in value["mentioned_places"]])
    return item


def mentioned(value, lookup):
    item = ", ".join([x["value"] for x in value[lookup]])
    return item


def get_content(ms_item_list):
    items = []
    for x in ms_item_list:
        text = x["locus_text"]
        title = x["title"]
        orgs = mentioned(x, "orgs")
        places = (x, "places")
        if x["year"] is not None:
            year = f'a {x["year"]}'
        else:
            year = False
        parts = [
            text,
            year,
            title,
            orgs,
            places,
        ]
        content = " ".join([part for part in parts if isinstance(part, str)])
        items.append(content)
    return " #### ".join(items)


with open(os.path.join("json_dumps", "msdesc.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

with open(os.path.join("json_dumps", "ms_item.json"), "r", encoding="utf-8") as f:
    ms_item_data = json.load(f)

ms_item_data = [value for key, value in ms_item_data.items() if value["msdesc"]]


result = []
for key, value in data.items():
    ms_item_list = list(
        filter(lambda x: x["msdesc"][0]["value"] == value["signatur"], ms_item_data)
    )
    result.append([value["signatur"], "ALMA", "data"])
    result.append(["Title", "245", value["title"]])
    result.append(["Date", "264", value["date"]])
    result.append(
        [
            "Extent, Measures, Foliation",
            "300",
            f"§§a {value['extent']}; $$c {value['height']} × {value['width']}mm; {value['foliation']}.",
        ]
    )
    result.append(["Fragments", "500", f"§§a {value['acc_mat']}"])
    result.append(
        [
            "Organisations/Places",
            "505/8/0",
            f"$$t {mentioned_orgs(value)}; {mentioned_places(value)}",
        ]
    )
    result.append(["Binding", "563", value["binding"]])
    result.append(["Content", "505", get_content(ms_item_list)])
    result.append(["", "", ""])

df = pd.DataFrame(result)
df.to_csv(os.path.join("alma/alma.csv"), index=False)
