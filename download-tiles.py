import argparse
import time
import yaml
import requests
from pathlib import Path

url_template = 'http://127.0.0.1:8080/tiles/1.0.0/{layer}/mercator/{z}/{x}/{y}.png'

parser = argparse.ArgumentParser()
parser.add_argument('tiles_yaml')
parser.add_argument('layer')

args = parser.parse_args()

path = Path('tiles') / args.layer

with open(args.tiles_yaml) as fp:
    tilelist = yaml.safe_load(fp.read())

for z, tiles in tilelist[args.layer].items():
    for x in range(*tiles['xrange']):
        for y in range(*tiles['yrange']):
            url = url_template.format(layer=args.layer, z=z, x=x, y=y)

            print(url)

            response = requests.get(url)

            file_path = (path / str(z) / str(x) / str(y)).with_suffix('.png')
            file_path.parent.mkdir(exist_ok=True, parents=True)
            open(file_path, 'wb').write(response.content)

            time.sleep(0.2)
