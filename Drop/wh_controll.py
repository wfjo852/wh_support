# -*- coding: utf-8 -*-

import json

from wh2api import wh
import wh2api

wh = wh.Login('http://192.168.0.15','c2m','c2m')

def auto_process(file_list):
    for check in file_list['check']:
        print(check)
        #프로젝트,에피소드, 시퀀스등이 비어있는지 확인하고, 시퀀스안에 샷 리스트를 받아서 check_result로 넣음
        result = check_create(check['project'], check['episode'], check['sequence'])
        file_list["check_result"].append(result)

    #위에서 정리된 내용을 기준으로 누락된 샷 생성
    shot_create(file_list)
    return file_list

def check_create_run(file_list):
    for check in file_list['check']:
        #프로젝트,에피소드, 시퀀스등이 비어있는지 확인하고, 시퀀스안에 샷 리스트를 받아서 check_result로 넣음
        result = check_create(check['project'], check['episode'], check['sequence'])
        file_list["check_result"].append(result)

    return file_list

def check_create(project_name,episode_name,sequence_name):
    global wh_project_list, wh_episode_list,wh_sequence_list,wh_shot_list
    global project_idx,episode_idx,sequence_idx
    wh_project_name_dict = {}
    wh_episode_name_dict = {}
    wh_sequence_name_dict = {}

    #웜홀 프로젝트 리스트 조회
    wh_project_list = wh2api.project.list()


#프로젝트
    #웜홀 리스트에서 프로젝트가 없다면 경고창 띄움
    if wh_project_list['projects'] != None :

        #웜홀 프로젝트를 프로젝트 이름 : 인덱스 형태의 딕셔너리 리스트 생성
        for project in wh_project_list['projects']:
            wh_project_name_dict.update({project["name"]:project['project_idx']})

        # 위에서 만든 딕셔너리 리스트의 키와 업로드 하려는 파일의 프로젝트 이름이 동일한지 체크, 같다면 프로젝트 인덱스 변수 생성
        # 에피소드 리스트 조회
        if project_name in wh_project_name_dict.keys():
            project_idx = wh_project_name_dict[project_name]
            wh_episode_list = wh2api.episode.list(project_idx)
            print(project_name, project_idx)
        else:
            project_idx = None
            print('일치하는 프로젝트가 없습니다. 생성후 다시 진행해 주세요.')
            return '일치하는 프로젝트가 없습니다. 생성후 다시 진행해 주세요.'
    else:
        project_idx = None
        print(wh_project_list)
        print('웜홀에 등록된 프로젝트가 없습니다.')
        return '웜홀에 등록된 프로젝트가 없습니다.'


#에피소드
    #에피소드 리스트가 비어있다면 무조건 생성
    if wh_episode_list['episodes'] != None:
        #에피소드 리스트를 에피소드 이름 : 에피소드 인덱스 형태의 딕셔너리 리스트로 생성
        for episode in wh_episode_list['episodes']:
            wh_episode_name_dict.update({episode["name"]:episode['episode_idx']})


        #위에서 만든 딕셔터리 리스트의 키와 업로드 에피소드 이름이 동일한지 체크, 같다면 에피소드 네임 인덱스 변수 생성
        #시퀀스 리스트 조회
        if episode_name in wh_episode_name_dict.keys():
            episode_idx = wh_episode_name_dict[episode_name]
            wh_sequence_list = wh2api.sequence.list(project_idx,episode_idx)
            print(episode_name,episode_idx)

        #에피소드가 없을경우 생성
        else:
            episode_create = wh2api.episode.create(project_idx,episode_name)
            episode_idx = episode_create['episode']['idx']

            wh_sequence_list = wh2api.sequence.list(project_idx, episode_idx)
            print('Create',episode_name,episode_idx)

    # 에피소드 리스트가 비어있음 생성
    else:
        episode_create = wh2api.episode.create(project_idx, episode_name)
        episode_idx = episode_create['episode']['idx']

        wh_sequence_list = wh2api.sequence.list(project_idx, episode_idx)
        print('create',episode_name, episode_idx)

# 시퀀스
    #시퀀스 리스트가 비어있다면 무조건 생성
    if wh_sequence_list['sequences'] != None:

        #시퀀스 리스트를 시퀀스 이름: 시퀀스 인덱스 형태의 딕셔너리 리스트로 생성
        for sequence in wh_sequence_list['sequences']:
            wh_sequence_name_dict.update({sequence["name"]: sequence['sequence_idx']})

        # 위에서 만든 딕셔터리 리스트의 키와 업로드 시퀀스 이름이 동일한지 체크, 같다면 시퀀스 네임 인덱스 변수 생성
        # 샷 리스트 조회
        if sequence_name in wh_sequence_name_dict.keys():
            sequence_idx = wh_sequence_name_dict[sequence_name]

            wh_shot_list = wh2api.shot.list(project_idx, episode_idx, sequence_idx)
            print(sequence_name,sequence_idx)


        #시퀀스 없을때 생성
        else:
            sequence_create = wh2api.sequence.create(project_idx,episode_idx,sequence_name)
            sequence_idx = sequence_create['sequence']['idx']
            wh_shot_list = wh2api.shot.list(project_idx,episode_idx,sequence_idx)
            print('create',sequence_name, sequence_idx)

    #시퀀스 리스트가 비어있을때 생성
    else:
        sequence_create = wh2api.sequence.create(project_idx, episode_idx, sequence_name)
        sequence_idx = sequence_create['sequence']['idx']
        wh_shot_list = wh2api.shot.list(project_idx, episode_idx, sequence_idx)
        print('create',sequence_name, sequence_idx)


    #딕셔너리 형태로 넘김
    return {project_name:project_idx,episode_name:episode_idx,sequence_name:sequence_idx,"shots":wh_shot_list['shots']}

def shot_create(file_list):
    global check_result_shot_list

    # 파일에서 등록해야 하는 파일의 정보를 꺼내옴 프로젝트, 에피소드, 시퀀스
    for file_info in file_list['result']:
        project_name = file_info['project']
        episode_name = file_info['episode']
        sequence_name = file_info['sequence']
        # print(1,project_name,episode_name,sequence_name,file_info)


        # 파일의 이름을 기준으로 웜홀에 에피소드, 시퀀스의 인덱스가 있는지 체크
        for check_result in file_list['check_result']:
            if project_name in check_result.keys() and \
                    episode_name in check_result.keys() and \
                    sequence_name in check_result.keys():


                #시퀀스 안에 샷 목록이 없다면, 무조건 생성
                if check_result['shots'] == None :

                    shot = wh2api.shot.create(check_result[project_name],
                                              check_result[episode_name],
                                              check_result[sequence_name], file_info["shot"])

                    # 리턴된 샷 생성 정보를 가지고 샷리스트 조회된것과
                    create_shot_info = {"shot_idx": shot['shot']['idx'], "name": shot['shot']['name'],
                                        "shot_order": shot['shot']['order']}

                    print(check_result)
                    check_result["shots"].append(create_shot_info)
                    print(file_info['shot'], ": 생성")
                    break

                else:
                    #시퀀스 내에 샷리스트를 만들어서 비교하기위한 자료 만듬
                    check_result_shot_list = []
                    for check_shot_info in check_result['shots']:
                        check_result_shot_list.append(check_shot_info['name'])



                #일치하는 이름이 없다면 웜홀 api를 이용해 샷 생성
                if  file_info['shot'] in check_result_shot_list:
                    print(file_info['shot'],": 이미 존재 함")
                    break

                else:
                    shot = wh2api.shot.create(check_result[project_name],
                                              check_result[episode_name],
                                              check_result[sequence_name], file_info["shot"])

                    # 리턴된 샷 생성 정보를 가지고 샷리스트 조회된것과
                    create_shot_info = {"shot_idx": shot['shot']['idx'], "name": shot['shot']['name'],
                                        "shot_order": shot['shot']['order']}
                    check_result["shots"].append(create_shot_info)
                    print(file_info['shot'], ": 생성")
                    break


        else:
            continue

def shot_task_create(file_list):
    global select_check_result

    for file_info in file_list['result']:
        project_name = file_info['project']
        episode_name = file_info['episode']
        sequence_name = file_info['sequence']
        shot_name = file_info['shot']
        task_name = file_info['task']

        # 파일의 이름을 기준으로 웜홀에 에피소드, 시퀀스의 인덱스가 있는지 체크
        for check_result in file_list['check_result']:
            if project_name in check_result.keys() and \
                    episode_name in check_result.keys() and \
                    sequence_name in check_result.keys() and \
                    shot_name in check_result.keys():
                select_check_result = check_result
                break
            else:
                print('선택된 샷이 없음')



        # wh2api.shot_task.list()
