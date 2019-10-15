import configparser


def load_cfg(conf_path="../env.conf"):
    config = configparser.ConfigParser()
    config.read(conf_path)
    # [0]=raw_path, [1]=json_path
    uncle_paths = [config.get("uncle", "raw_path"), config.get("uncle", "json_path")]
    canonical_paths = [config.get("canonical", "raw_path"), config.get("canonical", "json_path")]
    bc_path = [config.get("broadcast", "raw_path"), config.get("broadcast", "json_path")]
    forked_path = [config.get("forked", "raw_path"), config.get("forked", "json_path")]
    return [canonical_paths, bc_path, uncle_paths, forked_path]
