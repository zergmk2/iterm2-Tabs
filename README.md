# iTerm2 Tabs

<div align="center">

**快速切换 iTerm2 标签页的工具**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[English](README_EN.md) | 简体中文

</div>

## ✨ 功能特性

- 🎯 **快速切换** - 一键查看并切换所有 iTerm2 标签页
- ⌨️ **键盘导航** - 使用 ↑↓ 箭头键快速导航，Enter 选中
- 🔍 **实时搜索** - 输入关键字过滤标签页
- 🎨 **现代界面** - 简洁美观的 GUI，支持深色/浅色主题
- 🚀 **独立应用** - 可打包为 macOS .app，支持 Spotlight 启动
- 🌓 **主题切换** - 支持深色和浅色两种主题

## 📸 界面预览

```
┌─────────────────────────────────────────┐
│              iTerm2 Tabs                 │
├─────────────────────────────────────────┤
│ 🔍 [搜索标签页...]                      │
├─────────────────────────────────────────┤
│ [1] vim (ssh)                           │
│ [1] ~/project (-zsh)                    │
│ [1] ✳ Claude Code (node)               │
│ [2] tail -f log.txt                    │
│                                          │
│ ↑↓ Navigate | Enter: Select | Esc: Close│
└─────────────────────────────────────────┘
```

## ⚠️ 重要提示

**在使用本应用之前，必须先启用 iTerm2 Python API：**

1. 打开 iTerm2
2. 前往 `iTerm2 > Preferences > General`
3. 找到 `Magic` 部分
4. 勾选 ✅ `Enable Python API`

![iTerm2 Python API](docs/images/iterm2-python-api.png)

**如果不启用 Python API，本应用将无法工作！**

## 📦 安装方式

### 方式 1: 下载 macOS App（推荐）

1. 前往 [Releases](https://github.com/zergmk2/iterm2-Tabs/releases) 页面
2. 下载最新的 `iterm2-tabs.app.zip`
3. 解压并移动到 Applications 目录：

```bash
unzip iterm2-tabs.app.zip
cp -R iterm2-tabs.app /Applications/
```

4. 首次运行需要授权：
```bash
open /Applications/iterm2-tabs.app
```

5. 之后可以通过 Spotlight (⌘ + Space) 搜索 "iTerm2 Tabs" 启动

### 方式 2: 使用 uv 开发环境

#### 前置要求

- macOS 10.15+
- Python 3.12+
- iTerm2 3.4+（已启用 Python API）

#### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/zergmk2/iterm2-Tabs.git
cd iterm2-Tabs

# 2. 安装 uv（如果还没安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 创建虚拟环境（Python 3.12）
uv venv --python 3.12

# 4. 安装依赖
uv sync

# 5. 运行应用
uv run python -m iterm2_tabs
```

### 方式 3: 使用传统 pip

```bash
# 1. 克隆仓库
git clone https://github.com/zergmk2/iterm2-Tabs.git
cd iterm2-Tabs

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -e .

# 4. 运行应用
python -m iterm2_tabs
```

## 🚀 使用方法

### 启动应用

#### 从 macOS App 启动

```bash
# 方式 1: 使用 Spotlight
# 按 ⌘ + Space，输入 "iTerm2 Tabs"，按 Enter

# 方式 2: 从命令行启动
open -a "iterm2-tabs"
```

#### 从命令行启动

```bash
# 使用 uv
uv run python -m iterm2_tabs

# 或使用虚拟环境
source venv/bin/activate
python -m iterm2_tabs
```

### 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `↑` / `↓` | 上下移动选择 |
| `Enter` | 选中当前标签页 |
| `Esc` | 关闭窗口 |
| 直接输入 | 实时搜索过滤 |

### 使用 iTerm2 全局快捷键（推荐）

在 iTerm2 中创建自定义快捷键：

1. 打开 `iTerm2 > Preferences > Keys`
2. 点击 `+` 添加新的快捷键
3. 设置快捷键（例如：`⌘ + ⇧ + T`）
4. 选择 Action: `Run Command...`
5. Command 输入：
   ```bash
   # 如果使用 macOS App
   open -a "iterm2-tabs"

   # 如果使用命令行版本
   /path/to/python -m iterm2_tabs
   ```

## ⚙️ 配置

创建配置文件 `~/.iterm2-tabs-config.json`：

```json
{
  "window_width": 600,
  "window_height": 400,
  "show_window_number": true,
  "show_path": true,
  "theme": "dark",
  "font_size": 12
}
```

### 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `window_width` | int | 600 | 窗口宽度 |
| `window_height` | int | 400 | 窗口高度 |
| `show_window_number` | bool | true | 显示窗口编号 |
| `show_path` | bool | true | 显示工作目录 |
| `theme` | string | "dark" | 主题：`dark` 或 `light` |
| `font_size` | int | 12 | 字体大小 |

## 🛠️ 开发指南

### 开发环境设置

```bash
# 1. 克隆仓库
git clone https://github.com/zergmk2/iterm2-Tabs.git
cd iterm2-Tabs

# 2. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 创建开发环境
uv venv --python 3.12
uv sync

# 4. 安装开发工具
uv add --dev pytest black ruff mypy
```

### 常用命令

```bash
# 运行应用
make run

# 运行测试
make test

# 代码格式化
make format

# 代码检查
make lint

# 构建 macOS App
make dist

# 清理构建文件
make clean
```

### 项目结构

```
iterm2-Tabs/
├── src/iterm2_tabs/
│   ├── __init__.py          # 包入口
│   ├── __main__.py          # 命令行入口
│   ├── app.py               # 主应用逻辑
│   ├── config.py            # 配置管理
│   ├── gui.py               # GUI 界面
│   └── iterm2_connection.py # iTerm2 API 连接
├── scripts/
│   ├── build_app.sh         # 构建 macOS App
│   ├── release.sh           # 发布脚本
│   └── bump-version.sh      # 版本号更新
├── tests/                   # 测试文件
├── docs/                    # 文档
└── pyproject.toml          # 项目配置
```

## 🐛 故障排查

### 问题: "iTerm2 is not running!"

**原因**: iTerm2 未启动或 Python API 未启用

**解决方法**:
1. 确认 iTerm2 正在运行
2. 前往 `iTerm2 > Preferences > General > Magic`
3. 勾选 `Enable Python API`
4. 重启 iTerm2

### 问题: 界面显示但没有标签页

**原因**: iTerm2 Python API 连接失败

**解决方法**:
1. 检查 iTerm2 是否有打开的标签页
2. 查看日志：`~/Library/Logs/iterm2-tabs.log`
3. 启用调试模式：`ITERM2_TABS_DEBUG=1 python -m iterm2_tabs`

### 问题: 点击标签页后没有切换

**原因**: iTerm2 窗口未获得焦点

**解决方法**:
1. 手动点击 iTerm2 窗口
2. 或在 iTerm2 中设置全局快捷键（见上文）

### 问题: macOS App 无法打开

**原因**: 安全设置阻止了未签名的应用

**解决方法**:
1. 右键点击应用，选择"打开"
2. 或在系统设置中允许运行：
   `系统设置 > 隐私与安全性 > 仍要打开`

## 📝 开发日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新历史。

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [iTerm2 Python API](https://iterm2.com/python-api) - 强大的 iTerm2 自动化接口
- [uv](https://github.com/astral-sh/uv) - 极速的 Python 包管理器

## 📧 联系方式

- GitHub: [@zergmk2](https://github.com/zergmk2)
- Issues: [GitHub Issues](https://github.com/zergmk2/iterm2-Tabs/issues)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
