# see: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

import argparse
import xml.etree.ElementTree as ET
import yaml
import math


def deg2num(lat_deg, lon_deg, zoom):
    # from: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


ns = {
    'wms': 'http://www.opengis.net/wms',
    'xlink': 'http://www.w3.org/1999/xlink'
}
srs = 'CRS:84'
zrange = [10, 21]

parser = argparse.ArgumentParser()
parser.add_argument('capabilities_xml')

args = parser.parse_args()

tiles = {}

tree = ET.parse(args.capabilities_xml)
root_node = tree.getroot()
capability_node = root_node.find('wms:Capability', ns)

layers_node = capability_node.find('wms:Layer', ns)
for layer_node in layers_node.findall('wms:Layer', ns):
    name = layer_node.find('wms:Name', ns).text

    for bbox_node in layer_node.findall('wms:BoundingBox', ns):
        if bbox_node.get('CRS') == srs:
            west = float(bbox_node.get('minx'))
            south = float(bbox_node.get('miny'))
            east = float(bbox_node.get('maxx'))
            north = float(bbox_node.get('maxy'))

            tiles[name] = {}
            for z in range(*zrange):
                nw_tile = deg2num(north, west, z)
                se_tile = deg2num(south, east, z)

                tiles[name][z] = {
                    'xrange': [nw_tile[0], se_tile[0] + 1],
                    'yrange': [nw_tile[1], se_tile[1] + 1]
                }

print(yaml.dump(tiles))
