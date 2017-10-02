#!/bin/bash

setup() {
    REDDITWATCHER_DEF="
redditwatcher() {
    docker pull trstringer/redditwatcher:latest >> /dev/null
    docker run --rm \\
        -e REDDITWATCHER_CLIENTID=\$REDDITWATCHER_CLIENTID \\
        -e REDDITWATCHER_CLIENTSECRET=\$REDDITWATCHER_CLIENTSECRET \\
        -v /etc/localtime:/etc/localtime:ro \\
        trstringer/redditwatcher:latest \"\$@\"
}"

    if [[ -z $REDDITWATCHER_CLIENTID ]]; then
        printf 'please enter your reddit client id: '
        read REDDITWATCHER_CLIENTID
    fi

    if [[ -z $REDDITWATCHER_CLIENTSECRET ]]; then
        printf 'please enter your reddit secret: '
        read REDDITWATCHER_CLIENTSECRET
    fi

    grep "source ~/.redditwatcher" ~/.bashrc >> /dev/null
    if [ $? -ne 0 ]; then
        printf "adding .redditwatcher sourcing to bashrc..."
        printf "\nsource ~/.redditwatcher" >> ~/.bashrc
    else
        printf ".redditwatcher sourcing already in bashrc..."
    fi

    printf "export REDDITWATCHER_CLIENTID=$REDDITWATCHER_CLIENTID" > ~/.redditwatcher
    printf "\nexport REDDITWATCHER_CLIENTSECRET=$REDDITWATCHER_CLIENTSECRET" >> ~/.redditwatcher
    printf "\n$REDDITWATCHER_DEF" >> ~/.redditwatcher
    . ~/.bashrc
}

setup
