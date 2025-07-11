#!/usr/bin/env python3

"""Generate the CI matrix."""

import configparser
import json
import os
import sys
import random

rootdir = "variants/"

options = sys.argv[1:]

outlist = []

if len(options) < 1:
    print(json.dumps(outlist))
    exit()

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == "platformio.ini":
            config = configparser.ConfigParser()
            config.read(subdir + "/" + file)
            for c in config.sections():
                if c.startswith("env:"):
                    section = config[c].name[4:]
                    if "extends" in config[config[c].name]:
                        if options[0] + "_base" in config[config[c].name]["extends"]:
                            if "board_level" in config[config[c].name]:
                                if (
                                    config[config[c].name]["board_level"] == "extra"
                                ) & ("extra" in options):
                                    outlist.append(section)
                            else:
                                outlist.append(section)
                        # Add the TFT variants if the base variant is selected
                        elif section.replace("-tft", "") in outlist and config[config[c].name].get("board_level") != "extra":
                            outlist.append(section)
                        elif section.replace("-inkhud", "") in outlist and config[config[c].name].get("board_level") != "extra":
                            outlist.append(section)
                    if "board_check" in config[config[c].name]:
                        if (config[config[c].name]["board_check"] == "true") & (
                            "check" in options
                        ):
                            outlist.append(section)
if ("quick" in options) & (len(outlist) > 3):
    print(json.dumps(random.sample(outlist, 3)))
else:
    print(json.dumps(outlist))