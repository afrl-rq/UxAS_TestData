#! /bin/bash

SAVE_DIR=$(pwd)

RM_DATAWORK="rm -R ./datawork"
RM_LOG="rm -R ./log"

BIN="../../../../OpenUxAS/build/uxas"

mkdir -p RUNDIR_AirInspectPoint
cd RUNDIR_AirInspectPoint
$RM_DATAWORK
$RM_LOG
$BIN -cfgPath ../cfg_AirInspectPoint.xml