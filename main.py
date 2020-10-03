# -*- coding: utf-8 -*-

import os,sys
from datetime import datetime

from wh2_script import wh_file_manage
import wh_run,ffmpeg_run


#Path Setting
#path = sys.argv[2]
# path = r"H:\Park_doc\wormhole\Test_shot_BigBuck\export\test"
path = "/Users/jonghopark/Desktop/Wormhole2/BIgbuck_bunny/Anim_Data_burnin"
#업로드할 프로젝트 에피소드 선택
project_idx, project_name= wh_run.project_select()
episode_idx, episode_name = wh_run.episode_select(project_idx=project_idx)

#FFmpeg 세팅
ffmpeg = ffmpeg_run.FFMPEG_RUN(path)


Wh_file = wh_file_manage.File(split_text = "_",
                              project= project_name,
                              episode= episode_name,
                              sequence= [1],
                              shot= [1, 2],
                              task="")

#big_s0010_c002220_animation_v001.mov
# 0 _  1  _   2   _     3  _   4
#Splite Text나눈 단위를 다시 Splite Text로 합쳐서 붙힘.


#Path내 파일 체크.
file_list = Wh_file.file_dict(path)

print(file_list)

#new File_list 체크
print('새롭게 추가할 데이터를 추출 중 입니다.')
new_file_list = wh_run.compared_list(project_idx=project_idx,episode_idx=episode_idx,file_list=file_list)

print("추출 완료")


print('파일의 메타데이터를 추출 중 입니다.')
for file in new_file_list:
    file_name = file['file']
    length = ffmpeg.media_length(file_name)
    file.update(length)
print("메타데이터 추출 완료")

###
print("썸네일 추출중 입니다")
for file in new_file_list:
    thumbnail_file_name = {"thumbnail":os.path.splitext(file['file'])[0]+'.jpg'}
    file.update(thumbnail_file_name)

file_full_path_list = []
for file in new_file_list:
    file_full_path = [path,file["file"]]
    file_full_path_list.append(("/").join(file_full_path))

thumbnail_output_folder = ffmpeg.make_thumbnail(file_full_path_list)
print("썸네일 추출완료")



# 기본값 설정
sequence_name =[]
shot_name = []
attached = []
original_edit_path = file_full_path_list
length = []
description = []
direction_note = []

# 벌크업용 데이터 세팅
for file in new_file_list:
    sequence_name.append(file['sequence'])
    shot_name.append(file['shot'])
    attached.append(thumbnail_output_folder +"/"+file['thumbnail'])
    original_edit_path.append(path+"/" + file['file'])
    length.append(file['length'])
    description.append('Created Date : '+str(datetime.today().strftime("%Y/%m/%d %H:%M")))
    direction_note.append("")





bulk_run = ""

while bulk_run != "y" and bulk_run !='n':
    bulk_run = input("%s개의 데이터를 등록 하려고 합니다. 진행 하시겠습니까? \n 'yes' or 'no'" % (len(new_file_list)))



if bulk_run == "y":
    wh_run.wh2api.shot.bulk_create(project_idx=project_idx,
                                   episode_idx=episode_idx,
                                   sequence_name=sequence_name,
                                   shot_name=shot_name,
                                   description=description,
                                   direction_note=direction_note,
                                   thumbnail=attached,
                                   length=length,
                                   original_edit_path=original_edit_path)
elif bulk_run == 'n':
    print("사용자에 의해 프로세스가 중지 되었습니다.")