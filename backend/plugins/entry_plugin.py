import importlib
import os
from plugins.status_code import PluginReturnStatus

DEBUG = os.getenv('DEBUG', '').lower() in ['1', 'true', 'yes']

# plugin_name: plugin_display_name
allowed_plugins_display = { \
    "gmail":    "Gmail", \
    }

def get_allowed_plugin_display_list():
    if DEBUG:
        allowed_plugins_display["stub"]="Stub for test"
        return allowed_plugins_display
    else:
        return allowed_plugins_display

def get_allowed_plugin_list():
    return list(get_allowed_plugin_display_list().keys())

def dispatch_plugin(function_name, plugin_name, plugin_args = []):
    """
        function_name: update, init, del, info_def
            update: fetch data from source and update opensearch
            init: store info when initialize the plugin
            del: clean stored info when delete the plugin
            info_def: return a list of required info to initialize the plugin, with hint text. "password", "private_key" are special info that will be hidden in the UI. Supported field types: text, secret, int, two_step.
                Format:
                { "hint": "Enter your private key",
                "field_def": [
                    {
                        "field_name": "username",
                        "display_name": "Username",
                        "type": "text",
                    },
                    {
                        "field_name": "password",
                        "display_name": "Password",
                        "type": "secret",
                    },
                ]}.

        Each function should return a status code. Format: (status, other_return_values, ...)
    """

    if plugin_name not in get_allowed_plugin_list():
        # TODO: log error
        print("dispatch_plugin: Plugin not allowed: ", plugin_name)
        return PluginReturnStatus.NO_PLUGIN

    plugin_module = importlib.import_module("plugins.plugin_" + plugin_name)
    plugin_function = getattr(plugin_module, "plugin_" + plugin_name+ "_" + function_name)
    return plugin_function(*plugin_args)
