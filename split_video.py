#!/usr/bin/env python
import json
import re
from pathlib import PurePath, Path
from typing import Optional, AnyStr, List, Dict, Union
from datetime import timedelta
from subprocess import Popen, PIPE
from argparse import ArgumentParser
from hashlib import sha256

from dataclasses import dataclass, field

import toml
from dataclasses_json import dataclass_json, config, LetterCase
from tabulate import tabulate


class TimeDeltaHelper:
    timedelta_regex: re.Pattern = re.compile(
        r'^(?:(?P<hour>\d+):)?(?P<minute>\d+):(?P<second>\d+)(?:\.(?P<ms>\d+))?$')

    @staticmethod
    def from_str(delta_str=AnyStr) -> Optional[timedelta]:
        """
        解析
        :param delta_str:
        :return:
        """
        if not delta_str:
            return None

        match = TimeDeltaHelper.timedelta_regex.match(delta_str)
        if not match:
            raise Exception('input format error')
        group_dict = match.groupdict()
        return timedelta(
            hours=int(group_dict.get('hour')) if group_dict.get('hour') else 0,
            minutes=int(group_dict.get('minute')),
            seconds=int(group_dict.get('second')),
            milliseconds=int(group_dict.get('ms')) if group_dict.get('ms') else 0,
        )

    @staticmethod
    def to_str(td: timedelta) -> AnyStr:
        return td.__str__() if td else None

    @staticmethod
    def dataclass_json_config() -> Dict[str, dict]:
        return config(decoder=TimeDeltaHelper.from_str, encoder=TimeDeltaHelper.to_str)


@dataclass
class VideoInfo:
    filename: str
    duration: timedelta


@dataclass
class VideoPart:
    name: str
    start: timedelta
    end: timedelta


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PartSpec:
    name: str
    start: Optional[timedelta] = field(default=None, metadata=TimeDeltaHelper.dataclass_json_config())
    start_idx: Optional[int] = None
    end: Optional[timedelta] = field(default=None, metadata=TimeDeltaHelper.dataclass_json_config())
    end_idx: Optional[int] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ProjectSpec:
    workdir: PurePath = field(metadata=config(decoder=PurePath))
    files: List[str] = None
    parts: List[PartSpec] = None
    ffmpeg_args: Dict[str, Optional[str]] = field(default_factory=lambda: {'c': 'copy'})

    def split(self,
              videos: List[VideoInfo],
              max_part_length: Optional[timedelta] = None,
              latest_part_greedy: Optional[float] = None) -> List[VideoPart]:
        """
        file1: 21:30
        file2: 15:00
        file3: 45:00
        durations [21:30, 36:30, 01:20:30]
        """
        durations: List[timedelta] = []
        for video_info in videos:
            if not durations:
                durations.append(video_info.duration)
            else:
                durations.append(durations[-1] + video_info.duration)

        res: List[VideoPart] = []
        for idx, part in enumerate(self.parts):
            if not part.start:
                if idx == 0:
                    st = timedelta()
                else:
                    st = res[-1].end
            elif not part.start_idx or part.start == 1:
                st = part.start
            else:
                st = durations[part.start_idx - 2] + part.start

            if not part.end:
                if idx == len(self.parts) - 1:
                    et = durations[-1]
                else:
                    raise RuntimeError('未指定结束时间')
            elif not part.end_idx or part.end_idx == 1:
                et = part.end
            else:
                et = durations[part.end_idx - 2] + part.end

            current_part_duration = et - st
            assert current_part_duration.total_seconds() > 0
            if not max_part_length or current_part_duration < max_part_length * (
                    1 + latest_part_greedy if latest_part_greedy else 0):
                res.append(VideoPart(name=part.name, start=st, end=et))
                continue

            part_num = int(current_part_duration / max_part_length)
            if not latest_part_greedy or current_part_duration % max_part_length > (
                    current_part_duration * latest_part_greedy):
                part_num += 1

            last_et: Optional[timedelta] = None
            for i in range(part_num):
                name = f'{part.name}_part{i + 1}'
                if i == 0:
                    last_et = st + max_part_length
                    res.append(VideoPart(name=name, start=st, end=last_et))
                elif i == part_num - 1:
                    res.append(VideoPart(name=name, start=last_et - timedelta(seconds=5), end=et))
                else:
                    res.append(VideoPart(name=name, start=last_et - timedelta(seconds=5),
                                         end=last_et + max_part_length))
                    last_et += max_part_length
        return res


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Config:
    ffmpeg_bin: str = 'ffmpeg'
    ffprobe_bin: str = 'ffprobe'
    max_part_length: Optional[timedelta] = field(default=None, metadata=TimeDeltaHelper.dataclass_json_config())
    latest_part_greedy: Optional[float] = None
    re_mux_at_first: bool = False
    projects: List[ProjectSpec] = None


class FFMpeg:
    @staticmethod
    def get_video_duration(file: Union[PurePath, str], ffprobe_bin: str = 'ffprobe') -> timedelta:
        child = Popen(
            [ffprobe_bin,
             '-loglevel', '-8',
             '-print_format', 'json',
             '-show_format',
             str(file)],
            stderr=PIPE, stdout=PIPE)
        out, _ = child.communicate()
        return timedelta(seconds=float(json.loads(out)['format']['duration']))

    @staticmethod
    def get_concat_file(files: List[str]) -> bytes:
        b = b''
        for f in files:
            b += f'file \'file:{f}\'\n'.encode()
        return b

    @staticmethod
    def encode(input_file: Union[List[str], str], output_file: str, ffmpeg_bin: str = 'ffmpeg', **kwargs):
        cmd = [ffmpeg_bin, '-y', '-hide_banner']
        if isinstance(input_file, List) and len(input_file) > 1:
            cmd.extend([
                '-protocol_whitelist', 'file,pipe',
                '-auto_convert', '1',
                '-f', 'concat',
                '-safe', '0',
                '-i', '-'])
        else:
            cmd.extend(['-i', input_file if not isinstance(input_file, List) else input_file[0]])

        for k, v in kwargs.items():
            cmd.append('-' + k.replace('-', '_'))
            if v:
                cmd.append(v)
        cmd.append(output_file)
        child = Popen(cmd, stdin=PIPE)
        child.communicate(
            FFMpeg.get_concat_file(input_file) if isinstance(input_file, List) and len(input_file) > 1 else None)


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--dry-run', action='store_true', help='仅展示结果，不执行')
    parser.add_argument('file', type=open, help='输入文件')
    args = parser.parse_args()

    cfg: Config = Config.from_dict(toml.load(args.file))
    for project in cfg.projects:
        videos: List[VideoInfo] = [VideoInfo(file, FFMpeg.get_video_duration(project.workdir / file, cfg.ffprobe_bin))
                                   for file in project.files]
        input_file: Union[List[str], str] = [str(project.workdir / file) for file in project.files]
        if not args.dry_run and cfg.re_mux_at_first:
            content = '\n'.join([str(project.workdir / v.filename) for v in videos])
            h = sha256()
            h.update(content.encode())
            re_mux_file = f'{h.hexdigest()}.mp4'

            if not Path(project.workdir / re_mux_file).is_file():
                FFMpeg.encode(
                    input_file=[str(project.workdir / file) for file in project.files],
                    output_file=str(project.workdir / re_mux_file),
                    ffmpeg_bin=cfg.ffmpeg_bin,
                    c='copy'
                )
            videos = [VideoInfo(re_mux_file, FFMpeg.get_video_duration(project.workdir / re_mux_file, cfg.ffprobe_bin))]
            input_file = str(project.workdir / re_mux_file)

        video_parts: List[VideoPart] = project.split(videos, max_part_length=cfg.max_part_length,
                                                     latest_part_greedy=cfg.latest_part_greedy)
        print(tabulate([[vp.name, vp.start, vp.end, vp.end - vp.start] for vp in video_parts],
                       ('文件名', '开始时间', '结束时间', '时长')))
        if args.dry_run:
            continue
        for vp in video_parts:
            FFMpeg.encode(
                input_file=input_file,
                output_file=str(project.workdir / (vp.name + '.mp4')),
                ffmpeg_bin=cfg.ffmpeg_bin,
                ss=str(vp.start),
                to=str(vp.end),
                **project.ffmpeg_args
            )


if __name__ == '__main__':
    main()
