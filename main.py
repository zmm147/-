import json
import threading
import tkinter
import datetime
from tkinter import filedialog
import pysrt
import vlc
import tkinter as tk
import re
import shutil
from PyQt5.QtCore import QUrl, Qt, QThread, pyqtSignal, QCoreApplication, QObject
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QMenu, \
    QAction
import os.path
import csv
from moviepy.editor import *
from readmdict import MDX, MDD
import sys

sys.setrecursionlimit(sys.getrecursionlimit() * 5)

# from typing import Any
subtitle = ""
video_name = "aino10.mp4"
part = {}
app1 = None  # 将 QApplication 实例设置为全局变量
audio_path = ""
new_string_old = ""
cssfile = '''
<!DOCTYPE html>
<html>
<head>
<script>
document.addEventListener("DOMContentLoaded", function() {
  var radios = document.querySelectorAll('input[type="radio"][name="options"]');

  radios.forEach(function(radio) {
    radio.addEventListener("change", function() {
      if (this.checked) {
        var labelText = this.parentNode.innerHTML;
        console.log(labelText);
      }
    });
  });
});
</script>
<style>
body {margin:0; padding: 0; word-wrap: break-word!important; font-family: "Helvetica Neue",Helvetica, Arial,"PingFang SC","Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;line-height:1.2em;}

div.text_prons, span.hpron_word, div.fl {display:inline;padding-right:5px;}
div.d_hidden {display:none}
/*ul {margin:0;padding:0;}*/
/*li {margin:0 0 0 15px;padding:0 0 0 5px;}*/
div.hw_infs_d, div.labels, span.gram {display:inline;}

#ld_entries_v2_mainh{font-size:180%;font-weight:bold;color:#003399;}
#ld_entries_v2_others_block{margin-top:5px;}
#ld_entries_v2_others_block > .o_count{color:#777777;margin-bottom:4px;margin-top:0px;font-variant: small-caps;}
#ld_entries_v2_others_block > .o_list{}
#ld_entries_v2_others_block > .o_list{border:1px solid #ccc;list-style-type: none;padding:0px;margin:0px;height: 72px;overflow: hidden;overflow-y: auto;}
#ld_entries_v2_others_block > .o_list > li{margin:0;padding:0;}
#ld_entries_v2_others_block > .o_list > li > a{padding: 4px 3px 4px 15px;text-decoration: none;display:block;font-weight:bold;}
#ld_entries_v2_others_block > .o_list > li > a.selected:first-child{background-color:#E8F5F6;color:#000;}
#ld_entries_v2_others_block > .o_list > li > a:hover{background-color:#F0F0F0;color:black;}
#ld_entries_v2_others_block > .o_list > li > a > span{font-weight:normal !important;}
#ld_entries_v2_all{padding:10px;border:1px solid #ccc;border-radius:10px;margin:auto;position:relative;}

/*delete save part for GD*/
#ld_entries_v2_all > .save_faves > .txt{display:none;}

/*utils*/
.entry_v2 .vfont{display:none;} /*for GD*/

/*mw markup overrides*/
.entry_v2 .mw_spm_aq{color:#000;margin:0;padding:0;padding:0;border:none;}

/*Dotted line*/
.entry_v2 .dline {display:none;}

/*non-HW prons*/
.entry_v2 .pron_l_b{}
.entry_v2 .pron_l_a{}
.entry_v2 .pron_w{color:#717274;font-weight:normal;font-size:109%;}
.uro_line .pron_w{color:#717274;font-weight:normal;font-size:109%;}
.entry_v2 .pron_i{color:#D40218;}
.entry_v2 .pron_i:hover{color:#FF0000;text-decoration: none;}

/*non-HW variations*/
.entry_v2 .v_label{font-style: italic;color:#009900;}
.entry_v2 .v_text{font-weight:bold;}

/*non-HW inflections*/
.entry_v2 .i_label{font-style:italic;color:#757575;}
.entry_v2 .i_text{font-weight:bold; color:#0B5BC4;}
.uro_line > .i_label{font-weight:bold; color:#757575;}
.uro_line > .i_text{font-weight:bold; color:#0B5BC4;}

/*single word entry resets*/
.entry_v2 p {margin:0;padding:0 0 10px 0;font-weight:normal;}
.entry_v2 a{color:#1122CC;text-decoration:none;}
.entry_v2 a:hover{text-decoration:underline;}
.sms a{color:#1122CC;text-decoration:none; font-size: 110%; }
.sms a:hover{text-decoration:underline;}
.sms {color: #808080; font-size: 90%;}
.entry_v2 > .goto_main::before {content: "⇒ Main Entry: "; color:#808080; display: inline; font-size: 90%;} 

/*desktop: headword*/
.entry_v2 > .hw_d{font-size: 95%;margin: 0px -10px 1em -10px;background-color: #E7F5F5;padding: 0 50px 0 20px;position: relative;}
.entry_v2 > .hw_d.hw_0{border-top-left-radius:10px;border-top-right-radius:10px;margin:-10px -10px 1em -10px;}
.entry_v2 > .hw_d.hw_0.hw_wod{margin:0;background-color:transparent;padding:10px 0px;}
.entry_v2 > .hw_d > * {position:relative;vertical-align:middle;}
.entry_v2 > .hw_d > .hw_txt{font-size:150%; font-weight: bold; color:#032952; line-height: 1.5em;}
.entry_v2 > .hw_d > .hw_txt > sup{margin-right:2px;}
.entry_v2 > .hw_d > .hsl{margin-left:6px;font-style:italic;}
.entry_v2 > .hw_d > .hpron_label_a{margin-left:7px;}
.entry_v2 > .hw_d > .hpron_label_b{margin-left:7px;}
.entry_v2 > .hw_d > .hpron_word{color:#525157;font-weight:normal;margin-left:17px;font-size:109%;}
.entry_v2 > .hw_d > .hpron_icon{color:#D40218;font-size:110%;margin-left:7px;}
.entry_v2 > .hw_d > .hpron_icon:hover{text-decoration: none;}
.entry_v2 > .hw_d > .fl{color:#8f0610;font-style:italic;font-weight: bold;margin-left:8px;}
.uro_line > .fl{color:#8f0610;font-style:italic;font-weight: bold;margin-left:8px;}
.dro_line > .dre{font-size:145%; font-weight: bold; color:#032952;}
.uro > .uro_line > .ure{font-size:145%; font-weight: bold; color:#032952;}

/*desktop: headword variations*/
.entry_v2 > .hw_vars_d{margin-bottom:.6em;}

/*desktop: headword inflections*/
.entry_v2 > .hw_infs_d{margin-bottom:.6em;}


/*view: entry level labels*/
.entry_v2 > .labels{margin:0;}
.entry_v2 > .labels > .lb{font-style:italic;}
.entry_v2 > .labels > .gram{}
.entry_v2 > .labels > .gram > .gram_internal{color:#009900;}
.gram > .gram_internal{color:#009900;}
.entry_v2 > .labels > .sl{font-style:italic;}

/*view: phrasal verbs*/
.entry_v2 .pvl{}
.entry_v2 .pva{font-weight:bold;}

/*view: synonym paragraphs*/
.entry_v2 .synpar{border:1px solid #ccc;padding:4px 10px 6px 10px;margin-bottom:4em;}
.entry_v2 .synpar > .synpar_part{margin-bottom:5px;}
.entry_v2 .synpar > .synpar_part:last-child{margin-bottom:0;}
.entry_v2 .synpar > .synpar_part > .synpar_w{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 .synpar > .synpar_part > .syn_par_t{}
.entry_v2 .synpar > .synpar_part > *:last-child{margin-bottom:0;}

/*view: supplementary notes*/
.entry_v2 .snotes{margin-bottom:.5em;overflow:hidden;}
.entry_v2 .snotes > *{margin-bottom:0.4em;}
.entry_v2 .snotes > *:last-child{margin-bottom:0;}
.entry_v2 .snotes > .snote_text{}
.entry_v2 .snotes > .snote_text > .snote_link{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 .snotes > .snote_text > .snote_link sup{font-size:50%;}

/*view: supplementary noteboxes*/
.entry_v2 .snotebox{border:1px solid #ccc;padding:0.8em;margin-bottom:.5em;overflow:hidden;}
.entry_v2 .snotebox > .snotebox_text{text-align:justify;}
.entry_v2 .snotebox > .snotebox_text > .snote_link{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 .snotebox > .snotebox_text > .snote_link sup{font-size:50%;}

/*view: art*/
.entry_v2 .arts{margin-bottom:.5em;}
.entry_v2 .arts > .art{text-align: center;margin-bottom:4px;}
.entry_v2 .arts > .art:last-child{margin-bottom:0;}
.entry_v2 .arts > .art > img{border:1px solid #ddd;padding-top:0px;max-width:100%;}

/*view: usage note*/
.entry_v2 .un_text{}

/*view: sense blocks*/
.entry_v2 .sblocks{margin-bottom:.5em;}
.entry_v2 .sblocks > .sblock{width:100%;margin:0px 0px 0px 0px;}
.entry_v2 .sblocks > .sblock > .sblock_c{margin-bottom:4px;}
.entry_v2 .sblocks > .sblock > .sblock_c:last-child{margin-bottom:0;}
.entry_v2 .sblocks > .sblock > .sblock_c > .sn_block_num{float:left;font-weight:bold;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sblock_labels{}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sblock_labels > .slb{font-style:italic; color:#757575;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sblock_labels > .ssla{font-style:italic; color: #009900;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sblock_labels > .sgram{}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sblock_labels > .sgram > .sgram_internal{color:#009900;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sblock_labels > .bnote{font-weight:bold;font-style: italic;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sblock_labels > .vrs{}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sblock_labels > .infs{}

.entry_v2 .sblocks > .sblock > .sblock_c > .scnt{margin-bottom:4px;overflow:hidden;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt:last-child{margin-bottom:0;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense{}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > *:last-child{margin-bottom:0;padding-bottom:0;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .sn_letter{font-weight:bold;float:left;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .sd{font-style:italic;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .bnote{font-weight:bold;font-style:italic;color:#000;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .slb{font-style:italic; color:#757575;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .sgram{}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .sgram > .sgram_internal{color:#009900;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .ssla{font-style:italic;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .def_text{ font-size: 110%; margin-bottom:0px;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .def_text > .bc{font-weight:bold;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .def_labels{margin-top:5px;padding-left:14px;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .def_labels > .wsgram{}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .def_labels > .wsgram > .wsgram_internal{color:#009900;}
.entry_v2 .sblocks > .sblock > .sblock_c > .scnt > .sense > .def_labels > .sl{font-style:italic;}

/*view: verbal illustration*/
.entry_v2 .vis_w{padding-left:0em;}
.entry_v2 .vis_w > .vis{list-style-position:inside;list-style-position:outside;overflow:hidden;}
.entry_v2 .vis_w > .vis > .vi{padding:0;color:teal;}
.entry_v2 .vis_w > .vis > .vi::before {content: "●"; color:#5FB68C; display: inline; font-size: 60%}
.entry_v2 .vis_w > .vis > .vi > .vi_content{color:#000;margin-left:.2em; display: inline;}

/*view: dros*/
.entry_v2 > .dros{margin-bottom:.5em;}
.entry_v2 > .dros > .dro{margin-bottom:0.4em;padding-left:0.4em;}
.entry_v2 > .dros > .dro:last-child{margin-bottom:0;}
.entry_v2 > .dros > .dro > .dro_line{margin-left:-0.4em;}
.entry_v2 > .dros > .dro > .dro_line > *{vertical-align: middle}
.entry_v2 > .dros > .dro > .dro_line > .dre{display:inline;font-weight:bold;padding:0;margin:0;font-size:110%;color:#032952;}
.entry_v2 > .dros > .dro > .dro_line > .gram > .gram_internal{color:#009900; font-weight: bold; font-style:italic;}
.entry_v2 > .dros > .dro > .dro_line > .sl{font-style:italic; color:#009900;}
.entry_v2 > .dros > .dro > .dro_line > .rsl{font-style:italic;}
.entry_v2 > .dros > .dro > .dxs{margin-top:0.3em;display:block;}

/*view: uros*/
.entry_v2 > .uros{margin-bottom:.5em;}
.entry_v2 > .uros > .uro{margin-bottom:0.4em;padding-left:0.8em;}
.entry_v2 > .uros > .uro:last-child{margin-bottom:0;}
.entry_v2 > .uros > .uro > .uro_line{margin-left:-0.8em;}
.entry_v2 > .uros > .uro > .uro_line > *{vertical-align: middle}
.entry_v2 > .uros > .uro > .uro_line > .ure{display:inline;font-weight:bold;padding:0;margin:0;font-size:inherit;margin-right:0.5em}
.entry_v2 > .uros > .uro > .uro_line > .gram > .gram_internal{color:#009900;}
.entry_v2 > .uros > .uro > .uro_line > .lb{font-style: italic;}
.entry_v2 > .uros > .uro > .uro_line > .sl{font-style: italic;}
.entry_v2 > .uros > .uro > .uro_line > .fl{color:#8f0610;font-style:italic;font-weight: bold;}
.entry_v2 > .uros > .uro > .uro_def{margin:0.5em 0 0 0;}
.entry_v2 > .uros > .uro > .uro_def:first-child{margin-top:0;}
.entry_v2 > .uros > .uro > .uro_def > *:first-child{margin-top:0;}

/*view: inline synonyms*/
.entry_v2 .isyns{}
.entry_v2 .isyns > .bc{font-weight:bold;}
.entry_v2 .isyns > .isyn_link{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 .isyns > .isyn_link sup{font-size:50%;}
.entry_v2 .isyns > .syn_sn{}
/*view: cognate cross entries*/
.entry_v2 > .cxs{margin-top:.5em;margin-bottom:.3em;}
.entry_v2 > .cxs .cx_link{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 > .cxs .cx_link sup{font-size:50%;}
.entry_v2 > .cxs .cl{font-style:italic;}

/*view: directional cross entries*/
.entry_v2 .dxs{color: #8F0610;}
.entry_v2 .dxs.dxs_nl{margin-bottom:.5em;}
.entry_v2 .dxs .dx{color: #8F0610;}
.entry_v2 .dxs .dx .dx_link{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 .dxs .dx .dx_link sup{font-size:50%;}
.entry_v2 .dxs .dx .dx_span{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 .dxs .dx .dx_span sup{font-size:50%;}
.entry_v2 .dxs .dx .dx_sn{}
.entry_v2 .dxs .dx .dx_ab{font-style:italic;}
.entry_v2 .dxs .dx .dx_tag{font-style:italic;}

/*view: cas*/
.entry_v2 .cas{margin-top:6px;}
.entry_v2 .cas > .cas_h{}
.entry_v2 .cas > .ca_prefix{font-style:italic;}
.entry_v2 .cas > .ca_text{font-style:italic;}

/*view: usage paragraphs*/
.entry_v2 .usage_par{padding:0.3em 0.7em;border:1px solid #ccc;margin-bottom:.5em;}
.entry_v2 .usage_par > .usage_par_h{font-weight:bold;}
.entry_v2 .usage_par > .ud_text{text-align:justify;}
.entry_v2 .usage_par > *{margin-bottom:0.3em;}
.entry_v2 .usage_par > *:last-child{margin-bottom:0;}

/*view: synref*/
.entry_v2 .synref_block{}
.entry_v2 .synref_h1{font-weight: bold;}
.entry_v2 .synref_h2{}
.entry_v2 .synref_link{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 .synref_link sup{font-size:50%;}

/*view: usageref*/
.entry_v2 .usageref_block{}
.entry_v2 .usageref_block > .usageref_h1{font-weight: bold;}
.entry_v2 .usageref_block > .usageref_h2{}
.entry_v2 .usageref_block > .usageref_link{font-variant:small-caps;font-size:1.1em;line-height:1;}
.entry_v2 .usageref_block > .usageref_link sup{font-size:50%;}

/***************** 2016/2/6 ******************/

/* 此处修改例句颜色 */
.entry_v2 .vis_w > .vis > .vi > .vi_content {margin-left: .3em; color: #369; /* #3399FF; #0199FF; #3377FF; #398597; #1E90FF;*/}

/* 例句中的短语是否加粗、倾斜 */
.mw_spm_phrase {font-weight: bold; font-style: italic;color: #032952;}
.mw_spm_it {font-weight: bold; font-style: italic; color: #0B5BC4;}

/* 关闭无关内容的显示 */
.save_faves {display: none;}
.vi_more{display: none;}
.jumpcontent{display:none;}

/***************** 2016/2/15 ******************/

/* 分割线 */
.sms {
	padding-top: 12px;
	border-top: 1px dashed #ccc;
	clear: both;
}

/* 要跳转到的主词条 */
.realmainentry {font-weight: bold;}

.xml-hide-o_list{
	display: none;
}
.o_count{
-webkit-touch-callout: none; /* iOS Safari */
-webkit-user-select: none;   /* Chrome/Safari/Opera */
-khtml-user-select: none;    /* Konqueror */
-moz-user-select: none;      /* Firefox */
-ms-user-select: none;       /* IE/Edge */
user-select: none;           /* non-prefixed version, currently not supported by any browser */
}

ul {
display: block;
list-style-type: none;
-webkit-margin-before: 0;
-webkit-margin-after: 0;
-webkit-margin-start: 0;
-webkit-margin-end: 0;
-webkit-padding-start: 0;
}

a.play_pron {
	/*color:#D40218;font-size:167%;margin-left:7px;*/
    padding: 1em;
    background-size: 1.45em;
    background-image: url(C:/Users/14708/PycharmProjects/pythonProject2/sound.png);
    background-repeat: no-repeat;
    background-position: center;
    color: red; /* 设置文本颜色 */
}


.entry.entry_v2.boxy {
}

.usage_par,.sense .usage_par,.synpar {
    position: relative;
    margin:2em 0 1em;
    padding: 1em .7em .7em;
    border: 1px solid #ccc;
    border-radius: .2em;
}
.syn_par_h,
.usage_par_h {
    position: absolute;
    height: 1.4em;
    left: 0em;
    top: -1.6em;
    padding:0 1em;
    border-radius: .7em;
    background: #0b5bc4;
    font-size: 100%;
    line-height: 1.5em;
    color:white;
    font-weight: 700;
}

.usage_par_h .mw_zh, .syn_par_h .mw_zh {
    font-size: 90%;
    color:white;
}

.vi_content .mw_spm_aq .mw_zh {
    font-size: 85%;
    color:black;
    display:inline;
}

.def_text .mw_zh {
	margin-left: .3em;
    font-size: 90%;
    color:darkred;
}

/* 中文例句 */
.vi_content .mw_zh {
    font-size: 90%;
    color:#193031;
    display:block;
}
.vi_content {margin-left: .3em;color: #369;}
.v_label{color: #009900;}
.v_text{font-size:110%; font-weight: bold; color:#032952;}
.sl{font-style:italic; color:#009900;}

/* 图片缩放 */
.entryimg{max-height:5em;border:1px solid #ccc}
.entryimg.is-active{max-height:414px}
img{border:1px solid #ddd;padding-top:0px;max-width:100%;}

.all-entry {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 10px;
    margin-top: 25px;
    position: relative;
}
.custom-checkbox {
    transform: scale(1.5); /* 放大单选框 */
    margin-right: 10px; /* 设置单选框之间的间距 */
}
</style>
</head>
'''
print("开始加载词典")
filename = "韦氏高阶英汉双解词典v3.mdx"
headwords = [*MDX(filename)]  # 单词目录，对象为数组,元素为字节
items = [*MDX(filename).items()]  # 单词和释义
print("词典加载完毕")
# 创建一个tkinter窗口
root = tkinter.Tk()
root.title("Video Player")
root.geometry("800x630")
grid_frame = tk.Frame(root)
grid_frame.pack(side="top", fill="x")
# 创建一个画布，用于显示视频
canvas = tkinter.Canvas(root, bg="black")
canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

# 获取画布的窗口句柄
hwnd = canvas.winfo_id()

word_current_list = []

word_current_list1 = []
words_phrase = set()
words_set = set()


# 加载字幕前，处理字幕单词，变亮
def operate_subtitle():
    global word_current_list, words_phrase, words_set, word_current_list1
    word_current_list = []

    word_current_list1 = []
    words_phrase = set()
    words_set = set()
    if os.path.exists('markWordList.csv'):
        with open("markWordList.csv", "r", newline="", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            # next(csvreader)  # 跳过表头行
            for row in csvreader:
                if len(row) > 2:  # 确保行中有足够的字段
                    abc = row[1].split()
                if len(abc) > 1:
                    words_phrase.add(row[1])
                if len(abc) == 1:
                    words_set.add(row[1])

        if subtitle != "":
            subs = pysrt.open(subtitle)  # 打开srt文件
            for sub in subs:  # 遍历每一条字幕
                text = sub.text  # 获取字幕文本
                words_in_text = text.split()  # 把文本按空格分割成单词列表
                for i, word in enumerate(words_in_text):  # 遍历每一个单词及其索引
                    word_nof = word.rstrip(",.?!")
                    if word_nof in words_set:  # 如果单词在a文件中
                        words_in_text[i] = "<font color=\"#00ff00\">" + word + "</font>"  # 给单词加上<font>标签和颜色代码
                        word_current_list.append(word_nof)  # 添加找到的字幕生词到列表
                sub.text = " ".join(words_in_text)  # 把单词列表重新拼接成文本
                for words_phrase1 in words_phrase:
                    if words_phrase1 in sub.text:
                        d_w = "<font color=\"#ff0000\">" + words_phrase1 + "</font>"  # 给单词加上<font>标签和颜色代码
                        word_current_list1.append(words_phrase1)  # 添加找到的字幕生词到列表
                        sub.text = sub.text.replace(words_phrase1, d_w)

            word_current_list = word_current_list + word_current_list1
            subs.save("templating.srt")  # 保存srt文件
            print("templating.srt创建")
        else:
            print("字幕不存在")
            return None


# 创建一个VLC实例
instance = vlc.Instance()

# 创建一个播放器对象
player = instance.media_player_new()

# 将播放器对象绑定到画布的窗口句柄上
player.set_hwnd(hwnd)

# 进度条创建画布
canvas1 = tk.Canvas(root, width=600, height=50)
canvas1.pack()

# 创建进度条
progress_bar = canvas1.create_rectangle(0, 0, 0, 50, fill="green")

# 创建文本
text = canvas1.create_text(300, 25, text="00:00 / 00:00")


def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"


# 定义一个函数，用来更新进度条和文本
def update_progress_bar(event):
    # 获取鼠标点击或移动的位置
    length = player.get_length()
    x = event.x

    # 限制进度条的长度在0到600之间
    if x < 0:
        x = 0
    elif x > 600:
        x = 600

    # 设置进度条的坐标
    canvas1.coords(progress_bar, 0, 0, x, 50)

    # 计算当前时间（秒）
    current_time = x / 600 * length

    # 更新文本
    canvas1.itemconfig(text, text=f"{format_time(current_time / 1000)} / {format_time(length / 1000)}")

    # 跳转到相应的帧位置
    player.set_time(int(current_time))


def update_progress():
    length = player.get_length()
    if length > 0:
        current_time = player.get_time()
        progress = current_time / length * 600
        canvas1.coords(progress_bar, 0, 0, progress, 50)
        canvas1.itemconfig(text, text=f"{format_time(current_time / 1000)} / {format_time(length / 1000)}")
    root.after(200, update_progress)  # 更新频率可根据实际情况调整


# 绑定鼠标事件
canvas1.bind("<Button-1>", update_progress_bar)
canvas1.bind("<B1-Motion>", update_progress_bar)

label_list = []  # 在函数外部定义一个空列表


# canvas2 = tk.Canvas(canvas, background="yellow")
# canvas2.pack(side='bottom', fill='x')  # 使用横排布局
# label_frame = tk.Frame(canvas)
# label_frame.pack(side='bottom', fill='x')

# place the label on the root window

# 定义一个函数，用来暂停播放器
def show_label():
    global part
    current_time1 = player.get_time()
    # 打开字幕文件
    subs = pysrt.open(subtitle)

    # 提取时间在timestamp处的字幕文本
    part = subs.at({'milliseconds': current_time1})
    # 打印字幕文本
    sentence = part.text
    words = re.split(r'\s+', sentence)

    # loop through the words
    if label_list is not None:
        for label in label_list:
            label.destroy()
    for word in words:
        # create a label for each word
        label = tk.Label(canvas, text=word, foreground='white', background='green')
        # place the label on the root window
        label.pack(side='left', padx=0, pady=5, anchor='sw')
        # label = tk.Label(label_frame, text=word)
        # label.pack(side='left')
        label_list.append(label)


# 定义一个函数，用来开始播放器
def play():
    player.play()


def pause():
    player.pause()
    check_pause_status()


current_time_before = 0


# 根据视频状态调用showlabel函数
def check_pause_status():
    global current_time_before
    root.after(200, check_pause_status)
    if player.is_playing():
        pass
    else:
        current_time_now = player.get_time()
        if current_time_now != current_time_before:
            show_label()
            current_time_before = player.get_time()


update_progress()


def show_border(event):
    # 设置 label 的 relief 属性为 raised，表示凸起的边框
    # 设置事件发生的组件的 relief, borderwidth, padx 和 pady 属性
    event.widget.config(relief="solid", highlightbackground='red', highlightcolor="white")


# 定义一个函数，用于隐藏边框
def hide_border(event):
    # 设置 label 的 relief 属性为 flat，表示无边框
    event.widget.config(relief="flat")


# 定义一个函数，用于复制标签的文本
def copy_text():
    print(copy_word)
    root.clipboard_clear()
    root.clipboard_append(copy_word)


def mark_word(word_definite=None):
    # 去除释义的单选框
    unwanted_text = '''<input type="radio" name="options" value="option3">'''
    new_string = word_definite.replace(unwanted_text, "")
    word_definite = new_string
    sentence = part.text
    table = str.maketrans("", "", ",.!?")
    copy_word1 = copy_word.translate(table)
    # with open("markWordList.txt", "a", encoding="utf-8") as f:
    #     # 创建 CSV writer 对象
    #     f.write(copy_word1 + '\n')
    filename = "markWordList.csv"

    # 读取现有的最大索引（如果文件存在）
    try:
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            max_index = max(int(row[0]) for row in csvreader)
    except FileNotFoundError:
        max_index = 0
    except ValueError:
        print("读取生词表失败，因为文件为空，删除markWordList.csv文件后重试")

    # 写入新的条目，并自动加上索引

    # 写入列表数据
    start_time = part[0].start
    end_time = part[0].end
    start_time = str(start_time)
    end_time = str(end_time)
    start_time = srt_to_seconds(start_time)
    end_time = srt_to_seconds(end_time)
    # 创建一个视频媒体对象，并指定视频文件的路径
    mediaclip = VideoFileClip(video_name)

    # 截取视频中的一段，从第10秒到第20秒
    clip = mediaclip.subclip(start_time, end_time)

    # 保存输出文件，并指定输出文件的路径和名称

    # 获取当前脚本所在的目录
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # 创建子文件夹名称，固定为"media"
    subfolder_name = "media"

    # 构建子文件夹路径
    subfolder_path = os.path.join(script_directory, subfolder_name)

    # 如果子文件夹不存在，则创建它
    if not os.path.exists(subfolder_path):
        os.mkdir(subfolder_path)

    # 获取当前时间并格式化为字符串
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 构建视频文件名，以当前时间命名
    video_filename = f"{current_time}.mp4"

    # 构建输出视频文件的完整路径
    video_filepath = os.path.join(subfolder_path, video_filename)

    # 进行其他操作，如写入视频文件
    clip.write_videofile(video_filepath)

    # clip.write_videofile(f"{copy_word1}.mp4")

    # 复制音频文件到media文件夹
    # 定义原始音频文件路径和目标子文件夹路径
    original_audio_file = audio_path

    target_subfolder = "media\\"

    # 确保目标子文件夹存在
    if not os.path.exists(target_subfolder):
        os.makedirs(target_subfolder)

    # 构建目标音频文件的完整路径
    if audio_path != "":
        target_audio_file = os.path.join(target_subfolder, os.path.basename(original_audio_file))

    # 执行文件复制操作
        shutil.copy(original_audio_file, target_audio_file)

        print(f"音频文件已拷贝到{target_audio_file}")

    new_word = copy_word1
    new_sentence = sentence
    word_definite = word_definite.strip()
    new_index = max_index + 1
    new_audio_path = new_string_old
    video_path = video_filename
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([new_index, new_word, new_sentence, word_definite, new_audio_path, video_path])


# app = None  # 将 QApplication 实例设置为全局变量

new_string = ""
html = ""

app = None


def query_word():
    global html
    global worker
    global thread
    global app  # 在函数内部使用全局变量
    table = str.maketrans("", "", ",.!?")
    copy_word1 = copy_word.translate(table)
    query_word = copy_word1

    wordIndex = headwords.index(query_word.encode())
    word, html = items[wordIndex]
    word, html = word.decode(), html.decode()
    if html.startswith("@"):
        word2 = html.split('=')
        word = word2[1].strip()
        wordIndex = headwords.index(word.encode())
        word, html = items[wordIndex]
        word, html = word.decode(), html.decode()

    print(f"Found match: {word}")
    # open_pyqt_window()
    if app is None:
        app = QApplication(sys.argv)
    window = QueryMainWindow()
    window.show()
    app.exec_()


class QueryMainWindow(QMainWindow):
    def __init__(self):
        global new_string
        global audio_path
        global new_string_old
        super().__init__()
        self.worker = None
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # 设置本地HTML文件的路径
        replacement_block = '<input type="radio" name="options" value="option3"> <div class="sblock_labels">'
        replacement_b = '<input type="radio" name="options" value="option3"> <div class="sense"> <strong class="sn_letter">b&nbsp;</strong>'
        pattern_b = r'<div class="sense"> <strong class="sn_letter">b&nbsp;</strong>'
        pattern_block = r'<div class="sblock_labels">'

        html1 = re.sub(pattern_block, replacement_block, html)
        html2 = re.sub(pattern_b, replacement_b, html1)

        # 给html加div标签，一遍提取释义
        text = html2
        pattern = r'<input type="radio" name="options" value="option3">'
        replacement_list = ['<div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">',
                            '</div><div><input type="radio" name="options" value="option3">']

        def replace_function(match):
            try:
                return replacement_list.pop(0)
            except IndexError:
                # 处理列表为空的情况
                return "单词释义过多，所有不显示 --！"  # 或者你想要的默认替换值

        new_text = re.sub(pattern, replace_function, text)
        new_text = new_text + "</div>"

        pattern = r'(sound://[^"]+\.mp3)'
        match = re.search(pattern, new_text)

        if match:
            file_name = match.group(1)  # 获取捕获的文件名部分
            new_string_old = file_name.replace("sound://", "").replace("/", "")  # 使用捕获的文件名部分创建新字符串
            new_string = "abc/" + new_string_old
            audio_path = new_string
        else:

            print("没有找到单词发音")

        pattern_sound = r'sound://[^"]+\.mp3'
        new_text = re.sub(pattern_sound, new_string, new_text)
        # str_sound = '''class="fa fa-volume-up hpron_icon play_pron"''' + ''' style="background-image: url(
        # 'sound.png');"'''
        # new_text = new_text.replace('''class="fa fa-volume-up hpron_icon play_pron"''',
        #                             str_sound)
        html_file_path = cssfile + new_text
        play_button1 = QPushButton("Play Audio")
        layout.addWidget(play_button1)
        self.media_player = QMediaPlayer(self)
        play_button1.clicked.connect(self.play_local_audio)
        # 加载本地HTML文件
        self.setCentralWidget(central_widget)

        # 响应console返回html字符串
        class WebEnginePage(QWebEnginePage):
            def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
                mark_word(word_definite=message)


        self.web_view.setPage(WebEnginePage(self.web_view))
        self.web_view.setHtml(html_file_path)

    # def get_selected_text(self):
    #     selected_text = self.web_view.page().selectedText()
    #     print("Selected Text:", selected_text)
    #     print("开始查询")
    #
    #     # wordIndex2 = headwords.index(selected_text.encode())
    #     print("找到了第一次搜索单词1")
    #
    #     # word, html = items[wordIndex2]
    #     # word, html = word.decode(), html.decode()
    #     print("找到了第一次搜索单词")
    #
    #     print("higagaaaa")
    #     # self.web_view.setHtml(html_secend)

    def play_local_audio(self):
        local_audio_file = new_string  # Replace with your local audio file path
        media_content = QMediaContent(QUrl.fromLocalFile(local_audio_file))
        self.media_player.setMedia(media_content)
        self.media_player.play()


# def open_pyqt_window():
#     pyqt_thread = threading.Thread(target=run_pyqt_window)
#     pyqt_thread.start()


# 弹出添加单词窗口
def shou_dong():
    # 窗口布局，单词和释义及确定按钮，其他条目自动添加
    child_window = tk.Toplevel(root)

    tk.Label(child_window, text="单词：").pack()
    entry_text = tk.Entry(child_window)
    entry_text.pack()

    tk.Label(child_window, text="释义：").pack()
    text_area = tk.Text(child_window, height=5, width=30)
    text_area.pack()

    def get_inputs():
        input_text = entry_text.get()
        input_text_area = text_area.get("1.0", "end-1c")  # 获取文本域内容

        if input_text.strip() == "" or input_text_area.strip() == "":
            pass
        else:
            input_var = input_text
            input_area_var = input_text_area
            word_definite = new_string
            sentence = part.text
            table = str.maketrans("", "", ",.!?")
            copy_word1 = copy_word.translate(table)
            # with open("markWordList.txt", "a", encoding="utf-8") as f:
            #     # 创建 CSV writer 对象
            #     f.write(copy_word1 + '\n')
            filename = "markWordList.csv"

            # 读取现有的最大索引（如果文件存在）
            try:
                with open(filename, "r", newline="", encoding="utf-8") as csvfile:
                    csvreader = csv.reader(csvfile)
                    max_index = max(int(row[0]) for row in csvreader)
            except FileNotFoundError:
                max_index = 0

            # 写入新的条目，并自动加上索引

            # 写入列表数据
            start_time = part[0].start
            end_time = part[0].end
            start_time = str(start_time)
            end_time = str(end_time)
            start_time = srt_to_seconds(start_time)
            end_time = srt_to_seconds(end_time)
            # 创建一个视频媒体对象，并指定视频文件的路径
            mediaclip = VideoFileClip(video_name)

            # 截取视频中的一段，从第10秒到第20秒
            clip = mediaclip.subclip(start_time, end_time)

            # 保存输出文件，并指定输出文件的路径和名称

            # 获取当前脚本所在的目录
            script_directory = os.path.dirname(os.path.abspath(__file__))

            # 创建子文件夹名称，固定为"media"
            subfolder_name = "media"

            # 构建子文件夹路径
            subfolder_path = os.path.join(script_directory, subfolder_name)

            # 如果子文件夹不存在，则创建它
            if not os.path.exists(subfolder_path):
                os.mkdir(subfolder_path)

            # 获取当前时间并格式化为字符串
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # 构建视频文件名，以当前时间命名
            video_filename = f"{current_time}.mp4"

            # 构建输出视频文件的完整路径
            video_filepath = os.path.join(subfolder_path, video_filename)

            # 进行其他操作，如写入视频文件
            clip.write_videofile(video_filepath)

            # clip.write_videofile(f"{copy_word1}.mp4")

            # 复制音频文件到media文件夹
            # 定义原始音频文件路径和目标子文件夹路径
            # original_audio_file = audio_path
            # target_subfolder = "media\\"
            #
            # # 确保目标子文件夹存在
            # if not os.path.exists(target_subfolder):
            #     os.makedirs(target_subfolder)
            #
            # # 构建目标音频文件的完整路径
            # target_audio_file = os.path.join(target_subfolder, os.path.basename(original_audio_file))
            #
            # # 执行文件复制操作
            # shutil.copy(original_audio_file, target_audio_file)
            #
            # print(f"音频文件已拷贝到{target_audio_file}")

            new_word = input_var
            new_sentence = sentence
            word_definite = input_area_var
            new_index = max_index + 1
            new_audio_path = ""
            video_path = video_filename
            with open(filename, "a", newline="", encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([new_index, new_word, new_sentence, word_definite, new_audio_path, video_path])

            child_window.destroy()

    tk.Button(child_window, text="确定", command=get_inputs).pack()

    # child_window.mainloop()


def show_result():
    if input_var and input_area_var:
        result_label.config(text="文本框内容：" + input_var + "\n文本域框内容：" + input_area_var)


copy_word = ""
menu = tk.Menu(root, tearoff=0)
# 在菜单中添加一个命令项，文本为 "Copy"，命令为 copy_text 函数，并传入 event 参数
menu.add_command(label="复制", command=copy_text)
menu.add_command(label="手动添加", command=shou_dong)
menu.add_command(label="查词", command=query_word)


# 定义一个函数，用于弹出菜单
def popup_menu(event):
    global copy_word
    # 在鼠标右键点击的位置显示菜单
    menu.post(event.x_root, event.y_root)
    copy_word = event.widget.cget("text")


def srt_to_seconds(srt_time):
    # 使用正则表达式匹配时分秒毫秒
    match = re.match(r"(\d+):(\d+):(\d+),(\d+)", srt_time)
    if match:
        # 将匹配到的字符串转换为整数
        hours, minutes, seconds, milliseconds = map(int, match.groups())
        # 计算总的秒数
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        # 返回结果
        return total_seconds
    else:
        # 如果没有匹配到，返回 None
        return None


# 定义一个类，用于显示单词播放


# 定义一个函数，用于弹出新窗口
def pop_window():
    global sidebar
    global listbox
    # 创建新窗口
    new_window = tk.Toplevel()
    new_window.title("新窗口")
    new_window.geometry("%dx%d+%d+%d" % (100, root.winfo_height(), root.winfo_x() + root.winfo_width(), root.winfo_y()))

    # 创建侧边栏
    listbox = tk.Listbox(new_window, height=20, bg="lightgray")
    listbox.pack()

    # 向列表中添加一些内容
    if os.path.exists('markWordList.csv'):
        words_list = []  # 创建一个空集合
        with open("markWordList.csv", "r", newline="", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            # next(csvreader)  # 跳过表头行
            for row in csvreader:
                if len(row) > 2:  # 确保行中有足够的字段
                    index = row[0]
                    word = row[1]
                    sentence_row = row[2]
                    listbox.insert("end", "{}   {}".format(index, word))

    # 创建单词播放窗口
    def creat_small_video(event):
        global app1
        # 获取当前选中的索引
        index = listbox.curselection()
        # 获取当前选中的内容
        content = listbox.get(index)
        split_result = content.split('  ')

        if len(split_result) >= 2:
            index = split_result[0]
            word = split_result[1]

        else:
            print("收藏单词条目过短.")

        # 插入字符串"Hello World"到文本框中
        if os.path.exists('markWordList.csv'):
            with open("markWordList.csv", "r", newline="", encoding="utf-8") as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    if index in row[0]:
                        var = tk.StringVar()
                        var.set(row[2])
                        sssstence = row[2]
                        word_definite = row[3]
                        video_read_path = row[5]

        class CustomMainWindow(QMainWindow):
            def __init__(self, word_definite, word_video):
                super().__init__()
                self.setWindowTitle("PyQt WebEngine and Video Example")
                self.setGeometry(new_window.winfo_x() + new_window.winfo_width(), new_window.winfo_y(), 300, 600)

                central_widget = QWidget(self)
                self.setCentralWidget(central_widget)
                layout = QVBoxLayout(central_widget)

                video_widget = QVideoWidget(self)
                video_widget.setFixedSize(300, 240)  # Video area size
                layout.addWidget(video_widget)

                # Add QLabel to display a sentence with a width of 40
                sentence_label = QLabel(sssstence)
                sentence_label.setFixedSize(277, 50)
                sentence_label.setAlignment(Qt.AlignCenter)
                sentence_label.setWordWrap(True)
                sentence_label.setTextInteractionFlags(
                    Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)  # Allow text selection
                layout.addWidget(sentence_label)

                web_engine_view = QWebEngineView(self)
                layout.addWidget(web_engine_view)

                # Load HTML content
                web_engine_view.setHtml(word_definite + cssfile)

                # Set layout for the central widget
                central_widget.setLayout(layout)
                # Create QMediaPlayer and load local video
                self.media_player = QMediaPlayer()
                self.media_player.setVideoOutput(video_widget)

                # 加载视频
                script_directory = os.path.dirname(os.path.abspath(__file__))
                subfolder_path = os.path.join(script_directory, "media\\" + video_read_path)
                video_path = subfolder_path
                media_content = QMediaContent(QUrl.fromLocalFile(video_path))
                self.media_player.setMedia(media_content)
                self.media_player.play()

                central_widget.setLayout(layout)

        if app1 is None:
            app1 = QApplication(sys.argv)  # 创建 QApplication 实例

        main_window = CustomMainWindow(word_definite, word)
        main_window.show()
        app1.exec_()

    # 显示本集生词表
    def current_list():

        items = listbox.get(0, tkinter.END)
        items_to_delete = []

        for index1, item in enumerate(items):
            num, word1 = item.split('   ')
            if word1 not in word_current_list:
                items_to_delete.append(index1)

        # Delete the items in reverse order to avoid index issues
        for index in reversed(items_to_delete):
            listbox.delete(index)

    def deleted_word():
        index = listbox.curselection()
        # 获取当前选中的内容
        content = listbox.get(index)
        split_result = content.split('  ')
        with open("markWordList.csv", "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
        # 删除指定索引的条目
        sga = int(split_result[0]) - 1
        del rows[int(split_result[0]) - 1]
        for index1, row1 in enumerate(rows[sga:], start=sga):
            rows[index1][0] = str(index1 + 1)  # 更新索引字段，从1开始计数
        with open("markWordList.csv", "w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print("已删除")
        listbox.delete(index)

    # 绑定虚拟事件 <<ListboxSelect>> 到回调函数
    listbox.bind("<Double-Button-1>", creat_small_video)
    button_side = tk.Button(new_window, text="本集相关生词", command=current_list)
    button_side1 = tk.Button(new_window, text="永久删除单词", command=deleted_word)
    button_side.pack()
    button_side1.pack()


def csv_convert():
    if os.path.exists('markWordList.csv'):
        with open("markWordList.csv", "r", newline="", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            with open("anki.csv", "a", newline="", encoding="utf-8") as anki:
                csvwriter = csv.writer(anki)
                for row in csvreader:
                    csvwriter.writerow(
                        [row[0], row[1], row[2], row[3], "[sound:" + row[4] + "]", "[sound:" + row[5] + "]"])

    print("Anki-formatted CSV file has been created: anki.csv")


# 创建按钮
button = tk.Button(root, text="生词列表", command=pop_window)
button.pack(side="right")
button = tk.Button(root, text="导出为anki csv格式文件", command=csv_convert)
button.pack(side="right")
# 给 Label 类绑定鼠标进入事件，回调函数为 show_border
root.bind_class("Label", "<Enter>", show_border)
# 给 Label 类绑定鼠标离开事件，回调函数为 hide_border
root.bind_class("Label", "<Leave>", hide_border)
# 给 Label 类绑定鼠标右键点击事件，回调函数为 popup_menu
root.bind_class("Label", "<Button-3>", popup_menu)


def toggle_play_pause(event):
    if player.get_state() == vlc.State.Playing:
        player.pause()
    elif player.get_state() == vlc.State.Paused:
        player.play()


def seek_forward(event):
    player.set_time(player.get_time() + 5000)  # 前进5秒


def seek_backward(event):
    player.set_time(player.get_time() - 5000)  # 后退5秒


def increase_volume(event):
    current_volume = player.audio_get_volume()
    player.audio_set_volume(min(current_volume + 10, 100))  # 增加音量10%


def decrease_volume(event):
    current_volume = player.audio_get_volume()
    player.audio_set_volume(max(current_volume - 10, 0))  # 减少音量10%


root.bind("<space>", toggle_play_pause)
root.bind("<Right>", seek_forward)
root.bind("<Left>", seek_backward)
root.bind("<Up>", increase_volume)
root.bind("<Down>", decrease_volume)


def browse_and_play():
    global video_name
    global subtitle
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    if file_path:
        subtitle = file_path.replace(".mp4", ".srt")
        operate_subtitle()
        video_name = file_path
        media = instance.media_new(file_path)
        player.set_media(media)
        player.play()
        player.video_set_subtitle_file('templating.srt')

        # 加载中文字幕
        subtitle_file = file_path.replace(".mp4", ".zh.srt")
        try:
            subs = pysrt.open(subtitle_file)

            label = tk.Label(grid_frame, text="", font=("Helvetica", 12))
            label.grid(row=0, column=0)

            # 定义一个函数，用于更新标签显示
            def update_subtitle():
                current_time = player.get_time()

                # 查找当前时间对应的字幕
                current_sub = None
                for sub in subs:
                    if sub.start.ordinal <= current_time <= sub.end.ordinal:
                        current_sub = sub
                        break

                # 更新标签的文本内容
                if current_sub:
                    label.config(text=current_sub.text)

                else:
                    label.config(text="")  # 如果没有字幕，则清空标签内容

                root.after(100, update_subtitle)  # 每隔一段时间更新标签内容

            # 启动标签更新函数
            update_subtitle()
        except:
            print("没有找到.zh.srt格式中文字幕")


def secend_query(query_word):
    print("开始查询")

    wordIndex2 = headwords.index(query_word.encode())
    print("找到了第一次搜索单词1")

    word, html = items[wordIndex2]
    word, html = word.decode(), html.decode()
    print("找到了第一次搜索单词")
    if html.startswith("@"):
        print("String starts with @")
        word2 = html.split('=')
        word = word2[1].strip()
        wordIndex = headwords.index(word.encode())
        word, html = items[wordIndex]
        word, html = word.decode(), html.decode()

    print(f"Found match: {word}")
    print(html)

    # 设置本地HTML文件的路径
    replacement_block = '<input type="radio" name="options" value="option3"> <div class="sblock_labels">'
    replacement_b = '<input type="radio" name="options" value="option3"> <div class="sense"> <strong class="sn_letter">b&nbsp;</strong>'
    pattern_b = r'<div class="sense"> <strong class="sn_letter">b&nbsp;</strong>'
    pattern_block = r'<div class="sblock_labels">'

    html1 = re.sub(pattern_block, replacement_block, html)
    html2 = re.sub(pattern_b, replacement_b, html1)

    # 给html加div标签，一遍提取释义
    text = html2
    pattern = r'<input type="radio" name="options" value="option3">'
    replacement_list = ['<div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">',
                        '</div><div><input type="radio" name="options" value="option3">']

    def replace_function(match):
        return replacement_list.pop(0)

    new_text = re.sub(pattern, replace_function, text)
    new_text = new_text + "</div>"

    pattern = r'(sound://[^"]+\.mp3)'
    match = re.search(pattern, new_text)

    if match:
        file_name = match.group(1)  # 获取捕获的文件名部分
        new_string_old = file_name.replace("sound://", "").replace("/", "")  # 使用捕获的文件名部分创建新字符串
        new_string = "abc/" + new_string_old
        audio_path = new_string
    else:

        print("没有找到单词发音")

    pattern_sound = r'sound://[^"]+\.mp3'
    new_text = re.sub(pattern_sound, new_string, new_text)
    # str_sound = '''class="fa fa-volume-up hpron_icon play_pron"''' + ''' style="background-image: url(
    # 'sound.png');"'''
    # new_text = new_text.replace('''class="fa fa-volume-up hpron_icon play_pron"''',
    #                             str_sound)
    return cssfile + new_text


browse_button = tk.Button(root, text="Browse and Play", command=browse_and_play)
browse_button.pack(side="right")

button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, padx=60)
# 创建一个暂停按钮
pause_button = tk.Button(button_frame, text="Pause", command=pause)
pause_button.pack(side=tk.RIGHT)

# 创建一个开始按钮
play_button = tk.Button(button_frame, text="Play", command=play)
play_button.pack(side=tk.LEFT, padx=10)
# 进入tkinter主循环
root.mainloop()
