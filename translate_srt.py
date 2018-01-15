# -*- coding: utf-8 -*-
'''
This is a script that translate the English *.srt file
 into Chinese&English *.srt file
Translate by Google!
Before using this script, make sure that you have been install "pyexecjs",
Otherwise, you can use pip install to install.
 pip install pyexecjs
'''
from __future__ import division
import re
import execjs
import urllib.request
import json
import os


class Py4Js:
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;
        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";
        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };
    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


def open_url(url, content):
    postdata = {
        'q': content
    }
    data = urllib.parse.urlencode(postdata).encode(encoding='utf-8')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, data=data, headers=headers)
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')


def translate(subtitle):
    js = Py4Js()
    tk = js.getTk(subtitle)
    content = urllib.parse.quote(subtitle)
    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=1&tk="+tk

    result = open_url(url, subtitle)
    arr=json.loads(result)
    list=[]
    for i in range(len(arr[0])):
        list.append(arr[0][i][0])
    return list

def translate_file(root, name):
    new_srt = os.path.join(root, name)
    backup_srt = os.path.join(root, 'backup'+name)
    os.rename(new_srt, backup_srt)

    f = open(backup_srt)
    fsrt = open(new_srt, "w", encoding='utf-8')
    content = f.read()
    result = re.findall(r'\d+\n(?:\d\d:){2}(?:\d\d),(?:\d){3} --> (?:\d\d:){2}(?:\d\d),(?:\d){3}', content)
    sentence = re.split(r'\d+\n(?:\d\d:){2}(?:\d\d),(?:\d){3} --> (?:\d\d:){2}(?:\d\d),(?:\d){3}', content)
    sentence.pop(0)
    for i in range(len(sentence)):
        sentence[i]=re.sub(r'\n', ' ', sentence[i])
        sentence[i]=sentence[i].strip()

    arr=translate('\n@@@\n'.join(sentence))
    if arr[-1]==None:
        arr=arr[:-1]
    chinese=re.split('@@@\n',''.join(arr))

    for i in range(len(sentence)):
        fsrt.write(result[i] + '\n' + '<font color=#D8D8BF>' + sentence[i] + '\n' + '<font color=#5F9F9F>' + chinese[i] + '\n')
    print("Translate subtitle file '" + new_srt + "' successfully!")


def translate_file_in_path(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            # print(name)
            # os.rename(os.path.join(path, file), os.path.join(path, newname))
            if re.search(r'.*\.srt', name, re.I) is not None:
                translate_file(root, name)


def main():
    # 修改path即可
    # path文件夹及其子文件夹下的所有srt文件将被翻译
    # 并且将原始的srt文件命名为“backup+原始名字.srt”
    path = 'D:\\BaiduYunDownload\\ttt\\'
    translate_file_in_path(path)


if __name__ == "__main__":
    main()

