# -*- coding: utf-8 -*-

import os


class File:
    def __init__(self,split_text,project_idx=[],episode_idx=[],sequence_idx=[],shot_idx=[],task_idx=[]):


        self.split_text = split_text
        self.project_idx = project_idx
        self.episode_idx = episode_idx
        self.sequence_idx = sequence_idx
        self.shot_idx = shot_idx
        self.task_idx = task_idx

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
            result_text = {"project":self.join_name(file_split,self.project_idx),
                           "episode":self.join_name(file_split,self.episode_idx),
                           "sequence":self.join_name(file_split,self.sequence_idx),
                           "shot":self.join_name(file_split,self.shot_idx),
                           "task":self.join_name(file_split,self.task_idx),
                           "file":file}

            # 결과값 추가
            result.append(result_text)

            #웜홀에 체크해야 하는 프로젝트 에피소드 시퀀스 리스트
            create_check_text= {"project":self.join_name(file_split,self.project_idx),
                           "episode":self.join_name(file_split,self.episode_idx),
                           "sequence":self.join_name(file_split,self.sequence_idx)}

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