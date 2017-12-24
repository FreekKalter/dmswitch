#!/bin/sh

tmux new-window 'source ./venv/bin/activate; make run'
cd ./dmswitch/frontend/
#tmux select-pane -t 1
tmux split-window -h 'npm run build'
tmux select-pane -t 0
#cd ../

