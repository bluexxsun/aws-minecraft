#!/bin/bash

if [ -e /home/ec2-user/minecraft/shutdown_count.txt ]; then
	tmux send-keys -t minecraft list ENTER
	sleep 3s
	message=$(tmux capture-pane -t minecraft -p | sed '/^$/d' | tail -1)

	if [[ $message =~ "There are 0 of" ]]; then
		count=$(cat /home/ec2-user/minecraft/shutdown_count.txt)
		next_count=$((count - 1))

		if [ $next_count -eq 0 ]; then
			tmux send-keys -t minecraft stop ENTER
			rm -f /home/ec2-user/minecraft/shutdown_count.txt
			sleep 30s
			curl "API URL for instance stop of Lambda" # ここにインスタンスを停止する Lambda を実行する API の URL を入力
		else
			if [ $next_count -eq 1 ]; then
                        	curl -H "Content-Type: application/json" -X POST -d '{"content": "5分後にサーバーの停止処理を開始します(絵文字)"}' \
                                	"discord webhook URL" # ここに Discord webhook の URL を入力
			fi

			echo $next_count > /home/ec2-user/minecraft/shutdown_count.txt
		fi
	else
		echo 3 > /home/ec2-user/minecraft/shutdown_count.txt
	fi
else
	echo 3 > /home/ec2-user/minecraft/shutdown_count.txt
fi