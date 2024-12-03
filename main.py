import os
import math
import time
import imageio
import aiohttp
import asyncio
import numpy as np
from skimage.color import rgb2gray
from skimage.metrics import structural_similarity as ssim

config = [
    ["第01集", "https://vip.ffzy-play.com/20221102/10846_dbd66ba4/2000k/hls/mixed.m3u8"],
    ["第02集", "https://vip.ffzy-play.com/20221102/10847_a65799b4/2000k/hls/mixed.m3u8"],
    ["第03集", "https://vip.ffzy-play.com/20221102/10850_c0ca8638/2000k/hls/mixed.m3u8"],
    ["第04集", "https://vip.ffzy-play.com/20221102/10851_80225bb5/2000k/hls/mixed.m3u8"],
    ["第05集", "https://vip.ffzy-play.com/20221102/10853_bff1ba04/2000k/hls/mixed.m3u8"],
    ["第06集", "https://vip.ffzy-play.com/20221102/10852_52dccb05/2000k/hls/mixed.m3u8"],
    ["第07集", "https://vip.ffzy-play.com/20221102/10854_36d6b337/2000k/hls/mixed.m3u8"],
    ["第08集", "https://vip.ffzy-play.com/20221102/10855_a0c1a6ad/2000k/hls/mixed.m3u8"],
    ["第09集", "https://vip.ffzy-play.com/20221102/10856_03001b67/2000k/hls/mixed.m3u8"],
    ["第10集", "https://vip.ffzy-play.com/20221102/10857_0c6ea92f/2000k/hls/mixed.m3u8"],
    ["第11集", "https://vip.ffzy-play.com/20221102/10858_1ae6796d/2000k/hls/mixed.m3u8"],
    ["第12集", "https://vip.ffzy-play.com/20221102/10863_631d577a/2000k/hls/mixed.m3u8"],
    ["第13集", "https://vip.ffzy-play.com/20221102/10859_fe22125c/2000k/hls/mixed.m3u8"],
    ["第14集", "https://vip.ffzy-play.com/20221102/10860_42056229/2000k/hls/mixed.m3u8"],
    ["第15集", "https://vip.ffzy-play.com/20221102/10861_137eabab/2000k/hls/mixed.m3u8"],
    ["第16集", "https://vip.ffzy-play.com/20221102/10862_cbe1e31a/2000k/hls/mixed.m3u8"],
    ["第17集", "https://vip.ffzy-play.com/20221102/10864_881e3666/2000k/hls/mixed.m3u8"],
    ["第18集", "https://vip.ffzy-play.com/20221102/10866_fef126b6/2000k/hls/mixed.m3u8"],
    ["第19集", "https://vip.ffzy-play.com/20221102/10870_9bb9fd07/2000k/hls/mixed.m3u8"],
    ["第20集", "https://vip.ffzy-play.com/20221102/10865_49b2ba30/2000k/hls/mixed.m3u8"],
    ["第21集", "https://vip.ffzy-play.com/20221102/10867_64942cba/2000k/hls/mixed.m3u8"],
    ["第22集", "https://vip.ffzy-play.com/20221102/10869_c489e993/2000k/hls/mixed.m3u8"],
    ["第23集", "https://vip.ffzy-play.com/20221102/10868_a1daa00e/2000k/hls/mixed.m3u8"],
    ["第24集", "https://vip.ffzy-play.com/20221102/10874_f16c38ff/2000k/hls/mixed.m3u8"],
    ["第25集", "https://vip.ffzy-play.com/20221102/10873_8d2a1172/2000k/hls/mixed.m3u8"],
    ["第26集", "https://vip.ffzy-play.com/20221102/10872_3c47e330/2000k/hls/mixed.m3u8"],
    ["第27集", "https://vip.ffzy-play.com/20221102/10871_66471687/2000k/hls/mixed.m3u8"],
    ["第28集", "https://vip.ffzy-play.com/20221102/10875_48b5788c/2000k/hls/mixed.m3u8"],
    ["第29集", "https://vip.ffzy-play.com/20221102/10877_1af6cb93/2000k/hls/mixed.m3u8"],
    ["第30集", "https://vip.ffzy-play.com/20221102/10876_add4f66c/2000k/hls/mixed.m3u8"],
    ["第31集", "https://vip.ffzy-play.com/20221102/10879_4ac754db/2000k/hls/mixed.m3u8"],
    ["第32集", "https://vip.ffzy-play.com/20221102/10880_de4caaca/2000k/hls/mixed.m3u8"],
    ["第33集", "https://vip.ffzy-play.com/20221102/10881_fa408994/2000k/hls/mixed.m3u8"],
    ["第34集", "https://vip.ffzy-play.com/20221102/10878_86563727/2000k/hls/mixed.m3u8"],
    ["第35集", "https://vip.ffzy-play.com/20221102/10883_a987536a/2000k/hls/mixed.m3u8"],
    ["第36集", "https://vip.ffzy-play.com/20221102/10882_a49645bf/2000k/hls/mixed.m3u8"],
    ["第37集", "https://vip.ffzy-play.com/20221102/10884_1fd24d51/2000k/hls/mixed.m3u8"],
    ["第38集", "https://vip.ffzy-play.com/20221102/10885_b551f52d/2000k/hls/mixed.m3u8"],
    ["第39集", "https://vip.ffzy-play.com/20221102/10887_ed67ece5/2000k/hls/mixed.m3u8"],
    ["第40集", "https://vip.ffzy-play.com/20221102/10886_53a1e526/2000k/hls/mixed.m3u8"],
    ["第41集", "https://vip.ffzy-play.com/20221102/10890_46e89450/2000k/hls/mixed.m3u8"],
    ["第42集", "https://vip.ffzy-play.com/20221102/10888_5942a0ec/2000k/hls/mixed.m3u8"],
    ["第43集", "https://vip.ffzy-play.com/20221102/10889_a197ea98/2000k/hls/mixed.m3u8"],
    ["第44集", "https://vip.ffzy-play.com/20221102/10892_01632a89/2000k/hls/mixed.m3u8"],
    ["第45集", "https://vip.ffzy-play.com/20221102/10891_08023ac7/2000k/hls/mixed.m3u8"],
    ["第46集", "https://vip.ffzy-play.com/20221102/10893_319e865f/2000k/hls/mixed.m3u8"],
    ["第47集", "https://vip.ffzy-play.com/20221102/10894_be49adec/2000k/hls/mixed.m3u8"],
    ["第48集", "https://vip.ffzy-play.com/20221102/10895_ccc855cd/2000k/hls/mixed.m3u8"],
    ["第49集", "https://vip.ffzy-play.com/20221102/10896_af2c7a8d/2000k/hls/mixed.m3u8"],
    ["第50集", "https://vip.ffzy-play.com/20221102/10898_fd93b6f2/2000k/hls/mixed.m3u8"],
    ["第51集", "https://vip.ffzy-play.com/20221102/10899_f71745c9/2000k/hls/mixed.m3u8"],
    ["第52集", "https://vip.ffzy-play.com/20221102/10900_e07b2cca/2000k/hls/mixed.m3u8"],
    ["第53集", "https://vip.ffzy-play.com/20221102/10897_a595ec97/2000k/hls/mixed.m3u8"],
    ["第54集", "https://vip.ffzy-play.com/20221102/10901_340e3d7b/2000k/hls/mixed.m3u8"],
    ["第55集", "https://vip.ffzy-play.com/20221102/10902_d642842a/2000k/hls/mixed.m3u8"],
    ["第56集", "https://vip.ffzy-play.com/20221102/10903_7983103f/2000k/hls/mixed.m3u8"],
    ["第57集", "https://vip.ffzy-play.com/20221102/10905_c8000a4b/2000k/hls/mixed.m3u8"],
    ["第58集", "https://vip.ffzy-play.com/20221102/10907_5ea8f1ad/2000k/hls/mixed.m3u8"],
    ["第59集", "https://vip.ffzy-play.com/20221102/10904_38dea0e1/2000k/hls/mixed.m3u8"],
    ["第60集", "https://vip.ffzy-play.com/20221102/10906_47d167ae/2000k/hls/mixed.m3u8"],
    ["第61集", "https://vip.ffzy-play.com/20221102/10908_ba1c5f16/2000k/hls/mixed.m3u8"],
    ["第62集", "https://vip.ffzy-play.com/20221102/10910_0b422429/2000k/hls/mixed.m3u8"],
    ["第63集", "https://vip.ffzy-play.com/20221102/10909_153eef30/2000k/hls/mixed.m3u8"],
    ["第64集", "https://vip.ffzy-play.com/20221102/10911_76186b65/2000k/hls/mixed.m3u8"],
    ["第65集", "https://vip.ffzy-play.com/20221102/10913_e3999a13/2000k/hls/mixed.m3u8"],
    ["第66集", "https://vip.ffzy-play.com/20221102/10914_03a19a92/2000k/hls/mixed.m3u8"],
    ["第67集", "https://vip.ffzy-play.com/20221102/10912_d96f7979/2000k/hls/mixed.m3u8"],
    ["第68集", "https://vip.ffzy-play.com/20221102/10916_91af03fb/2000k/hls/mixed.m3u8"],
    ["第69集", "https://vip.ffzy-play.com/20221102/10917_3e955d4a/2000k/hls/mixed.m3u8"],
    ["第70集", "https://vip.ffzy-play.com/20221102/10915_b5c3671e/2000k/hls/mixed.m3u8"],
    ["第71集", "https://vip.ffzy-play.com/20221102/10918_3057d854/2000k/hls/mixed.m3u8"],
    ["第72集", "https://vip.ffzy-play.com/20221102/10919_3551824d/2000k/hls/mixed.m3u8"],
    ["第73集", "https://vip.ffzy-play.com/20221102/10922_f6a624c5/2000k/hls/mixed.m3u8"],
    ["第74集", "https://vip.ffzy-play.com/20221102/10920_2d223570/2000k/hls/mixed.m3u8"],
    ["第75集", "https://vip.ffzy-play.com/20221102/10921_fb1f353b/2000k/hls/mixed.m3u8"],
    ["第76集", "https://vip.ffzy-play.com/20221102/10923_ebc5386c/2000k/hls/mixed.m3u8"],
    ["第77集", "https://vip.ffzy-play.com/20221102/10925_60819b76/2000k/hls/mixed.m3u8"],
    ["第78集", "https://vip.ffzy-play.com/20221102/10924_ccdc229d/2000k/hls/mixed.m3u8"]
]


class Processbar:
    def __init__(self, length: int = 50, c1: str = "=", c2: str = ">", c3: str = " "):
        self._each = 100 / length
        self._size, self._c1, self._c2, self._c3 = length, c1, c2, c3
        self._real, self._ads = 0, 0
        self.episode, self.steps, self._cur = "", 0, 0

    def reset(self):
        self._real, self._ads, self._cur = 0, 0, 0

    def next(self, is_real: bool):
        if is_real:
            self._real += 1
        else:
            self._ads += 1
        self._cur += 1
        if self._cur >= self.steps:
            self._cur = self.steps

        percent = self._cur * 100 / self.steps
        done, ing = math.floor(percent / self._each), percent % self._each
        c2, right = "", self._size - done
        if ing:
            c2, right = self._c2, right - 1
        print(
            f"\r{self.episode}: [{self._c1 * done}{c2}{self._c3 * (self._size - 1 - done)}] "
            f"{percent:5.2f}%, 正片：{self._real:-4d}, 广告：{self._ads:-2d}",
            end=""
        )

    def flush(self):
        self.reset()
        print("\n")


class BaseFilter:
    def __call__(self, content: bytes, process: Processbar) -> bytes:
        process.next(True)
        return content


class SimilarityFilter(BaseFilter):
    def __init__(self, rate: float = 0.95):
        self._rate = rate
        self._ads: list[np.ndarray] = []
        for i in range(5):
            img = imageio.v2.imread(f"ads/{i}.png")
            self._ads.append(rgb2gray(img))

    def __call__(self, content: bytes, process: Processbar) -> bytes:
        try:
            video = imageio.get_reader(content, format="mp4")  # noqa
            first_frame = rgb2gray(video.get_data(0))
            video.close()

            for i in range(5):
                score, _ = ssim(first_frame, self._ads[i], full=True, data_range=255)
                if score > self._rate:
                    process.next(False)
                    return b""
            process.next(True)
            return content
        except Exception as e:
            print(f"\t[ERROR] 读取视频流失败：{e}")
            return b""


class ResolutionFilter(BaseFilter):
    def __init__(self, width: int = 1920, height: int = 1080):
        self._width = width
        self._height = height

    def __call__(self, content: bytes, process: Processbar) -> bytes:
        try:
            video = imageio.get_reader(content, format="mp4")  # noqa
            meta = video.get_meta_data()
            video.close()

            if "size" in meta:
                width, height = meta["size"]
                if width != self._width or height != self._height:
                    process.next(True)
                    return content
                process.next(False)
                return b""
            else:
                print("\t[ERROR] 元信息读取失败")
                return b""

        except Exception as e:
            print(f"\t[ERROR] 读取视频流失败：{e}")
            return b""


class M3U8Downloader:
    def __init__(self, process: Processbar, action: callable = None):
        self._process = process
        self._action = action or BaseFilter()

    def download(self, ep_name: str, m3u8_url: str, base: str = None):
        """
        下载某个m3u8视频文件
        :param ep_name: 打印以及存储名称
        :param m3u8_url: m3u8视频文件地址
        :param base: ts前缀路径与m3u8前缀路径不同时，使用`base`指定ts前缀路径
        :return: 视频下载完成后，存放于 `eps/<ep_name.ts>` 中
        """
        self._process.episode = ep_name
        base = base or m3u8_url.rsplit("/", 1)[0]
        res = asyncio.run(self._run(m3u8_url, base))
        with open(f"eps/{ep_name}.ts", "wb") as fp:
            ads, real = 0, 0
            for chunk in res:
                if chunk:
                    real += 1
                    fp.write(chunk)
                else:
                    ads += 1
        self._process.flush()

    async def _run(self, m3u8_url: str, base: str):
        connector = aiohttp.TCPConnector(ssl=False)
        session = aiohttp.ClientSession(connector=connector)
        ts_list = await self._parse_tss(session, m3u8_url)
        self._process.steps = len(ts_list)
        tasks = []
        for name in ts_list:
            task = asyncio.ensure_future(self._download_ts(session, f"{base}/{name}"))
            tasks.append(task)
        result = await asyncio.gather(*tasks)
        await session.close()
        return result

    @staticmethod
    def _to_mp4(ts_file: str, mp4_file: str):
        os.system(f"ffmpeg -i {ts_file} -c copy {mp4_file}")

    @staticmethod
    async def _parse_tss(session: aiohttp.ClientSession, m3u8_url: str) -> list[str]:
        resp = await session.get(m3u8_url)
        if resp.status != 200:
            raise RuntimeError(f"\t[ERROR] 获取m3u8文件失败: {resp.status}, URL: {m3u8_url}")
        m3u8_text = await resp.text()
        m3u8_list = m3u8_text.split("\n")
        return [i for i in m3u8_list if i and i[0] != "#"]

    async def _download_ts(self, session: aiohttp.ClientSession, ts_url: str) -> bytes:
        resp = await session.get(ts_url)
        if resp.status != 200:
            raise RuntimeError(f"\t[ERROR] 获取ts文件失败: {resp.status}, URL: {ts_url}")
        content = await resp.content.read()
        return self._action(content, self._process)


def main():
    downloader = M3U8Downloader(Processbar(), ResolutionFilter())
    for i in range(41, 78):
        downloader.download(config[i][0], config[i][1])
        time.sleep(1)


if __name__ == "__main__":
    main()
