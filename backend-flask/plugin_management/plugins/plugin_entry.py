import importlib

def dispatch_plugin(path_prefix, function_name, plugin_name, plugin_args):
    #function_name: update, init, del
    plugin_module = importlib.import_module(path_prefix + "plugins.plugin_" + plugin_name)
    plugin_function = getattr(plugin_module, "plugin_" + plugin_name+ "_" + function_name)
    return plugin_function(*plugin_args)
