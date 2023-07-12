# -*- coding: utf-8 -*-
import os

import yaml
from dotenv import load_dotenv

## this file auto load the Spacefile with environment variables without actually expose
load_dotenv()
with open("Spacefile") as f:
    content = f.read()
    # Replace placeholders with environment variables using .format()
    content = content.format(**os.environ)
    config = yaml.safe_load(content)
    yaml.safe_dump_all(
        config, open("Spacefile", "w"), default_flow_style=False
    )  # noqa: SIM115
