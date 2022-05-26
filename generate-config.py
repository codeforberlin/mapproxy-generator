import argparse
import xml.etree.ElementTree as ET
import yaml

ns = {
    'wms': 'http://www.opengis.net/wms',
    'xlink': 'http://www.w3.org/1999/xlink'
}
srs = 'EPSG:3068'
version = '1.3.0'

parser = argparse.ArgumentParser()
parser.add_argument('capabilities_xml')

args = parser.parse_args()

config = {
    'globals': {},
    'grids': {
        'mercator': {
            'base': 'GLOBAL_MERCATOR'
        }
    },
    'services': {
        'demo': {},
        'tms': {
            'origin': 'nw',
            'use_grid_names': True
        }
    },
    'layers': [],
    'caches': {},
    'sources': {}
}

tree = ET.parse(args.capabilities_xml)
root_node = tree.getroot()
capability_node = root_node.find('wms:Capability', ns)

online_resource_node = capability_node.find('wms:Request', ns) \
                                      .find('wms:GetMap', ns) \
                                      .find('wms:DCPType', ns) \
                                      .find('wms:HTTP', ns) \
                                      .find('wms:Get', ns) \
                                      .find('wms:OnlineResource', ns)
url = online_resource_node.get('{{{xlink}}}href'.format(**ns))

layers_node = capability_node.find('wms:Layer', ns)
for layer_node in layers_node.findall('wms:Layer', ns):
    name = layer_node.find('wms:Name', ns).text
    title = layer_node.find('wms:Title', ns).text

    cache = f'{name}_cache'
    source = f'{name}_source'

    config['layers'].append({
        'name': name,
        'sources': [cache],
        'title': title
    })
    config['caches'][cache] = {
        'grids': ['mercator'],
        'sources': [source]
    }
    config['sources'][source] = {
        'req': {
            'format': 'png',
            'layers': name,
            'style': 'simple',
            'transparent': True,
            'url': url
        },
        'supported_srs': [srs],
        'type': 'wms',
        'wms_opts': {
            'version': version
        }
    }

print(yaml.dump(config))
