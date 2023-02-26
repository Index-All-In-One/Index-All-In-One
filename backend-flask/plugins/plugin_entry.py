import importlib

def dispatch_plugin(plugin_name, plugin_args):
    plugin_module = importlib.import_module("plugins.plugin_" + plugin_name)
    plugin_function = getattr(plugin_module, "plugin_" + plugin_name)
    plugin_function(*plugin_args)
