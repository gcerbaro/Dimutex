#!/bin/bash

SESSION="dimutex-nodes"

# Cria nova sessão tmux em modo detached
tmux new-session -d -s $SESSION

# No primeiro painel, roda docker logs do node1
tmux send-keys -t $SESSION:0 "docker logs -f node1" C-m

# Divide a janela verticalmente para o node2
tmux split-window -v -t $SESSION:0
tmux send-keys -t $SESSION:0.1 "docker logs -f node2" C-m

# Divide a janela horizontalmente para o node3
tmux split-window -h -t $SESSION:0.0
tmux send-keys -t $SESSION:0.2 "docker logs -f node3" C-m

# Vai para o painel do node2 e divide horizontalmente para node4
tmux split-window -h -t $SESSION:0.1
tmux send-keys -t $SESSION:0.3 "docker logs -f node4" C-m

# Vai para o painel do node4 e divide verticalmente para node5
tmux split-window -v -t $SESSION:0.3
tmux send-keys -t $SESSION:0.4 "docker logs -f node5" C-m

# Anexa à sessão para você ver os painéis
tmux attach-session -t $SESSION
