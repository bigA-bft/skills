---
name: token-tracker
description: 记录每次对话的内容和 token 使用情况，保存到项目目录的 Markdown 文件中。当用户需要记录对话历史、跟踪 token 消耗时使用。
---

# Token Tracker 技能

## 功能

- 记录每次对话的完整内容（用户输入 + Claude 输出）
- 记录 token 使用情况（输入 tokens、输出 tokens）
- 保存到项目目录下的 `.claude/token-usage.md`
- 自动生成日期和时间戳
- 支持查看统计汇总

## 使用方法

### 1. 记录新对话

当完成一次对话后，使用此技能记录：

```bash
python .claude/skills/token-tracker/scripts/track.py "<用户输入>" "<Claude 输出>" <输入tokens> <输出tokens>
```

或者使用交互模式：

```bash
python .claude/skills/token-tracker/scripts/track.py
```

### 2. 查看统计

```bash
python .claude/skills/token-tracker/scripts/stats.py
```

### 3. 快速记录（无需 token 数据）

如果暂时不知道 token 数量，可以只记录对话内容：

```bash
python .claude/skills/token-tracker/scripts/track.py "<用户输入>" "<Claude 输出>"
```

## 记录文件格式

记录保存在项目根目录下的 `.claude/token-usage.md`：

```markdown
# Token 使用记录

## 2026-03-13

### 14:30 - 查询设备信息
**用户输入：** 查询设备0800ea0002FCmqtt信息
**Claude 输出：** 查询成功！设备 0800ea0002FC 的MQTT信息如下...
**Token 使用：** 输入 450, 输出 280, 总计 730

---

### 今日汇总
- 对话次数: 2
- 总输入 tokens: 1650
- 总输出 tokens: 1170
- 总计: 2820

## 总计
- 总对话次数: 2
- 总输入 tokens: 1650
- 总输出 tokens: 1170
- 总计: 2820
```

## 示例

### 示例 1：完整记录

用户："帮我记录这次对话"

```bash
python .claude/skills/token-tracker/scripts/track.py "查询设备信息" "查询成功！设备 0800ea0002FC..." 450 280
```

输出：
```
✅ 已记录到 .claude/token-usage.md
时间: 2026-03-13 14:30
输入 tokens: 450
输出 tokens: 280
总计: 730
```

### 示例 2：只记录对话内容

```bash
python .claude/skills/token-tracker/scripts/track.py "你好" "你好！有什么可以帮助你的？"
```

输出：
```
✅ 已记录到 .claude/token-usage.md
时间: 2026-03-13 14:35
（token 数据待补充）
```

### 示例 3：查看统计

```bash
python .claude/skills/token-tracker/scripts/stats.py
```

输出：
```
📊 Token 使用统计

今日 (2026-03-13):
  对话次数: 5
  输入 tokens: 2,450
  输出 tokens: 1,890
  总计: 4,340

总计:
  对话次数: 12
  输入 tokens: 8,650
  输出 tokens: 5,420
  总计: 14,070
```

## 注意事项

1. 记录文件保存在当前项目的 `.claude/token-usage.md`
2. 如果文件不存在会自动创建
3. token 数据为可选，如果暂时不知道可以留空后续补充
4. 对话内容中的双引号需要转义或使用单引号包裹
