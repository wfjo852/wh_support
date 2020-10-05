# -*- coding: utf-8 -*-

import os, sys
from wh2_script import wh_ffmpeg

# Setting
movie_ext =['.mp4','.mov']
export_ext ='.mp4'
subprocess_path = "./exec"
font_path = "./exec"


class FFMPEG_RUN:
    def __init__(self,file_path):
        self.file_path = file_path
        self.ffmpeg = wh_ffmpeg.Wh_ffmpeg(self.file_path,subprocess_path,font_path)

    def media_length(self,file_name):
        ffprobe = self.ffmpeg.ffprobe_file(file_name=file_name)
        length=ffprobe['streams'][0]['nb_frames']
        return {"length": length}

    def make_thumbnail(self,file_path_list=[]):

        output_folder_path = self.ffmpeg.make_thumbnail(file_path_list,image_size="640*360",
                                                        frame= "1",
                                                        overwrite="n")
        return output_folder_path









# file_path = sys.argv[2]
# file_path = r"H:\Park_doc\wormhole\Test_shot_BigBuck\export\test"

# file_list = os.listdir(file_path)
#
#
# for file in file_list:
#     #파일 이름 , 파일 확장자로 분리
#     file_name, file_ext = os.path.splitext(file)
#
#     #파일의 확장자가 지정해 놓은 동영상 확장자안에 있는 경우 진행
#     if file_ext in movie_ext:
#         output_file_name = file_name + export_ext
#         ffmpeg.conv_file(file,output_file_name)
#         print("컨버팅 완료 : ",file,">>",output_file_name)
#     else:
#         print(file,": 영상 포맷이 맞지 않습니다.")