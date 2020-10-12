# -*- coding: utf-8 -*-

import subprocess, os, json, shutil

from wh2_script import wh_progress


class Wh_ffmpeg:

    def __init__(self, file_path, ffmpeg_location,font_location,tmp="/tmp",output="/output",thumbnail='_thumbnail'):
        self.file_path = file_path
        self.output_tmp_folder= file_path + tmp
        self.output_folder = file_path + output
        self.thumbnail_folder = file_path + thumbnail

        self.subprocess_folder = ffmpeg_location
        self.ffmpeg_path = r"%s/ffmpeg"%(ffmpeg_location)
        self.ffprobe_path = r"%s/ffprobe"%(ffmpeg_location)
        self.font_location = font_location
        self.fnull = open(os.devnull,"w")

    def ffprobe_file(self, file_name):
        input_file = '%s/%s' %(self.file_path,file_name)

        "ffprobe -v quiet -print_format json -show_format -show_meta -show_streams input.mp4"
        ffprobe_cmd = [self.ffprobe_path,
                       '-v', 'quiet',
                       '-print_format', 'json',
                       '-show_format',
                       '-show_streams',
                       input_file]
        ffprobe_cmd = " ".join(ffprobe_cmd)
        # print(ffprobe_cmd)
        result = subprocess.check_output(ffprobe_cmd).decode("utf-8")
        self.result_json = json.loads(result)
        return self.result_json



    def conv_file (self, input_file_name,output_file_name, convert_folder_name='tmp',bitrate=4000000):
        #'bitrate = int'
        input_file = self.file_path +"/"+ input_file_name
        output_file = self.file_path +"/"+ convert_folder_name + "/" + output_file_name

        output_folder = self.file_path +"/"+ convert_folder_name

        file_info_json = Wh_ffmpeg.ffprobe_file(self, input_file_name)
        if int(file_info_json['format']['bit_rate']) < bitrate:
            print('원본의 비트레이트 : ', file_info_json['format']['bit_rate'])
            print('원본의 비트레이트보다 설정한 비트레이트가 높습니다.')
            input('아무키나 누르세요.')
            pass
        else:
            if os.path.isdir(output_folder):
                print(output_folder)
                print("디렉토리 있음")
                pass
            else:
                os.mkdir(output_folder)
                print('디렉토리 생성')


            bitrate = str(bitrate)
            #비트레이트 텍스트로 변경

            file_conv_cmd = [self.ffmpeg_path,'-i',input_file,
                             '-b:v',bitrate,
                             '-maxrate',bitrate,
                             '-bufsize',bitrate,
                             '-y',
                             '-vf',f'pad=ceil(iw/2)*2:ceil(ih/2)*2',
                             output_file]
            file_conv_cmd = ' '.join(file_conv_cmd)
            subprocess.call(file_conv_cmd)

    def draw_text(self,
                  text,
                  font_size='60',
                  font='gulim.ttc',
                  text_y_location='0'):
        font_path = r'%s/%s'%(self.font_location,font)
        # print(font_path)
        draw_text = "drawtext=fontsize=%s:fontfile='%s':fontcolor=white:x=(w-text_w)/2:y=((h-text_h)/2)+%s:text='%s'" %(font_size, font_path, text_y_location, text)
        # print(draw_text)
        return draw_text

    def make_text_movie(self,
                        text=[],
                        font_size='60',
                        font='gulim.ttc',
                        text_y_offset=0,
                        output_file_name = "test.mp4",
                        video_res='1920x1080',
                        font_color='black'):
        # 기본 세팅
        draw_texts=[]
        font_location = 0-text_y_offset
        output_file_path = '%s/%s' %(self.output_tmp_folder, output_file_name)

        for x in text:
            result = Wh_ffmpeg.draw_text(self, x, text_y_location=str(font_location), font_size=font_size, font=font)
            font_location = font_location +int(font_size)
            draw_texts.append(result)

        draw_texts = ', '.join(draw_texts)


        make_text_movie_cmd = [self.ffmpeg_path,
                          '-f', 'lavfi',
                          '-i', 'color=c=%s:s=%s:d=0.001' % (font_color, video_res),
                          '-y',
                          '-r','24',
                          '-vf', '"%s"' % (draw_texts), output_file_path]

        make_text_movie_cmd = " ".join(make_text_movie_cmd)


        #tmp폴더 만들기
        if os.path.isdir(self.output_tmp_folder):
            pass
        else:
            os.mkdir(self.output_tmp_folder)

        subprocess.call(make_text_movie_cmd)
        return output_file_path


    def merge_movie(self, contat_file_path, output_file_name):
        output_file_path = '%s/%s'%(self.output_folder,output_file_name)

        merge_movie_cmd = [self.ffmpeg_path,
                           '-f','concat',
                           '-safe', '0',
                           '-i',contat_file_path,
                           '-r', '24',
                           '-c','copy',
                           '-y',
                           '-vf', '"pad=ceil(iw/2)*2:ceil(ih/2)*2"',
                           output_file_path]
        merge_movie_cmd = " ".join(merge_movie_cmd)

        print(merge_movie_cmd)

        #output 폴더 만들기
        if os.path.isdir(self.output_folder):
            pass
        else:
            os.mkdir(self.output_folder)

        subprocess.call(merge_movie_cmd)
        return self.output_folder

    def make_concat_file(self,file=[]):
        # concat_file = open(self.file_path+"/concat_file.txt","w")
        concat_file = open("./concat_file.txt", "w")

        for x in file:
            print(x)
            text = "file '%s'\n"%(x)
            concat_file.write(text)
        concat_file.close()
        # self.concat_file_path =self.file_path+"/concat_file.txt"
        self.concat_file_path = "./concat_file.txt"
        return self.concat_file_path
    def remove_dir_tmp(self):
        os.remove(self.concat_file_path)
        shutil.rmtree(self.output_tmp_folder,ignore_errors=True )

    def make_thumbnail(self,file_path_list=[],image_size="1280*720",frame='1',overwrite="y"):


        for file_path,i in zip(file_path_list,range(0,len(file_path_list))):
            export_file_name = os.path.splitext(os.path.basename(file_path))[0]+'.jpg'
            make_thumbnail_cmd = [self.ffmpeg_path,
                                  '-i', file_path,
                                  '-aframes',frame,
                                  '-an',#오디오 비활성화
                                  '-vframes','1',#프레임 지정
                                  f'-{overwrite}',#덮어쓰기
                                  '-s',image_size,#아웃풋 사이즈
                                  '-vf', '"pad=ceil(iw/2)*2:ceil(ih/2)*2"',#홀수프레임 크기를 짝수로
                                  self.thumbnail_folder +"/"+ export_file_name]


            make_thumbnail_cmd = " ".join(make_thumbnail_cmd)

            # 썸네일 폴더 만들기
            if os.path.isdir(self.thumbnail_folder):
                pass
            else:
                os.mkdir(self.thumbnail_folder)

            subprocess.call(make_thumbnail_cmd,stdout= self.fnull, stderr=subprocess.STDOUT)

            #progress바 출력
            wh_progress.printProgress(i,len(file_path_list))

        return self.thumbnail_folder