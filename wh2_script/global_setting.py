# -*- coding: utf-8 -*-
import os, json

from . import message

#각종 경로 처리
install_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# print(install_path)
ffmpeg_path = install_path + "/exec"
font_path = install_path + "/exec"
login_path = install_path + "/setting"
file_format_path = install_path + "/setting"
file_type_path = install_path + "/setting"



#import하는 파일의 타입 추가 // file_type.json으로 저장해 두고 사용
file_type_read = open(file_type_path+"/file_type.json",'r',encoding="utf-8")
file_type_load = json.load(file_type_read)

import_ext =file_type_load['import_ext']
split_text = file_type_load['split_text']




#질문 처리
def q_input(q_text,answer_list=[],show=True):
    answer_text = ("/").join(answer_list)

    def Questions():
        if show == True:
            answer = input(q_text+"(%s) : "%(answer_text))
            return(answer)
        elif show == False:
            answer = input(q_text+" : ")
            return (answer)

    # 첫번째 질문
    answer=Questions()

    while answer not in answer_list:
        #선택 가능한것 외 선택 했을때
        print(message.process_select_error)
        answer = Questions()

    return answer
