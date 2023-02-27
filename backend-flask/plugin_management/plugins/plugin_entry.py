import importlib

def dispatch_plugin_update(plugin_name, plugin_args):
    plugin_module = importlib.import_module("plugins.plugin_" + plugin_name)
    plugin_function = getattr(plugin_module, "plugin_" + plugin_name+ "_update")
    return plugin_function(*plugin_args)

def dispatch_plugin_init(plugin_name, plugin_args):
    plugin_module = importlib.import_module("plugins.plugin_" + plugin_name)
    plugin_function = getattr(plugin_module, "plugin_" + plugin_name+ "_init")
    return plugin_function(*plugin_args)

def dispatch_plugin_del(plugin_name, plugin_args):
    plugin_module = importlib.import_module("plugins.plugin_" + plugin_name)
    plugin_function = getattr(plugin_module, "plugin_" + plugin_name+ "_del")
    return plugin_function(*plugin_args)
