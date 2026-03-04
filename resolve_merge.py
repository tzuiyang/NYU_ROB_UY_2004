#!/usr/bin/env python3
import os
import subprocess

os.chdir('/home/pi/team_daniel_jo_souta/NYU_ROB_UY_2004')

# Abort the current merge
result = subprocess.run(['git', 'merge', '--abort'], capture_output=True)
print("Merge aborted")

# Now reset to upstream/main
result = subprocess.run(['git', 'reset', '--hard', 'upstream/main'], capture_output=True, text=True)
print("Reset to upstream/main:")
print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

# Check final status
result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print("\nFinal status:")
print(result.stdout)
