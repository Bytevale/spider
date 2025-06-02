import requests
# 1,准备请求
url = 'https://k0u71y9yaay1dz.djvod.ndcimgs.com/bs2/photo-video-mz/5225583103521127702_7236dcf21e67a098_5005_hd15.mp4?tag=1-1748869236-unknown-0-fwg8cqtn47-84b6257f1e707faf&provider=self&clientCacheKey=3xagtctad7a5zim_c91c9fdc&di=3c0f89fe&bp=14734&x-ks-ptid=162457922975&kcdntag=p:Heilongjiang;i:ChinaUnicom;ft:UNKNOWN;h:COLD;pn:kuaishouVideoProjection&ocid=99&tt=hd15&ss=vp'
# 2，发送请求
response = requests.get(url=url)
# 3,获取的请求内容
result = response.content
# 4,保存为文件
# 4.1，打开文件
with open('vedio/异域风情.mp4','wb') as file:
    # 4.2,写入文件
    file.write(result)







