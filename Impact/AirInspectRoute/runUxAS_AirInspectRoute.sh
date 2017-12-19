#! /bin/bash

SAVE_DIR=$(pwd)

RM_DATAWORK="rm -R ./datawork"
RM_LOG="rm -R ./log"

BIN="../../../../OpenUxAS/build/uxas"

mkdir -p RUNDIR_AirInspectRoute
cd RUNDIR_AirInspectRoute
$RM_DATAWORK
$RM_LOG
$BIN -cfgPath ../cfg_AirInspectRoute.xml -runUntil 5