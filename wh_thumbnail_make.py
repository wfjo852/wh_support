#-*- coding:utf-8 -*-
import os,sys


import ffmpeg_run
from wh2_script import global_setting



#파일 리스트 조회
def file_dict(file_path):
    # 파일 리스트 조회
    file_list = []
    for file in os.listdir(file_path):
        if os.path.splitext(file)[1] in global_setting.import_ext:
            file_list.append(file)

    return file_list



def make_thumbnail(path):
    #FFmpeg 세팅
    ffmpeg = ffmpeg_run.FFMPEG_RUN(path)

    #Path내 파일 체크.
    file_list = file_dict(path)


    #파일에 풀패스 리스트로 전환
    file_full_path_list = []
    for file in file_list:
        file_full_path = [path,file]
        file_full_path_list.append(("/").join(file_full_path))

    thumbnail_run = ""

    while thumbnail_run != "y" and thumbnail_run != 'n':
        thumbnail_run = input("\n%s개의 영상 파일의 썸네일을 출력 하려고 합니다. 진행 하시겠습니까? \n 'y' or 'n'\n" % (len(file_list)))

    if thumbnail_run =="y":
        thumbnail_output_folder = ffmpeg.make_thumbnail(file_full_path_list)
        print("썸네일 추출완료")

    elif thumbnail_run == "n":
        print("사용자에 의해 프로세스가 중지 되었습니다.")
        sys.exit(1)