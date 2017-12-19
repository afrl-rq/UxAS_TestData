#! /bin/bash

SAVE_DIR=$(pwd)

RM_DATAWORK="rm -R ./datawork"
RM_LOG="rm -R ./log"

BIN="../../../../OpenUxAS/build/uxas"

mkdir -p RUNDIR_AirExpandSqPoint
cd RUNDIR_AirExpandSqPoint
$RM_DATAWORK
$RM_LOG
$BIN -cfgPath ../cfg_AirExpandSqPoint.xml -runUntil 5