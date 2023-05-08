from plugins.status_code import PluginReturnStatus

def plugin_gdrive_update(plugin_instance_id,opensearch_hostname='localhost'):
    # only do update job for this plugin, don't need to loop or sleep
    # should accept opensearch_hostname as argument
    # Ensure that if plugin_xxx_del has been executed, unfinished update won't be write to opensearch anymore

    print("Plugin gdrive update: ", plugin_instance_id, opensearch_hostname)
    return PluginReturnStatus.SUCCESS

def plugin_gdrive_init(plugin_instance_id, plugin_init_info):
    # do init jobs, such as store credentials in database
    # plugin_init_info is a dict, defined in plugin_gdrive_info_def
    print("Plugin gdrive init: ", plugin_instance_id, plugin_init_info)

    return PluginReturnStatus.SUCCESS

def plugin_gdrive_del(plugin_instance_id):
    # do delete jobs, such as delete credentials in database
    print("Plugin gdrive del: ", plugin_instance_id)
    return PluginReturnStatus.SUCCESS

def plugin_gdrive_info_def():
    return PluginReturnStatus.SUCCESS, {"hint": "This is the hint of gdrive plugin", \
            "field_def":[ \
                { \
                    "field_name": "username", \
                    "display_name": "Username", \
                    "type": "text",
                }, \
                {
                    "field_name": "password", \
                    "display_name": "Password", \
                    "type": "secret",
                }, \
            ],}
