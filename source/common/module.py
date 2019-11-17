from source.instance import get_json_from_path


class Module:
    def __init__(self, wd, state=None, default=None):
        self.properties = get_json_from_path(wd / "settings.json")
        if state:
            # merges static settings and dynamically passed state. States override settings.
            self.properties.update(state)
        elif default:
            self.properties.update(default)
