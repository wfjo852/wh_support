# -*- coding: utf-8 -*-

import sys
import time


#Path Setting
path = sys.argv[2]
action = sys.argv[3]

# path = r"H:\Park_doc\wormhole\Test_shot_BigBuck\export\Anim_Data_burnin"
# action = "bulk_shot_create"

print(path,action," Progress running \n")

if action == 'bulk_shot_create':
    import wh_bulk_shot_create
    wh_bulk_shot_create.bulk_shot_create(path=path)


elif action =="thumbnail_create":
    import wh_thumbnail_make
    wh_thumbnail_make.make_thumbnail(path=path)

elif action =="logout":
    from wh2_script import global_setting
    login_json_write = open(global_setting.login_path + "/login.json", 'w', encoding="utf-8")
    login_json_write.close()
    print('Wormhole_logout_done')
