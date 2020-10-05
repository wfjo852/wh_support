# -*- coding: utf-8 -*-

import os
import json


class File:
    def __init__(self, split_text,
                 project=list or str,
                 episode=list or str,
                 sequence=list or str,
                 shot=list or str,
                 task=list or str):


        self.split_text = split_text
        self.project = project
        self.episode = episode
        self.sequence = sequence
        self.shot = shot
        self.task = task

    def file_dict(self,file_path):
        #파일 리스트 조회
        file_list = os.listdir(file_path)

        #기본 변수 세팅
        result =[]
        create_check = []

        #파일 확장자 제거 및 조합하는 규칙 기준으로 파일의 프로젝트, 에피소드,시퀀스를 설정함
        for file in file_list:
            file_name = os.path.splitext(file)[0]#확장자 제거
            file_split = file_name.split(self.split_text)#split 기호로 나누기

            #결과값
            result_text = {"project":self.join_name(file_split, self.project),
                           "episode":self.join_name(file_split, self.episode),
                           "sequence":self.join_name(file_split, self.sequence),
                           "shot":self.join_name(file_split, self.shot),
                           "task":self.join_name(file_split, self.task),
                           "file":file}

            # 결과값 추가
            result.append(result_text)

            #웜홀에 체크해야 하는 프로젝트 에피소드 시퀀스 리스트
            create_check_text= {"project":self.join_name(file_split, self.project),
                           "episode":self.join_name(file_split, self.episode),
                           "sequence":self.join_name(file_split, self.sequence)}

            #체크 값 추가
            create_check.append(create_check_text)

        #리스트 딕셔너리의 딕셔너리가 중복된것은 없애고 고유값만 남긴채로 리스트 재정리
        create_check_result = list(map(dict, set(tuple(sorted(data.items())) for data in create_check)))

        # 딕셔너리 형태로 출력
        # return {"result":result,"check":create_check_result,"check_result":[]}
        return {"result":result}

    #문자 조합.
    def join_name(self,file_split,join_idx):

        result = []

        if join_idx != [] and type(join_idx) != str : #입력값이 리스트가 비어있지 않고,스트링이 아닌경우
            for idx in join_idx:
                result.append(file_split[int(idx)])
        elif type(join_idx) == str : #입력값이 문자일경우
            return join_idx
        else:
            return ""

        return (self.split_text).join(result)




#파일 포맷 물어보기

def file_format(split_text,sample_file_name):
    print(sample_file_name,"를",f"'{split_text}'","로 구분했습니다.")
    file_name = os.path.splitext(sample_file_name)[0]  # 확장자 제거
    file_split = file_name.split(split_text)  # split 기호로 나누기
    idx = 0
    for text in file_split:
        print(idx,":",text)
        idx = idx +1
    sequence = input("이중 시퀀스에 해당하는 것을 순서대로 선택하세요 \n ex) 1 or 2,3")
    shot = input("이중 샷에 해당하는 것을 순서대로 선택 하세요\n ex) 2 or 2,3")

    return sequence,shot

try:
    file_format_read = open("./setting/file_format.json","r",encoding="utf-8")
    file_format_info = json.load(file_format_read)

    if file_format_info["sequence"] !="" and file_format_info["shot"] !="":

    else:
        print("정보가 비어있습니다. 다시 시도합니다.")

except:
    print("파일 포맷 기록이 없습니다.")
