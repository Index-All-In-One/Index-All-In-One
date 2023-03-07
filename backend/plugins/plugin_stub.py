from plugins.status_code import PluginReturnStatus

def plugin_stub_update(plugin_instance_id,opensearch_hostname='localhost'):
    # only do update job for this plugin, don't need to loop or sleep
    # should accept opensearch_hostname as argument
    # Ensure that if plugin_gmail_del has been executed, unfinished update won't be write to opensearch anymore

    print("Plugin stub update: ", plugin_instance_id, opensearch_hostname)
    return PluginReturnStatus.SUCCESS

def plugin_stub_init(plugin_instance_id, plugin_init_info):
    # do init jobs, such as store credentials in database
    # plugin_init_info is a dict, defined in plugin_stub_info_list
    print("Plugin stub init: ", plugin_instance_id, plugin_init_info)
    return PluginReturnStatus.SUCCESS

def plugin_stub_del(plugin_instance_id):
    # do delete jobs, such as delete credentials in database
    print("Plugin stub del: ", plugin_instance_id)
    return PluginReturnStatus.SUCCESS

def plugin_stub_info_list():
    return PluginReturnStatus.SUCCESS, {"hint": "This is the hint of stub plugin", \
            "field_type": {"username": "text", "password": "secret",},}
