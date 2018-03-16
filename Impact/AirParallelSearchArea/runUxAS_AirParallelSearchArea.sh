#! /bin/bash

SAVE_DIR=$(pwd)

RM_DATAWORK="rm -R ./datawork"
RM_LOG="rm -R ./log"

BIN="../../../../OpenUxAS/build/uxas"

mkdir -p RUNDIR_AirParallelSearchArea
cd RUNDIR_AirParallelSearchArea
$RM_DATAWORK
$RM_LOG
$BIN -cfgPath ../cfg_AirParallelSearchArea.xml -runUntil 5