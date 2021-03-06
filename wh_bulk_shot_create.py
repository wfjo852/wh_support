# -*- coding: utf-8 -*-

import os,sys, time
from datetime import datetime
from prettytable import PrettyTable

from wh2_script import wh_file_manage, wh_excle, wh_progress,global_setting, message
import wh_run,ffmpeg_run



def bulk_shot_create(path):
    time.sleep(2)
    #table 세팅
    table=PrettyTable(['Project',"Episode",'Sequence','Shot','Length','File'])
    #파일의 포맷을 기록 하는 기능
    file_format_class = wh_file_manage.File_format(global_setting.split_text,os.listdir(path)[0])
    file_format = file_format_class.run()


    #업로드할 프로젝트 에피소드 선택
    project_idx, project_name= wh_run.project_select()
    episode_idx, episode_name = wh_run.episode_select(project_idx=project_idx)

    #파일 포맷 및 기본 정보 입력
    Wh_file = wh_file_manage.File(split_text = global_setting.split_text,
                                  project= project_name,
                                  episode= episode_name,
                                  sequence= file_format['sequence'],
                                  shot= file_format['shot'],
                                  task="")
    #FFmpeg 세팅
    ffmpeg = ffmpeg_run.FFMPEG_RUN(path)


    #Path내 파일 체크.
    file_list = Wh_file.file_dict(path)


    #기존 데이터와 비교
    print(message.bulk_new_file)
    new_file_list = wh_run.compared_list(project_idx=project_idx,episode_idx=episode_idx,file_list=file_list)
    print(message.bulk_new_file_done)
    #추가할 데이터 정리 완료(new_file_list)


    #메타데이터 추출 시작
    print(message.bulk_meta_file(len(new_file_list)))
    for file,i in zip(new_file_list,range(0,len(new_file_list))):
        file_name = file['file']
        length = ffmpeg.media_length(file_name)
        file.update(length)
        wh_progress.printProgress(i,len(new_file_list))

        #테이블 세팅
        table.add_row([project_name,episode_name,file['sequence'],file["shot"],length['length'],file_name])
    print(message.bulk_meta_file_done)
    #메타데이터 추출 완료


    #썸네일 추출 시작
    print(message.bulk_thumbnail_create)
    for file in new_file_list:
        thumbnail_file_name = {"thumbnail":os.path.splitext(file['file'])[0]+'.jpg'}
        file.update(thumbnail_file_name)

    file_full_path_list = []
    for file in new_file_list:
        file_full_path = [path,file["file"]]
        file_full_path_list.append(("/").join(file_full_path))

    thumbnail_output_folder = ffmpeg.make_thumbnail(file_full_path_list)
    print(message.bulk_thumbnail_create_done)
    #썸네일 추출 완료



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





    #벌크 업로드 여부 확인
    print(table)
    bulk_run= global_setting.q_input(message.bulk_create_question % (len(new_file_list)), ['y', 'n'])


    #벌크 업로드 실행
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
        print(message.process_stop)
        sys.exit(1)




    #엑셀 출력 여부 확인

    excle_write = global_setting.q_input(message.bulk_created_list_export_question,['y','n'])

    #엑셀로 출력
    if excle_write =='y':
        columns_header = ["project",'episode',"sequence","shot","length","file","thumbnail"]
        workbook =  wh_excle.Create_workbook("Created_shot_list")
        workbook.input_line(columns_header)
        for file in new_file_list:
            workbook.input_line([file['project'],
                                 file['episode'],
                                 file['sequence'],
                                 file['shot'],
                                 file['length'],
                                 path+"/"+file['file'],
                                 path+"/"+file['thumbnail']])

        workbook.save_file(path + "_Created_list.xlsx")
        print(message.bulk_created_list_export_done,path+"_Created_list.xlsx")
    else:
        print(message.process_stop)
        sys.exit(1)