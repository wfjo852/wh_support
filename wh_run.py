# -*- coding: utf-8 -*-

import getpass
import json
from prettytable import PrettyTable

from wh2_script import global_setting
from wh2api_internal import wh
import wh2api_internal as wh2api

def wh_login():
    wh_url = input("wormhole url : ")
    user_id = input('User ID : ')
    user_pw = getpass.getpass()

    # wh_url = "http://localhost"
    # user_id = "c2m"
    # user_pw = "c2m"

    wh_login = wh.Login(wh_url = wh_url, user_id=user_id, user_pw=user_pw)
    wh_token = wh_login.whtoken['whtoken']
    login_json_write = open(global_setting.login_path + "/login.json", 'w', encoding="utf-8")
    login_json_file = {"wh_url": wh_url, "user_id": user_id, "wh_token": wh_token}
    json.dump(login_json_file,login_json_write)
    login_json_write.close()

    return wh_token

def project_select():

    project_list = wh2api.project.list()['projects']

    #테이블 세팅
    table = PrettyTable(['index','project_name'])

    project_dict = {}
    for project in project_list:
        project_dict_update = {project['idx']: project['name']}
        project_dict.update(project_dict_update)
        table.add_row([project['idx'],project['name']])

    #테이블 출력
    print(table)
    project_sel_idx = global_setting.q_input("project index를 선택 하세요.",project_dict.keys(),False)
    project_sel_name = project_dict[project_sel_idx]

    print('선택한 프로젝트의 이름은 %s 입니다.'%(project_sel_name))
    return project_sel_idx, project_sel_name


def episode_select(project_idx):
    episode_list = wh2api.episode.list(project_idx= project_idx)['episodes']
    table = PrettyTable(['index','Episode_name'])

    episode_dict ={}
    for episode in episode_list:
        episode_dict_update = {episode['idx'] : episode['name']}
        episode_dict.update(episode_dict_update)
        table.add_row([episode['idx'],episode['name']])

    #테이블 출력
    print(table)
    episode_sel_idx = global_setting.q_input("Episode index를 선택 하세요.",episode_dict.keys(),False)
    episode_sel_name = episode_dict[episode_sel_idx]

    print('선택한 에피소드의 이름은 %s 입니다.'%(episode_sel_name))
    return episode_sel_idx,episode_sel_name

def shot_bulk_list(project_idx,episode_idx):
    wh_compare_list=[]

    wh_shot_list = wh2api.shot.list(project_idx=project_idx,episode_idx=episode_idx)
    for shot in wh_shot_list["shots"]:
        compare_name = shot['sequence_name']+"_"+shot['shot_name']
        wh_compare_list.append(compare_name)
    return wh_compare_list

def compared_list(project_idx,episode_idx,file_list):
    new_file_list =[]

    if 'result' in file_list:

        wh_compare_list = shot_bulk_list(project_idx=project_idx,episode_idx=episode_idx)

        for file in file_list['result']:
            compared_name = file['sequence']+"_"+file['shot']
            if compared_name in wh_compare_list:
                pass
            else:
                new_file_list.append(file)

    else:
        print("file_list의 정보가 정확하지 않습니다.")
        return 'error'


    return new_file_list





#login Info파일 유무 및 유효성 검사
try:
    login_json_read = open(global_setting.login_path + "/login.json", 'r', encoding="utf-8")
    login_info = json.load(login_json_read)

    if login_info['wh_token'] != "" and login_info['wh_url'] != "" and login_info['user_id'] != "":
        wh_url = login_info['wh_url']
        user_id = login_info['user_id']
        wh_token = login_info['wh_token']

        wh.Login(wh_url=wh_url, user_id=user_id, wh_token=wh_token)

    else:
        print("정보가 비어 있습니다. 다시 로그인 합니다. ")
        wh_login()

except:
    print("Login 기록이 없습니다. 로그인을 진행 합니다.")
    wh_login()






