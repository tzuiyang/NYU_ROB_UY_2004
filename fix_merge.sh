#!/bin/bash
cd /home/pi/team_daniel_jo_souta/NYU_ROB_UY_2004
export GIT_EDITOR=true
git commit --no-edit --allow-empty -m "Merge upstream/main into local branch"
status=$?
echo "Merge completed with status: $status"
