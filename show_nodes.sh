#!/bin/bash

SESSION="dimutex-nodes"

# Encerra a sessão antiga, se existir
tmux kill-session -t $SESSION 2>/dev/null

# Cria nova sessão em modo detached
tmux new-session -d -s $SESSION

# Painel 0: logs do node1
tmux send-keys -t $SESSION:0.0 "docker logs -f dimutex_node1_1" C-m

# Divide verticalmente para painel 1: node2
tmux split-window -v -t $SESSION:0
tmux send-keys -t $SESSION:0.1 "docker logs -f dimutex_node2_1" C-m

# Divide verticalmente para painel 1: node2
tmux split-window -v -t $SESSION:0
tmux send-keys -t $SESSION:0.2 "docker logs -f dimutex_node3_1" C-m

# Divide verticalmente para painel 1: node2
tmux split-window -v -t $SESSION:0
tmux send-keys -t $SESSION:0.3 "docker logs -f dimutex_node4_1" C-m

# Divide verticalmente para painel 1: node2
tmux split-window -v -t $SESSION:0
tmux send-keys -t $SESSION:0.4 "docker logs -f dimutex_node5_1" C-m

# Deixa janelas do mesmo tamanho
tmux select-layout -t $SESSION:0 even-vertical

# Anexa à sessão
tmux attach-session -t $SESSION
