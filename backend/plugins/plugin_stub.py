def plugin_stub_update(plugin_instance_id,opensearch_hostname='localhost'):
    print("Plugin stub update: ", plugin_instance_id, opensearch_hostname)

def plugin_stub_init(plugin_instance_id, plugin_init_info):
    print("Plugin stub init: ", plugin_instance_id, plugin_init_info)

def plugin_stub_del(plugin_instance_id):
    print("Plugin stub del: ", plugin_instance_id)

def plugin_stub_info_list():
    return {"hint": "", \
            "info_list": ["username", "password", "private_key"]}
