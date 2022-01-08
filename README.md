# split-video 视频快速分P工具

## 依赖

```text
ffmpeg
ffprobe
```

## 安装

```shell
git clone https://github.com/hr3lxphr6j/split-video.git
cd split-video
pip install -r requirements.txt
```

## 使用例子

```shell
python3 split_video.py input.toml
```

```toml
# input.toml
maxPartLength = "01:00:00"
latestPartGreedy = 0.1

[[projects]]
workdir = "./"
files = [
    "[2022-01-05 13-56-41][周逸逸哦啦啦][先跑图~晚上抽卡]_1.mp4", # 该视频总时长：03:00:00
    "[2022-01-05 13-56-41][周逸逸哦啦啦][先跑图~晚上抽卡]_2.mp4", # 该视频总时长：03:00:00
    "[2022-01-05 13-56-41][周逸逸哦啦啦][先跑图~晚上抽卡]_3.mp4"  # 该视频总时长：01:35:51
]
[[projects.parts]]
name = "原神"
end = "04:50:00" # 第一部分到 4小时50分钟 结束

[[projects.parts]]
name = "LOL大乱斗+下棋" # 这一部分以上一部分的结尾作为开始（4小时50分钟），到最终视频末为结束
```

### 结果

```text
文件名                开始时间    结束时间        时长
--------------------  ----------  --------------  --------------
原神_part1            0:00:00     1:00:00         1:00:00
原神_part2            0:59:55     2:00:00         1:00:05
原神_part3            1:59:55     3:00:00         1:00:05
原神_part4            2:59:55     4:00:00         1:00:05
原神_part5            3:59:55     4:50:00         0:50:05
LOL大乱斗+下棋_part1  4:50:00     5:50:00         1:00:00
LOL大乱斗+下棋_part2  5:49:55     6:50:00         1:00:05
LOL大乱斗+下棋_part3  6:49:55     7:35:50.657000  0:45:55.657000
```

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ2FudHRcbiAgICBkYXRlRm9ybWF0IEhIOm1tOnNzXG4gICAgYXhpc0Zvcm1hdCAlSDolTTolU1xuICAgIHRvZGF5TWFya2VyIG9mZlxuICAgIHRpdGxlIOWIhlDnu5PmnpxcbiAgICBcbiAgICBzZWN0aW9uIOi-k-WHuuaWh-S7tlxuICAgIOWOn-elnl9wYXJ0MTogYWN0aXZlLCBvZjEsIDAwOjAwOjAwLCAwMTowMDowMFxuICAgIOWOn-elnl9wYXJ0MjogYWN0aXZlLCBvZjIsIDAwOjU5OjU1LCAwMjowMDowMFxuICAgIOWOn-elnl9wYXJ0MzogYWN0aXZlLCBvZjMsIDAxOjU5OjU1LCAwMzowMDowMFxuICAgIOWOn-elnl9wYXJ0NDogYWN0aXZlLCBvZjQsIDAyOjU5OjU1LCAwNDowMDowMFxuICAgIOWOn-elnl9wYXJ0NTogYWN0aXZlLCBvZjUsIDAzOjU5OjU1LCAwNDo1MDowMFxuICAgIExPTOWkp-S5seaWlyvkuIvmo4tfcGFydDE6IGFjdGl2ZSwgb2Y2LCAwNDo1MDowMCwgMDU6NTA6MDBcbiAgICBMT0zlpKfkubHmlpcr5LiL5qOLX3BhcnQyOiBhY3RpdmUsIG9mNywgMDU6NDk6NTUsIDA2OjUwOjAwXG4gICAgTE9M5aSn5Lmx5paXK-S4i-aji19wYXJ0MzogYWN0aXZlLCBvZjgsIDA2OjQ5OjU1LCAwNzozNTo1MFxuICAgIHNlY3Rpb24g5Y6f5paH5Lu2XG4gICAgWzIwMjItMDEtMDUgMTMtNTYtNDFdW-WRqOmAuOmAuOWTpuWVpuWVpl1b5YWI6LeR5Zu-fuaZmuS4iuaKveWNoV1fMS5tcDQ6IGFjdGl2ZSwgaWYxLCAwMDowMDowMCwgMDM6MDA6MDBcbiAgICBbMjAyMi0wMS0wNSAxMy01Ni00MV1b5ZGo6YC46YC45ZOm5ZWm5ZWmXVvlhYjot5Hlm75-5pma5LiK5oq95Y2hXV8yLm1wNDogYWN0aXZlLCBpZjIsIDAzOjAwOjAwLCAwNjowMDowMFxuICAgIFsyMDIyLTAxLTA1IDEzLTU2LTQxXVvlkajpgLjpgLjlk6bllabllaZdW-WFiOi3keWbvn7mmZrkuIrmir3ljaFdXzMubXA0OiBhY3RpdmUsIGlmMywgMDY6MDA6MDAsIDA3OjM1OjUxIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/edit/#eyJjb2RlIjoiZ2FudHRcbiAgICBkYXRlRm9ybWF0IEhIOm1tOnNzXG4gICAgYXhpc0Zvcm1hdCAlSDolTTolU1xuICAgIHRvZGF5TWFya2VyIG9mZlxuICAgIHRpdGxlIOWIhlDnu5PmnpxcbiAgICBcbiAgICBzZWN0aW9uIOi-k-WHuuaWh-S7tlxuICAgIOWOn-elnl9wYXJ0MTogYWN0aXZlLCBvZjEsIDAwOjAwOjAwLCAwMTowMDowMFxuICAgIOWOn-elnl9wYXJ0MjogYWN0aXZlLCBvZjIsIDAwOjU5OjU1LCAwMjowMDowMFxuICAgIOWOn-elnl9wYXJ0MzogYWN0aXZlLCBvZjMsIDAxOjU5OjU1LCAwMzowMDowMFxuICAgIOWOn-elnl9wYXJ0NDogYWN0aXZlLCBvZjQsIDAyOjU5OjU1LCAwNDowMDowMFxuICAgIOWOn-elnl9wYXJ0NTogYWN0aXZlLCBvZjUsIDAzOjU5OjU1LCAwNDo1MDowMFxuICAgIExPTOWkp-S5seaWlyvkuIvmo4tfcGFydDE6IGFjdGl2ZSwgb2Y2LCAwNDo1MDowMCwgMDU6NTA6MDBcbiAgICBMT0zlpKfkubHmlpcr5LiL5qOLX3BhcnQyOiBhY3RpdmUsIG9mNywgMDU6NDk6NTUsIDA2OjUwOjAwXG4gICAgTE9M5aSn5Lmx5paXK-S4i-aji19wYXJ0MzogYWN0aXZlLCBvZjgsIDA2OjQ5OjU1LCAwNzozNTo1MFxuICAgIHNlY3Rpb24g5Y6f5paH5Lu2XG4gICAgWzIwMjItMDEtMDUgMTMtNTYtNDFdW-WRqOmAuOmAuOWTpuWVpuWVpl1b5YWI6LeR5Zu-fuaZmuS4iuaKveWNoV1fMS5tcDQ6IGFjdGl2ZSwgaWYxLCAwMDowMDowMCwgMDM6MDA6MDBcbiAgICBbMjAyMi0wMS0wNSAxMy01Ni00MV1b5ZGo6YC46YC45ZOm5ZWm5ZWmXVvlhYjot5Hlm75-5pma5LiK5oq95Y2hXV8yLm1wNDogYWN0aXZlLCBpZjIsIDAzOjAwOjAwLCAwNjowMDowMFxuICAgIFsyMDIyLTAxLTA1IDEzLTU2LTQxXVvlkajpgLjpgLjlk6bllabllaZdW-WFiOi3keWbvn7mmZrkuIrmir3ljaFdXzMubXA0OiBhY3RpdmUsIGlmMywgMDY6MDA6MDAsIDA3OjM1OjUxIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRlZmF1bHRcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)

## 配置文件说明

```toml
# 可选，ffmpeg 二进制路径
ffmpegBin = "ffmpeg"
# 可选，ffprobe 二进制路径
ffprobeBin = "ffprobe"
# 可选，分P长度，为空则不限制
maxPartLength = "01:00:00"
# 可选，如果最后一个分P的长度小于 maxPartLength * latestPartGreedy 则不独立分P
latestPartGreedy = 0.1
# 可选，在开始前将所有输入文件先连接为一个，之后用这个文件来执行分卷。在对一堆flv执行分卷时，打开这个会加快速度
reMuxAtFirst = false

[[projects]]
# 输入文件所在目录
workdir = "./"
# 输入文件列表
files = [
    "[2021-10-30 20-45-18][周逸逸哦啦啦][今晚把树脂肝完].mp4",
    "[2021-10-30 20-56-01][周逸逸哦啦啦][今晚把树脂肝完].mp4",
    "[2021-10-30 18-37-23][周逸逸哦啦啦][今晚把树脂肝完].mp4"
]
[[projects.parts]]
# 分P的名字
name = "原神"
# 可选，当不指定时使用上一个 part 的 end 作为 start
start = "00:30:00"
# 可选，用那个文件的相对时间，不指定或为0时，使用绝对时间
# 比如 start_idx = 2 时，这一个 part 的开始时间是从第二个文件（[2021-10-30 20-56-01][周逸逸哦啦啦][今晚把树脂肝完].mp4）的 30 分钟开始
start_idx = 0
# 结束时间
end = "04:50:00"
# 可选，同 start_idx
end_idx = 0

[[projects.parts]]
# 最后一个 part 的 end 可以不指定，到文件结束为止
name = "LOL大乱斗+下棋"
```
