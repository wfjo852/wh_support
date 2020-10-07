# -*- coding: utf-8 -*-
import os

#각종 경로 처리
install_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(install_path)
ffmpeg_path = install_path + "/exec"
font_path = install_path + "/exec"
login_path = install_path + "/setting"
file_format_path = install_path + "/setting"

#import하는 파일의 타입 추가
import_ext =[".mov",".mp4"]