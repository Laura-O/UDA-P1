#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

"""
In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

expected_cuisines = ["asian", "thai", "regional", "ice_cream", "chinese",
                    "turkish", "german", "pizza", "mexican", "italian",
                    "indian", "steak_house", "argentinian", "greek", "russian",
                    "kebab", "french", "burger", "oriental", "sausages",
                    "cake", "shisha", "spanish", "donuts", "vietnamese",
                    "lahmacun", "tapas", "sandwich", "pasta", "salad", "sushi",
                    "japanese", "balkan", "international"]

cuisine_mapping = {
                    "Wok und mehr": "asian",
                    "Wurst": "sausages",
                    "Balkan und internationale Speisen": "balkan; international",
                    "icecream": "ice_cream",
                    "german and french": "german; french",
                    "Kuchen,_Flammkuchen,_Espresso,_Capppuccino,Getränke":
                    "cake; tarte flambée; coffee; drinks"
                    }

def update_cuisine(cuisine):
    if cuisine not in expected_cuisines:
        if cuisine in cuisine_mapping:
            cuisine = cuisine_mapping[cuisine]
        elif "," in cuisine:
            cuisine = cuisine.replace(",", ";")
        if ";" in cuisine:
            cuisine_list = cuisine.split(';')
            for i in xrange(len(cuisine_list)):
                if cuisine_list[i] in cuisine_mapping:
                    cuisine_list[i] = cuisine_mapping[cuisine_list[i]]
            cuisine = ";".join(cuisine_list)
    return cuisine



def update_phone(phone_number):
    # found at http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
    rep = {"-": "", "(": "", ")": "", "/": "", " ": "", "-": "", "+": "", ".": ""}
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    phone_number = pattern.sub(lambda m: rep[re.escape(m.group(0))],phone_number)

    if phone_number[:2] == "49":
        phone_number = "0" + phone_number[2:]

    if phone_number[:4] == "0049":
        phone_number = phone_number[4:]

    if phone_number[:2] == "00":
        phone_number = phone_number[1:]

    if phone_number[0] != "0" and phone_number != "112":
        phone_number = "0" + phone_number

    return phone_number


problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        node['id'] = element.attrib['id']
        node['type'] = element.tag

        for k, v in element.items():
            if k in CREATED:
                node.setdefault("created", {})
                node["created"][k] = v
            elif k == "lat":
                node.setdefault("pos", [None, None])
                node["pos"][0] = float(v)
            elif k == "lon":
                node.setdefault("pos", [None, None])
                node["pos"][1] = float(v)
            else:
                node[k] = v

        # 2nd level tags
        for tag in element.iter('tag'):
            k, v = tag.get('k'), tag.get('v')

            if k == "phone":
                v = update_phone(v)
                node[k] = v

            if k == "cuisine":
                v = update_cuisine(v)
                node[k] = v

            if problemchars.search(k) is not None:
                continue
            elif ":" in k:
                segments = k.split(':')
                if segments[0] == "addr":
                    if len(segments) != 2:
                        continue
                    node.setdefault("address", {})
                    node["address"][segments[1]] = v
                else:
                    new_key = k.replace(':', "_")
                    node[new_key] = v
            else:
                node[k] = v

        # children way
        if element.tag == 'way':
            for node_ref in element.iter('nd'):
                node.setdefault("node_refs", [])
                ref = node_ref.get("ref")
                if ref is not None:
                    node["node_refs"].append(ref)

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    data = process_map('paderborn.osm', False)
