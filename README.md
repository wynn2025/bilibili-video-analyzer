# B站视频数据分析器 (Bilibili Video Data Analyzer)

> 输入B站视频URL/BV号，一键提取播放/点赞/投币/收藏/弹幕/评论数据，生成终端可视化报告。

## 功能亮点

- 核心数据看板：播放量、点赞、投币、收藏、评论、弹幕、分享一目了然
- 质量评估：互动率等级(S/A/B/C/D)、点赞率、弹幕率、投币比
- 综合评分：0-100分制，含可视化进度条
- 优化建议：基于数据自动生成改进建议
- 美观终端输出：ANSI彩色+进度条可视化

## 使用方法

```bash
# 方式1：直接传BV号
python bilibili_analyzer.py BV1GJ411x7h7

# 方式2：传完整URL
python bilibili_analyzer.py https://www.bilibili.com/video/BV1GJ411x7h7
```

## 输出示例

```
  --- Video Info ---
  Title:    【官方 MV】Never Gonna Give You Up
  UP:       索尼音乐中国 (UID:486906719)
  Duration: 3m33s

   Core Data Dashboard
  ▶ Views      ████████████████████████████    9962.3万
  👍 Likes      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░     272.7万

   Quality Metrics
  Engagement:  7.01% [B-Tier OK]

   Score
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░ 42/100 Average
```

## 依赖

- Python 3.7+
- 无第三方依赖（纯标准库）

## 适用人群

- B站UP主（分析自己和竞品视频表现）
- 内容运营（评估视频传播效果）
- 数据分析师（快速获取B站视频数据）
- MCN机构（批量评估达人视频质量）
