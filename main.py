# -*- coding: utf-8 -*-

import os,sys

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
                              project_idx = project_name,
                              episode_idx = episode_name,
                              sequence_idx = [1],
                              shot_idx = [1,2],
                              task_idx = "")

#big_s0010_c002220_animation_v001.mov
# 0 _  1  _   2   _     3  _   4
#Splite Text나눈 단위를 다시 Splite Text로 합쳐서 붙힘.


#Path내 파일 체크.
file_list = Wh_file.file_dict(path)


print('파일의 메타데이터를 추출 중 입니다.')
for file in file_list['result']:
    file_name = file['file']
    length = ffmpeg.media_length(file_name)
    file.update(length)
print("Done")
print(file_list)

