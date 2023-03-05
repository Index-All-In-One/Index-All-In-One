def plugin_stub_update(plugin_instance_id,opensearch_hostname='localhost'):
    print("Plugin stub update: ", plugin_instance_id, opensearch_hostname)
    return None

def plugin_stub_init(plugin_instance_id, plugin_init_info):
    print("Plugin stub init: ", plugin_instance_id, plugin_init_info)
    return None

def plugin_stub_del(plugin_instance_id):
    print("Plugin stub del: ", plugin_instance_id)
    return None

def plugin_stub_info_list():
    return None, {"hint": "This is the hint of stub plugin", \
            "field_type": {"username": "text", "password": "secret",},}
