import importlib

# plugin_name: plugin_display_name
allowed_plugins = { \
    "stub":     "Stub for test", \
    "gmail":    "Gmail", \
    }

def get_allowed_plugin_list():
    return allowed_plugins

def dispatch_plugin(function_name, plugin_name, plugin_args = []):
    """
        function_name: update, init, del, info_list
            update: fetch data from source and update opensearch
            init: store info when initialize the plugin
            del: clean stored info when delete the plugin
            info_list: return a list of required info to initialize the plugin, with hint text. "password", "private_key" are special info that will be hidden in the UI. Format: { "hint": "Enter your private key", "info_list": <info_list>}
        Each function should return a status code. Format: (status, other_return_values, ...)
    """

    if plugin_name not in allowed_plugins:
        # TODO: log error
        print("dispatch_plugin: Plugin not allowed: ", plugin_name)
        # TODO: return status
        return None
    plugin_module = importlib.import_module("plugins.plugin_" + plugin_name)
    plugin_function = getattr(plugin_module, "plugin_" + plugin_name+ "_" + function_name)
    return plugin_function(*plugin_args)
