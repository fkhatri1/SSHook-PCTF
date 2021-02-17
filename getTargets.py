#!/usr/bin/env python3
import swpag_client
import os
import time

GAME_URL = 'http://52.52.83.248'    # Team interface
FLAG_TOKEN = '6rykmdB99cYyrCcOqJv2'  # Must keep this token secret. Anyone with this token can log in as team.

TARGET_DIR = "/home/ctf/targets"

if not os.path.exists(TARGET_DIR):
	os.mkdir(TARGET_DIR)

t = swpag_client.Team(GAME_URL, FLAG_TOKEN)
svc_list = t.get_service_list()

# create directories
svc_ids = []
for svc in svc_list:
	sid = svc['service_id']
	svc_ids.append(sid)
	sid_dir = os.path.join(TARGET_DIR, str(sid))
	if not os.path.exists(sid_dir):
		os.mkdir(sid_dir)


# assumes that tick_ids are incremented by 1 for every new tick
tick_id = -1
while True:
	tick_info = t.get_tick_info()
	if tick_id >= tick_info['tick_id']:
		secs = min(60, max(1, tick_info['approximate_seconds_left']))
		time.sleep(secs)
		continue

	tick_id = tick_info['tick_id']
	for sids in svc_ids:
		sid_dir = os.path.join(TARGET_DIR, str(sid))

		# remove stale target files
		files = os.listdir(sid_dir)
		for f in files:
			try:
				file_tid = int(f[:4])
				if file_tid < tick_id - 5:
					os.remove(os.path.join(sid_dir, f))
			except:
				pass

		# create files with target information
		for target in t.get_targets(sids):
			fname = '{tick_id:04d}_{hostname}_{flag_id}'.format(tick_id=tick_id, **target)
			with open(os.path.join(sid_dir, fname), 'a'):  
				pass
