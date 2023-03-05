from plugins.status_code import PluginReturnStatus

def plugin_stub_update(plugin_instance_id,opensearch_hostname='localhost'):
    print("Plugin stub update: ", plugin_instance_id, opensearch_hostname)
    return PluginReturnStatus.SUCCESS

def plugin_stub_init(plugin_instance_id, plugin_init_info):
    print("Plugin stub init: ", plugin_instance_id, plugin_init_info)
    return PluginReturnStatus.SUCCESS

def plugin_stub_del(plugin_instance_id):
    print("Plugin stub del: ", plugin_instance_id)
    return PluginReturnStatus.SUCCESS

def plugin_stub_info_list():
    return PluginReturnStatus.SUCCESS, {"hint": "This is the hint of stub plugin", \
            "field_type": {"username": "text", "password": "secret",},}
