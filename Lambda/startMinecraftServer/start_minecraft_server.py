import boto3
import time
import urllib
from discord import post_discord_message
from parameter_store import get_parameter


def lambda_handler(event, context):
    is_test = False
    test_string = "test_" if is_test else ""

    try:
        post_discord_message(f"マイクラサーバーの起動準備中...{get_parameter('emoji_yoshi')}")
        
        ec2_client = boto3.client('ec2')
        ec2_client.start_instances(InstanceIds=[get_parameter(f"minecraft_{test_string}ec2_id")])
        time.sleep(2)
        network_interfaces = ec2_client.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'addresses.private-ip-address',
                    'Values': [get_parameter(f"minecraft_{test_string}ec2_private_ip_address")]
                },
            ],
        )
        
        public_ip = network_interfaces['NetworkInterfaces'][0]['Association']['PublicIp']
        domain = get_parameter("ddns_now_username")
        password = get_parameter("ddns_now_token")
        req = urllib.request.Request(f"https://f5.si/update.php?domain={domain}&password={password}&ip={public_ip}")
        urllib.request.urlopen(req)

        post_discord_message(f"マイクラサーバー起動処理完了！{get_parameter('emoji_server_started')}\n`{domain}.f5.si` (接続まで3分くらいかかるかも)\n`{public_ip}` (急ぎの人はこっち)")
        return "Completed to start Minecraft Server!"

    except Exception as e:
        print(e.args)
        post_discord_message(f"{get_parameter('discord_mention')}\nマイクラサーバー起動失敗{get_parameter('emoji_doushite')}")
        return "Failed to start Minecraft Server."
