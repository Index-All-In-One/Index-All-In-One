from plugins.status_code import PluginReturnStatus

def plugin_stub_update(plugin_instance_id,opensearch_hostname='localhost'):
    # only do update job for this plugin, don't need to loop or sleep
    # should accept opensearch_hostname as argument
    # Ensure that if plugin_gmail_del has been executed, unfinished update won't be write to opensearch anymore

    print("Plugin stub update: ", plugin_instance_id, opensearch_hostname)
    return PluginReturnStatus.SUCCESS

def plugin_stub_init(plugin_instance_id, plugin_init_info):
    # do init jobs, such as store credentials in database
    # plugin_init_info is a dict, defined in plugin_stub_info_def
    print("Plugin stub init: ", plugin_instance_id, plugin_init_info)

    if "two_step_code" not in plugin_init_info:
        # send code here
        return PluginReturnStatus.NEED_TWO_STEP_CODE

    return PluginReturnStatus.SUCCESS

def plugin_stub_del(plugin_instance_id):
    # do delete jobs, such as delete credentials in database
    print("Plugin stub del: ", plugin_instance_id)
    return PluginReturnStatus.SUCCESS

def plugin_stub_info_def():
    return PluginReturnStatus.SUCCESS, {"hint": "This is the hint of stub plugin", \
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
                {
                    "field_name": "two_step_code", \
                    "display_name": "2FA Code", \
                    "type": "two_step",
                }, \
            ],}
