#! /bin/bash

SAVE_DIR=$(pwd)

RM_DATAWORK="rm -R ./datawork"
RM_LOG="rm -R ./log"

BIN="../../../../OpenUxAS/build/uxas"

mkdir -p RUNDIR_Blockade
cd RUNDIR_Blockade
$RM_DATAWORK
$RM_LOG
$BIN -cfgPath ../cfg_Blockade.xml