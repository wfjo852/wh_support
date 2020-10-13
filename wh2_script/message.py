# -*- coding: utf-8 -*-

#벌크 메시지(wh_bulk_shot_create.py)
bulk_new_file = "\n새롭게 추가할 데이터를 추가 중 입니다."
bulk_new_file_done = "추출 완료"

bulk_meta_file = "\n\n%s개 파일의 메타데이터를 추출 중 입니다."#%(len(new_file_list))
bulk_meta_file_done = "메타데이터 추출 완료"

bulk_thumbnail_create= "\n\n썸네일 추출중 입니다"
bulk_thumbnail_create_done = "썸네일 추출완료\n\n"

bulk_create_question = "%s개의 데이터를 등록 하려고 합니다. 진행 하시겠습니까?" #%(len(new_file_list)

bulk_created_list_export_question = "Bulk Create한 샷 목록을 엑셀로 출력 하시겠습니까?"
bulk_created_list_export_done = '\n\n엑셀 파일로 저장 되었습니다. \n'

#Thumbnail_Create(wh_thumbnail_make.py)
thumbnail_create_question =  "\n%s개의 영상 파일의 썸네일을 출력 하려고 합니다. 진행 하시겠습니까?"#%(len(file_list)
thumbnail_create_done = bulk_thumbnail_create_done

#Wormhole Run(wh_run.py)
wh_project_select = "project index를 선택 하세요."
wh_project_select_result = "선택한 프로젝트의 이름은 %s 입니다."#%(project_sel_name)
wh_episode_select = "Episode index를 선택 하세요."
wh_episode_select_result = "선택한 에피소드의 이름은 %s 입니다."#%(episode_sel_name)

wh_compared_list_error = "file_list의 정보가 정확하지 않습니다."

wh_login_file_data_none = "정보가 비어 있습니다. 다시 로그인 합니다. "
wh_login_file_none = "Login 기록이 없습니다. 로그인을 진행 합니다."

#process
process_stop = "사용자에의해 프로세스가 중지 되었습니다."
process_done = "프로세스가 완료 되었습니다."
process_select_error ="선택가능한 값이 아닙니다."

#file

file_example = "%s를 %s로 구분했습니다."#%(self.sample_file_name,self.split_text)

file_sequence_input = "\n이중 시퀀스에 해당하는 것을 순서대로 선택하세요 \n"
file_sequence_ex = "ex) %s를 이용해 작성하세요 1 or 2%s3" #%(self.split_text,self.split_text)
file_shot_input = "\n이중 샷에 해당하는 것을 순서대로 선택 하세요\n"
file_shot_ex = file_sequence_ex

file_info_blank = "\n정보가 비어있습니다. 다시 시작해 주세요."
file_continue = "해당 네이밍 규칙으로 진행 하시겠습니까?"
file_none = "\n파일 포맷 기록이 없습니다."