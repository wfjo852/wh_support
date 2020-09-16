# -*- coding: utf-8 -*-

import getpass
from wh2api import wh
import wh2api

# wh_url = input("wormhole url : ")
# user_id = input('User ID : ')
# user_pw = getpass.getpass()

wh_url = "http://192.168.0.15"
user_id ="c2m"
user_pw ="c2m"

whlogin = wh.Login(wh_url = wh_url, user_id=user_id, user_pw=user_pw)


def project_select():

    project_list = wh2api.project.list()['projects']
    print("index \t project_name")

    project_dict = {}
    for project in project_list:
        project_dict_update = {project['project_idx']: project['name']}
        project_dict.update(project_dict_update)
        print(project['project_idx']+"\t"+project['name'])


    project_sel_idx = input("프로젝트를 선택 하세요.")
    if project_sel_idx in project_dict.keys():
        project_sel_name = project_dict[project_sel_idx]

        print('선택한 프로젝트의 이름은 %s 입니다.'%(project_sel_name))
        return project_sel_idx, project_sel_name
    else:
        pass


def episode_select(project_idx):
    episode_list = wh2api.episode.list(project_idx= project_idx)['episodes']
    print("index \t episode_name")

    episode_dict ={}
    for episode in episode_list:
        episode_dict_update = {episode['episode_idx'] : episode['name']}
        episode_dict.update(episode_dict_update)
        print(episode['episode_idx']+"\t"+ episode['name'])

    episode_sel_idx = input("에피소드를 선택 하세요.")
    episode_sel_name = episode_dict[episode_sel_idx]

    print('선택한 에피소드의 이름은 %s 입니다.'%(episode_sel_name))

    return episode_sel_idx,episode_sel_name
