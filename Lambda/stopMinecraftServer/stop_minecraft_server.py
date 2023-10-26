import boto3
from discord import post_discord_message
from parameter_store import get_parameter

    
def lambda_handler(event, context):
    is_test = False
    test_string = "test_" if is_test else ""
    
    try:
        post_discord_message(f"マイクラサーバーの終了処理を開始します{get_parameter('emoji_yoshi')}")
    
        ec2_client = boto3.client('ec2')
        ec2_client.stop_instances(InstanceIds=[get_parameter(f"minecraft_{test_string}ec2_id")])
        
        post_discord_message(f"マイクラサーバーの終了処理が完了しました{get_parameter('emoji_server_stopped')}")
        return "Completed to stop Minecraft Server!"
        
    except Exception as e:
        print(e.args)
        post_discord_message(f"{get_parameter('discord_mention')}\nマイクラサーバーの終了に失敗しました{get_parameter('emoji_doushite')}")
        return "Failed to stop Minecraft Server."
