# -*- coding: utf-8 -*-

import sys


#Path Setting
path = sys.argv[2]
action = sys.argv[3]
print(path,action," Progress running \n")



if action == 'bulk_shot_create':
    import wh_bulk_shot_create
    wh_bulk_shot_create.bulk_shot_create(path=path)


elif action =="thumbnail_make":
    import wh_thumbnail_make
    wh_thumbnail_make.make_thumbnail(path=path)