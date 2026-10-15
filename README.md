# Yongjian Wang · Personal homepage

中英双语学术主页和 GitHub 个人简介的源文件。

- 主页：https://fertaylageeze.github.io/
- GitHub：https://github.com/FertayLageeze
- 内容数据：[docs/data/profile.json](docs/data/profile.json)
- 网页：[docs/index.html](docs/index.html)
- 配套个人简介：[profile/README.md](profile/README.md) / [中文](profile/README.zh-CN.md)

## 更新内容

编辑 `docs/data/profile.json`，然后运行：

```bash
python tools/build.py
python tools/check.py
```

不需要安装依赖。`build.py` 同时生成静态网页和个人简介，论文状态、标题、作者和链接由同一份数据维护。界面样式在 `docs/assets/style.css`，语言切换和筛选逻辑在 `docs/assets/main.js`。

预览：

```bash
python -m http.server 8765 --directory docs
```

浏览器打开 `http://localhost:8765`。网页默认中文，可切换英文；关闭 JavaScript 时仍能阅读全部中文内容。

## 论文维护

- `status` 只能是 `published`、`under-review`、`withdrawn`。
- 在投稿件保留明确的在投标签；录用后再更新状态和正式出版信息。
- `functional-barriers` 已撤稿，目前仅声明计划上传 arXiv。正式上线后，将 `url` 改为真实的 arXiv 地址，并更新状态说明，勿提前添加占位链接。
- `equal_contribution` 按正式出版页面标注。
- `source` 记录内容依据。公开展示的论文范围以作者确认的清单为准。

## 发布

`FertayLageeze.github.io` 仓库的 GitHub Pages 使用 `main` 分支的 `/docs` 目录。提交生成后的 `docs/` 即可更新网站。

配套简介发布到 `FertayLageeze/FertayLageeze` 仓库，将 `profile/README.md` 和 `profile/README.zh-CN.md` 放到该仓库根目录。更新主页内容后，同步这两个文件以保持一致。

## 公开内容范围

此仓库只保存用于主页的公开内容及从作者简历中提取的独立头像。原始简历不放入仓库，不提供原始简历下载。联系方式仅公开邮箱。教育栏目只展示硕士阶段；出生日期、手机号、家庭信息不属于公开页面内容。

## 校验

`check.py` 检查论文状态、静态资源、页面锚点和公开内容范围。页面使用系统字体，本地图片，不依赖第三方追踪、外部字体服务或构建框架。
