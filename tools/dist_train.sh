#!/usr/bin/env bash

DATASET=$1
CONFIG=$2
WORK_DIR=$3
GPUS=${GPUS:-4}
NNODES=${NNODES:-1}
NODE_RANK=${NODE_RANK:-0}
PORT=${PORT:-29500}
MASTER_ADDR=${MASTER_ADDR:-"127.0.0.1"}
PY_ARGS=${@:4}

PYTHONPATH="$(dirname $0)/..":$PYTHONPATH \
python -m torch.distributed.launch \
    --nnodes=$NNODES \
    --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR \
    --nproc_per_node=$GPUS \
    --master_port=$PORT \
    $(dirname "$0")/train.py \
    ../configs/$DATASET/$CONFIG.py \
    --work-dir=$WORK_DIR/$DATASET/$CONFIG/ \
    --launcher="pytorch" \
    ${PY_ARGS}