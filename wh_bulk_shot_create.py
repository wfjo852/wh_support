# -*- coding: utf-8 -*-



import os,sys, time
from datetime import datetime

from wh2_script import wh_file_manage,wh_excle
import wh_run,ffmpeg_run



def bulk_shot_create(path):

    #파일의 포맷을 기록 하는 기능
    file_format_class = wh_file_manage.File_format("_",os.listdir(path)[0])
    file_format = file_format_class.run()


    #업로드할 프로젝트 에피소드 선택
    project_idx, project_name= wh_run.project_select()
    episode_idx, episode_name = wh_run.episode_select(project_idx=project_idx)

    #파일 포맷 및 기본 정보 입력
    Wh_file = wh_file_manage.File(split_text = "_",
                                  project= project_name,
                                  episode= episode_name,
                                  sequence= file_format['sequence'],
                                  shot= file_format['shot'],
                                  task="")
    #FFmpeg 세팅
    ffmpeg = ffmpeg_run.FFMPEG_RUN(path)


    #Path내 파일 체크.
    file_list = Wh_file.file_dict(path)


    #new File_list 체크
    print('\nn새롭게 추가할 데이터를 추출 중 입니다.')
    new_file_list = wh_run.compared_list(project_idx=project_idx,episode_idx=episode_idx,file_list=file_list)

    print("추출 완료")


    print('\n\n파일의 메타데이터를 추출 중 입니다.')
    for file in new_file_list:
        file_name = file['file']
        length = ffmpeg.media_length(file_name)
        file.update(length)
    print("메타데이터 추출 완료")

    ###
    print("\n\n썸네일 추출중 입니다")
    for file in new_file_list:
        thumbnail_file_name = {"thumbnail":os.path.splitext(file['file'])[0]+'.jpg'}
        file.update(thumbnail_file_name)

    file_full_path_list = []
    for file in new_file_list:
        file_full_path = [path,file["file"]]
        file_full_path_list.append(("/").join(file_full_path))

    thumbnail_output_folder = ffmpeg.make_thumbnail(file_full_path_list)
    print("썸네일 추출완료\n\n")



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
    bulk_run = ""

    while bulk_run != "y" and bulk_run !='n':
        bulk_run = input("%s개의 데이터를 등록 하려고 합니다. 진행 하시겠습니까? \n 'y' or 'n'\n" % (len(new_file_list)))


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
        print("사용자에 의해 프로세스가 중지 되었습니다.")
        sys.exit(1)




    #엑셀 출력 여부 확인
    excle_write =""

    while excle_write != "y" and excle_write != "n":
        excle_write = input("Bulk Create한 샷 목록을 엑셀로 출력 하시겠습니까? \n 'y' or 'n'\n")

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
        print('\n\n엑셀 파일로 저장 되었습니다. \n',path+"_Created_list.xlsx")
    else:
        print("사용자에 의해 프로세스가 중지 되었습니다.")
        sys.exit(1)