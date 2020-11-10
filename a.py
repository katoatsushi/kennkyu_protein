import collections

abc = [
    'フレームレスのスタイリッシュなデザインに加え、高輝度かつ鮮明な画面表示を実現するQHD HDR対応IPS 27インチモニターです',
    'Dell SシリーズS2719DM 27インチHDRフレームレスモニター',
    'この美しいデザインの超薄型モニタは、最薄部5.5 mmのスタイリッシュな形状であらゆる部屋にマッチします',
    'この美しいデザインの超薄型モニタは、最薄部5.5 mmのスタイリッシュな形状であらゆる部屋にマッチします',
    'one two     three',
    'Dell SシリーズS2719DM 27インチHDRフレームレスモニター',
    'この美しいデザインの超薄型モニタは、最薄部5.5 mmのスタイリッシュな形状であらゆる部屋にマッチします'
]

c = collections.Counter(abc)
solo_array = []
for key, value in c.items():
    if value != 1:
        solo_array.extend([key])
for m in solo_array :
    print(m)
