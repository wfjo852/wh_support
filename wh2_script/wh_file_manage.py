# -*- coding: utf-8 -*-

import os
import json
from wh2_script import global_setting, message


class File:
    def __init__(self, split_text,
                 project=list or str,
                 episode=list or str,
                 sequence=list or str,
                 shot=list or str,
                 task=list or str,
                 ext = global_setting.import_ext):

        self.ext = ext
        self.split_text = split_text
        self.project = project
        self.episode = episode
        self.sequence = sequence
        self.shot = shot
        self.task = task

    def file_dict(self,file_path):
        #파일 리스트 조회
        file_list = []
        for file in os.listdir(file_path):
            if os.path.splitext(file)[1] in self.ext:
                file_list.append(file)

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

        # result 리스트안에 값이 1개인 경우
        if len(result) ==1:
            return result[0]
        else:
            return (self.split_text).join(result)




#파일 포맷 물어보기

class File_format:
    def __init__(self,split_text,sample_file_name):

        self.split_text = split_text
        self.sample_file_name = sample_file_name
        self.file_name = os.path.splitext(sample_file_name)[0]  # 확장자 제거
        self.file_split = self.file_name.split(split_text)  # split 기호로 나누기
        self.file_format_info=""

    #json파일을 만드는 함수
    def make_json(self):
        #샘플용 파일네임을 보여줌.
        print(message.file_example %(self.sample_file_name,self.split_text))
        idx = 0
        for text in self.file_split:
            print(idx,":",text)
            idx = idx +1
        sequence = input(message.file_sequence_input + message.file_sequence_ex % (self.split_text, self.split_text))
        shot = input(message.file_shot_input + message.file_shot_ex % (self.split_text, self.split_text))

        #file_format json파일 생성
        file_format_write = open(global_setting.file_format_path + "/file_format.json", "w", encoding="utf-8")

        file_format_info = {"sequence":sequence.split(self.split_text),"shot":shot.split(self.split_text)}
        json.dump(file_format_info,file_format_write)
        file_format_write.close()
        return self.run()

    #split name으로 묶는 함수
    def join_name(self,join_idx):

        result = []

        if join_idx != [] and type(join_idx) != str : #입력값이 리스트가 비어있지 않고,스트링이 아닌경우
            for idx in join_idx:
                result.append(self.file_split[int(idx)])
        elif type(join_idx) == str : #입력값이 문자일경우
            return join_idx
        else:
            return ""

        if len(result) ==1:
            return result[0]
        else:
            return (self.split_text).join(result)


    #최초 실행
    def run(self):
        #파일 유무 확인
        try:
            file_format_read = open(global_setting.file_format_path + "/file_format.json", "r", encoding="utf-8")
            file_format_info = json.load(file_format_read)

            #파일 포맷 규칙에 따라 결과값 추출
            if file_format_info["sequence"] !="" and file_format_info["shot"] !="":
                sequence = self.join_name(file_format_info['sequence'])
                shot = self.join_name(file_format_info['shot'])
                print("\n",self.sample_file_name,"\nsequence name : ",sequence,"\nshot name :",shot)

            #파일 포맷json파일 안에 데이터가 부족한 경우
            else:
                print(message.file_info_blank)
                self.make_json()


            #파일 포맷 json파일의 리셋 여부 확인
            reset = ""
            while reset != 'y' and reset != 'n':
                reset = global_setting.q_input(message.file_continue,['y','n'])

            if reset =="y":
                return file_format_info

            elif reset == "n":
                return self.make_json()
            else:
                print("error")

        #파일 없음 json 파일 만듬
        except:
            print(message.file_none)
            self.make_json()


