# 置入模块
import requests
import os
import re
import opencc
import datetime

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

def find_genre(arr,kw_gen,kw_gen2): # 查找频道组索引位置
    pattern_gen = '|'.join(kw_gen)
    pattern_gen2 = '|'.join(kw_gen2)
    for idx, content in enumerate(arr):
        if re.search(pattern_gen,content) and re.search(pattern_gen2,content):
            return idx
        
def find_channel(kw_gen,kw_gen2,kw_ch,dekw_ch): #查找筛选频道
    gi = find_genre(ogenre_content,kw_gen,kw_gen2)
    if gi is None:
        return
    else:
        pattern_ch = '|'.join(kw_ch)
        depattern_ch = '|'.join(dekw_ch)
        with open(input_file,'r',encoding='utf-8') as file, open(txt_ch,'a',encoding='utf-8') as name_ch:
            search_line = 0
            for line in file:
                search_line += 1
                if ogenre_start_line[gi] <= search_line <= ogenre_end_line[gi]:
                    if re.search(pattern_ch, line, re.IGNORECASE) and not re.search(depattern_ch, line, re.IGNORECASE):
                        name_ch.write(line)

def cre_genre():
    with open(txt_ch,'w',encoding='utf-8') as name_ch:
        name_ch.write(f'{name_gen},#genre#\n')
    file_paths.append(txt_ch)
    del_files.append(txt_ch)

# 获取远程直播源文件
# url = "https://raw.githubusercontent.com/Fairy8o/IPTV/main/DIYP-v4.txt"
url = "https://raw.githubusercontent.com/Fairy8o/IPTV/main/PDX-V4.txt"
r = requests.get(url)
# open('DIYP-v4.txt','wb').write(r.content)
open('PDX-V4.txt','wb').write(r.content)

# 直播源文件繁转简
# file_T = 'DIYP-v4.txt'
file_T = 'PDX-V4.txt'
file_S = 'TV.txt'
convert_s2t(file_T,file_S)

input_file = 'TV.txt' # 定义原源
file_paths = [] # 待合并文件列表
del_files = [file_T,file_S] # 待清空文件列表

# 根据原直播源频道分组建立索引
ogenre = genre_index(input_file)
ogenre_content = []
ogenre_start_line = []
ogenre_end_line = []
for line_num,line_content in ogenre:
    ogenre_content.append(line_content)
    ogenre_start_line.append(line_num)
ogenre_end_line = shift_array(ogenre_start_line)
ogenre_start_line = subtract_add(ogenre_start_line)

# 组00：示例组
# name_gen = '展示频道组名'
# name_ch = 'HD'
# txt_ch = 'HD.txt'
# cre_genre()
# find_channel(['高码'], [''], [','], ['👉','卡顿','选择','ipv6','ip-v6'])

# 组01：抓取央视组频道
name_gen = '🇨🇳 央视爸爸'
name_ch = 'CCTV'
txt_ch = 'CCTV.txt'
cre_genre()
kw_gen2 = ''
kw_ch = ['CCTV']
dekw_ch = ['ipv6', 'ip-v6']
find_channel(['独家'], kw_gen2, kw_ch, dekw_ch)
find_channel(['电信'], ['专线'], kw_ch, dekw_ch)

# 组02：抓取卫视组频道，并排除广东相关
name_gen = ' ┣  地方卫视'
name_ch = 'WS'
txt_ch = 'WS.txt'
cre_genre()
kw_gen2 = ''
kw_ch = ['卫视']
dekw_ch = ['广东', '大湾区', 'ipv6', 'ip-v6']
find_channel(['卫视'], kw_gen2, kw_ch, dekw_ch)
find_channel(['独家'], kw_gen2, kw_ch, dekw_ch)
find_channel(['电信'], ['专线'], kw_ch, dekw_ch)

# 组03：抓取卫视、广东组中广东相关频道
name_gen = ' ┣  广东频道'
name_ch = 'GD'
txt_ch = 'GD.txt'
cre_genre()
kw_gen2 = ''
kw_ch = ['广东', '大湾区', '佛山', '广州', '深圳']
dekw_ch = ['ipv6', 'ip-v6']
find_channel(['卫视'], kw_gen2, kw_ch, dekw_ch)
find_channel(['独家'], kw_gen2, kw_ch, dekw_ch)
find_channel(['电信'], ['专线'], kw_ch, dekw_ch)
find_channel(['广东'], kw_gen2, kw_ch, dekw_ch)
find_channel(['地方'], kw_gen2, kw_ch, dekw_ch)

# 组04：抓取香港、澳门组频道
name_gen = ' ┣  港澳地区'
name_ch = 'GA'
txt_ch = 'GA.txt'
cre_genre()
kw_gen2 = ''
find_channel(['香港'], ['路1'], ['TVB','RTHK','VIU','HOY','线','香港','凤凰','J1','J2','明珠','港台'], ['IPV6','ip-v6','魔法'])
find_channel(['香港'], ['路2'], ['TVB','RTHK','VIU','HOY','线','香港','凤凰','J1','J2','明珠','港台'], ['IPV6','ip-v6','魔法'])
find_channel(['澳门'], kw_gen2, ['澳门','澳亚','澳视'], ['IPV6','ip-v6','魔法'])

# 组05：抓取台湾组频道
name_gen = ' ┣  台湾省　'
name_ch = 'TW'
txt_ch = 'TW.txt'
cre_genre()
kw_gen = ['台湾','湾湾']
kw_ch = ['东森','lovenature','探索','八大','中视','三立','台视','TVBS','民视','HBO']
dekw_ch = ['ipv6','ip-v6','魔法','美洲']
find_channel(kw_gen, ['路1'], kw_ch, dekw_ch)
find_channel(kw_gen, ['路2'], kw_ch, dekw_ch)
find_channel(kw_gen, ['路3'], kw_ch, dekw_ch)
# find_channel(kw_gen, ['路4'], kw_ch, dekw_ch)

# 组06：抓取日本组频道
name_gen = '🇯🇵 小日子　'
name_ch = 'JP'
txt_ch = 'JP.txt'
cre_genre()
kw_gen2 = ''
kw_ch = ',' #全抓
find_channel(['小日','日本'], kw_gen2, kw_ch, ['IPV6','ip-v6','魔法','👉','卡顿','选择'])

# 组07：抓取韩国组频道
name_gen = '🇰🇷 大棒子　'
name_ch = 'KR'
txt_ch = 'KR.txt'
cre_genre()
kw_gen2 = ''
kw_ch = ',' #全抓
find_channel(['韩国','泡菜'], kw_gen2, kw_ch, ['IPV6','ip-v6','魔法','👉','卡顿','选择'])

# 读取要合并的文件
file_contents = []
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        file_contents.append(content)

# 备份原文件并生成合并的文件
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M')
backup_file = f'index_{timestamp}.txt'
# 构建完整的备份文件路径
backup_file_path = os.path.join('backup', backup_file)
# 重命名原始文件为备份文件并移动到子目录
os.rename('index.txt', backup_file_path)
#写入合并文件
with open('index.txt', 'w', encoding='utf-8') as output:
    output.write('\n'.join(file_contents))

# 写入更新日期时间（以频道组形式）
    now = datetime.datetime.now()\
        + datetime.timedelta(hours=8) # GMT+8
    output.write(f"\n🕘 更新时间,#genre#\n")
    output.write(f"{now.strftime('%Y-%m-%d')},https://tv.cdesign.io/blank.mp4\n")
    output.write(f"{now.strftime('%H:%M:%S')},https://tv.cdesign.io/blank.mp4\n")
    output.write("CDESIGN.io,https://tv.cdesign.io/blank.mp4\n")

# 清除过程文件
for f in del_files:
    os.remove(f)
