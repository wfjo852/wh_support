# -*- coding: utf-8 -*-
import os, json


#각종 경로 처리
install_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# print(install_path)
ffmpeg_path = install_path + "/exec"
font_path = install_path + "/exec"
login_path = install_path + "/setting"
file_format_path = install_path + "/setting"
file_type_path = install_path + "/setting"



#import하는 파일의 타입 추가

file_type_read = open(file_type_path+"/file_type.json",'r',encoding="utf-8")
file_type_load = json.load(file_type_read)


import_ext =file_type_load['import_ext']
split_text = file_type_load['split_text']
