import munch
import yaml

def load_config(config_path: str) -> munch.Munch:
    with open(config_path, "r") as f:
        cfg_dict = yaml.safe_load(f)
        cfg = munch.munchify(cfg_dict)
    return cfg