import xml.etree.ElementTree as ET


TMX_FILE = "data/maps/farm_old.tmx"
OUT_FILE = "data/maps/farm_new.tmx"

SOURCE_LAYER = "farmable_outgroup"
TARGET_LAYER = "farmable_ingroup"


# ----------------------------
# load xml
# ----------------------------
tree = ET.parse(TMX_FILE)
root = tree.getroot()


def get_layer(name):
    for layer in root.findall("layer"):
        if layer.get("name") == name:
            return layer
    raise ValueError(f"Layer not found: {name}")


def parse_csv_layer(layer):
    data = layer.find("data").text.strip()

    width = int(layer.get("width"))
    values = list(map(int, data.replace("\n", "").split(",")))

    return [
        values[i:i + width]
        for i in range(0, len(values), width)
    ]


def encode_csv(grid):
    return "\n".join(
        ",".join(str(v) for v in row) + ","
        for row in grid
    )


# ----------------------------
# get layers
# ----------------------------
out_layer = get_layer(SOURCE_LAYER)
in_layer = get_layer(TARGET_LAYER)

outgroup = parse_csv_layer(out_layer)
ingroup = parse_csv_layer(in_layer)

height = len(outgroup)
width = len(outgroup[0])


# ----------------------------
# merge (ingroup overrides outgroup)
# ----------------------------
result = [row[:] for row in outgroup]

for y in range(height):
    for x in range(width):
        if ingroup[y][x] != 0:
            result[y][x] = ingroup[y][x]


# ----------------------------
# write back into target layer
# ----------------------------
in_layer.find("data").text = encode_csv(result)


# ----------------------------
# save
# ----------------------------
tree.write(OUT_FILE, encoding="utf-8", xml_declaration=True)