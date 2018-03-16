#! /bin/bash

SAVE_DIR=$(pwd)

RM_DATAWORK="rm -R ./datawork"
RM_LOG="rm -R ./log"

BIN="../../../../OpenUxAS/build/uxas"

mkdir -p RUNDIR_SurfaceInspectRoute
cd RUNDIR_SurfaceInspectRoute
$RM_DATAWORK
$RM_LOG
$BIN -cfgPath ../cfg_SurfaceInspectRoute.xml -runUntil 5