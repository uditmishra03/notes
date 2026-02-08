#!/bin/bash
#

FILE="user.csv"

if [ ! -f "$FILE" ]; then
        echo "$FILE does not exists, Please check back again!"
        exit 1
fi

tail -n+2 "$FILE" | while read line
do
        username=$(echo $line | cut -d ',' -f1)
        passwd=$(echo $line | cut -d ',' -f2)

#       echo $username, $passwd

        id $username &> /dev/null

        if [ $? -ne 0 ];then
            useradd $username
            echo "$username:$passwd" | chpasswd
            if [ $? -eq 0 ];then
                echo -e "$username has been created\n"
            fi
        else
            echo -e "$username already exists\n"
        fi
done
