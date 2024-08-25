#!/bin/bash
file=$1
output="$(pwd)/$file"
for repo in $(cat projects-accepted-revised.txt); do
	cd /home/repos/github/"$repo" || exit 1
	echo "$repo" >> "$output"
	for hour in $(seq 0 23); do
		commits=$(git log --grep="git-svn-id" --since="2013-01-01" --until="2013-12-31" --pretty=format:"%b %ad" | grep "$hour:..:.." | wc -l)
		if [ -z "$commits" ]; then
			commits=0
		fi
			if [ $commits -gt 1 ] ; then
				echo "$hour:00:00-$hour:59:59" >> "$output"
				echo "$commits" >> "$output"
		
			fi
	done
done	
	
