from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_netmiko.tasks import netmiko_save_config
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

def nornir_filtering(task):
    config_cmd = ["info-center enable",
                  "info-center loghost 192.168.56.1"
                  ]
    task.run(task=netmiko_send_config, config_commands=config_cmd)
    task.run(task=netmiko_save_config, confirm="y",confirm_response="y")
    task.run(task=netmiko_send_command, command_string="display arp")

nr = InitNornir(config_file="hosts.yaml")
nr_filter = nr.filter(type="switch")
results=nr_filter.run(task=nornir_filtering)
print_result(results)