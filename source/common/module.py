from source.instance import get_json_from_path
from source.instance import Instance


class Module:
    def __init__(self, wd, state=None, default=None):
        try:
            self.properties = get_json_from_path(wd / "settings.json")
        except FileNotFoundError:
            self.properties = {}
        self.instance = Instance.state
        if state:
            # merges static settings and dynamically passed state. States override settings.
            self.properties.update(state)
        elif default:
            self.properties.update(default)
