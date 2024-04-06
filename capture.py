# 置入模块
import requests
import os
import re
import opencc
import datetime

# 获取远程直播源文件
url = "https://raw.githubusercontent.com/Fairy8o/IPTV/main/DIYP-v4.txt"
r = requests.get(url)
open('DIYP-v4.txt','wb').write(r.content)

def convert_s2t(file_T,file_S): # 繁转简
    converter = opencc.OpenCC('t2s')
    with open(file_T,'r',encoding='utf-8') as f:
        t_text = f.read()
        s_text = converter.convert(t_text)
    with open(file_S,'w',encoding='utf-8') as f:
        f.write(s_text)

def genre_index(input_file): # 以'#genre#'为关键词，建立频道分组索引
    genre_lines=[]
    with open(input_file,'r',encoding='utf-8') as f:
        for idx,line in enumerate(f,start=1):
            if "#genre#" in line:
                genre_lines.append((idx,line.strip()))
    return genre_lines

def count_lines(input_file): # 文件行数，确定最后一个频道位置
    with open(input_file,'r',encoding='utf-8') as f:
        return sum(1 for line in f)

def shift_array(arr): # 数组向左平移并减一行，得到频道组结束行位置数组
    shift_arr = arr[1:]+[count_lines(input_file)+1]
    return [x - 1 for x in shift_arr]

def subtract_add(arr): # 数组内容加1，得到频道组第一个频道位置
    return [x + 1 for x in arr]

def find_genre(arr,kw_gen): # 查找频道组索引位置
    pattern_gen = '|'.join(kw_gen)
    for idx, content in enumerate(arr):
        if re.search(pattern_gen,content):
            return idx

file_T = 'DIYP-v4.txt'
file_S = 'TV.txt'
convert_s2t(file_T,file_S)

input_file = 'TV.txt'

ogenre = genre_index(input_file)
ogenre_content = []
ogenre_start_line = []
ogenre_end_line = []
for line_num,line_content in ogenre:
    ogenre_content.append(line_content)
    ogenre_start_line.append(line_num)

ogenre_end_line = shift_array(ogenre_start_line)
ogenre_start_line = subtract_add(ogenre_start_line)

gi = find_genre(ogenre_content,['高码'])
keywords = ['']
dekeywords = ['👉','卡顿','选择','IPV6','ip-v6']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('HD.txt','w',encoding='utf=8') as HD:
    HD.write('\n🚀 高清專區,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line) and not re.search(depattern,line):
                HD.write(line)

gi = find_genre(ogenre_content,['央视'])
keywords = ['CCTV']
dekeywords = ['IPV6','ip-v6']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('YS.txt','w',encoding='utf=8') as YS:
    YS.write('\n🇨🇳 央視爸爸,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line, re.IGNORECASE) and not re.search(depattern,line, re.IGNORECASE):
                YS.write(line)

gi = find_genre(ogenre_content,['卫视'])
keywords = ['卫视']
dekeywords = ['广东','大湾区']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('WS.txt','w',encoding='utf=8') as WS:
    WS.write('\n ┣  地方衛視,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line) and not re.search(depattern,line):
                WS.write(line)

# 搜索广东频道
# 从卫视频道组筛选广东相关频道
gi = find_genre(ogenre_content,['卫视'])
keywords = ['广东','大湾区']
dekeywords = ['IPV6','ip-v6']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('GD.txt','w',encoding='utf=8') as GD:
    GD.write('\n ┣  廣東制霸,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line) and not re.search(depattern,line, re.IGNORECASE):
                GD.write(line)
# 从广东频道组筛选广东相关频道，追加录入
gi = find_genre(ogenre_content,['广东'])
keywords = ['广东','佛山']
dekeywords = ['IPV6','ip-v6']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('GD.txt','a',encoding='utf=8') as GD:
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line) and not re.search(depattern,line, re.IGNORECASE):
                GD.write(line)

# 搜索香港、澳门频道组，筛选抓取频道
# 筛选香港频道
gi = find_genre(ogenre_content,['香港'])
keywords = ['TVB','RTHK','VIU','HOY','线','香港','凤凰','J1','J2','明珠','港台']
dekeywords = ['IPV6','ip-v6','魔法']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('HA.txt','w',encoding='utf=8') as HA:
    HA.write('\n ┣  港澳地区,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line, re.IGNORECASE) and not re.search(depattern,line, re.IGNORECASE):
                HA.write(line)
# 筛选澳门频道，追加
gi = find_genre(ogenre_content,['澳门'])
keywords = ['澳门','澳亚','澳视']
dekeywords = ['IPV6','ip-v6','魔法']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('HA.txt','a',encoding='utf=8') as HA:
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line, re.IGNORECASE) and not re.search(depattern,line, re.IGNORECASE):
                HA.write(line)

# 搜索台湾频道组，筛选抓取频道
gi = find_genre(ogenre_content,['台湾','湾'])
# 优先筛选加入
keywords = ['东森','NATURE','探索']
dekeywords = ['IPV6','ip-v6','魔法','美洲']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('TW.txt','w',encoding='utf=8') as TW:
    TW.write('\n ┣  台灣省　,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line, re.IGNORECASE) and not re.search(depattern,line, re.IGNORECASE):
                TW.write(line)
# 追加筛选加入（排序靠后）
keywords = ['八大','中视','三立','台视','TVBS','民视']
dekeywords = ['IPV6','ip-v6','魔法']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('TW.txt','a',encoding='utf=8') as TW:
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line, re.IGNORECASE) and not re.search(depattern,line, re.IGNORECASE):
                TW.write(line)

# 搜索日本频道组，筛选抓取频道
gi = find_genre(ogenre_content,['小日','日本'])
# 筛选加入
keywords = ['']
dekeywords = ['IPV6','ip-v6','魔法','👉','卡顿','选择']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('JP.txt','w',encoding='utf=8') as JP:
    JP.write('\n🇯🇵 小日子　,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line, re.IGNORECASE) and not re.search(depattern,line, re.IGNORECASE):
                JP.write(line)

# 搜索韩国频道组，筛选抓取频道
gi = find_genre(ogenre_content,['韩国','泡菜'])
# 筛选加入
keywords = ['']
dekeywords = ['IPV6','ip-v6','魔法','👉','卡顿','选择']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('KR.txt','w',encoding='utf=8') as KR:
    KR.write('\n🇰🇷 大棒子　,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line, re.IGNORECASE) and not re.search(depattern,line, re.IGNORECASE):
                KR.write(line)

# 搜索HBO频道
# 从国际频道组筛选相关频道
gi = find_genre(ogenre_content,['国际'])
keywords = ['HBO']
dekeywords = ['IPV6','ip-v6','魔法']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('IN.txt','w',encoding='utf=8') as IN:
    IN.write('\n🌏 HBO  　,#genre#\n')
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line) and not re.search(depattern,line, re.IGNORECASE):
                IN.write(line)
# 从HBO组筛选相关频道，追加录入
gi = find_genre(ogenre_content,['HBO'])
keywords = ['HBO']
dekeywords = ['IPV6','ip-v6','魔法']
pattern = '|'.join(keywords)
depattern = '|'.join(dekeywords)
with open(input_file,'r',encoding='utf-8') as file, open('IN.txt','a',encoding='utf=8') as IN:
    search_line = 0
    for line in file:
        search_line += 1
        if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
            if re.search(pattern, line) and not re.search(depattern,line, re.IGNORECASE):
                IN.write(line)

# 读取要合并的文件
file_contents = []
file_paths = ['HD.txt','YS.txt','WS.txt','GD.txt','HA.txt','TW.txt','JP.txt','KR.txt','IN.txt']
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        file_contents.append(content)

# 生成合并的文件
with open('index.txt', 'w', encoding='utf-8') as output:
    output.write('\n'.join(file_contents))
# 写入更新日期时间
    now = datetime.datetime.now()\
        + datetime.timedelta(hours=8) #GMT+8
    output.write(f"\n更新时间,#genre#\n")
    output.write(f"{now.strftime('%Y-%m-%d')},https://tv.cdesign.io/blank.mp4\n")
    output.write(f"{now.strftime('%H:%M:%S')},https://tv.cdesign.io/blank.mp4\n")
    output.write("CDESIGN.io,https://tv.cdesign.io/blank.mp4\n")

os.remove('DIYP-v4.txt') # 删除获取源原文件
os.remove('TV.txt') # 删除源T2S文件
os.remove('HD.txt')
os.remove('YS.txt')
os.remove('WS.txt')
os.remove('GD.txt')
os.remove('HA.txt')
os.remove('TW.txt')
os.remove('JP.txt')
os.remove('KR.txt')
os.remove('IN.txt')
