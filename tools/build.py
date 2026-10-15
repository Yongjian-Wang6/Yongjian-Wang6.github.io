#!/usr/bin/env python3
"""Render the static homepage and GitHub profile from one public data file."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"
P = json.loads((SITE / "data/profile.json").read_text())
HOMEPAGE = f"https://{P['github'].lower()}.github.io/"
E = html.escape


def bi(value, tag="span", **attrs):
    attr = "".join(f' {k.rstrip("_").replace("_", "-")}="{E(str(v), quote=True)}"' for k, v in attrs.items())
    return (f'<{tag}{attr}><span lang="zh-CN">{E(value["zh"])}</span>'
            f'<span lang="en">{E(value["en"])}</span></{tag}>')


def label(zh, en, tag="span", **attrs):
    return bi({"zh": zh, "en": en}, tag, **attrs)


def authors(paper):
    out = []
    for author in paper["authors"]:
        name = E(author)
        if author in (P["name"], P["name_zh"]):
            name = f"<strong>{name}</strong>"
        if author in paper.get("equal_contribution", []):
            name += "<sup>†</sup>"
        out.append(name)
    return ", ".join(out)


STATUS = {
    "published": {"zh": "已发表", "en": "Published"},
    "under-review": {"zh": "在投", "en": "Under review"},
    "withdrawn": {"zh": "已撤稿 · 计划上传 arXiv", "en": "Withdrawn · arXiv planned"},
}


def paper_html(paper):
    title = E(paper["title"])
    if paper.get("url"):
        title = f'<a href="{E(paper["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{title}<span class="outbound" aria-hidden="true"> ↗</span></a>'
    note = bi(paper["note"], "p", class_="paper-note") if paper.get("note") else ""
    link = ""
    if paper.get("url"):
        name = "DOI ↗" if paper.get("doi") else "OpenReview ↗"
        link = f'<a class="text-link" href="{E(paper["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{name}</a>'
    citation = ""
    if paper.get("doi"):
        bib = "@article{wang2024brain,\n  title = {" + paper["title"] + "},\n  author = {" + " and ".join(paper["authors"]) + "},\n  journal = {Frontiers in Neuroscience},\n  volume = {18},\n  pages = {1325062},\n  year = {2024},\n  doi = {" + paper["doi"] + "}\n}"
        citation = f'<details class="citation"><summary>BibTeX</summary><pre><code>{E(bib)}</code></pre></details>'
    return f'''<article class="paper" id="paper-{E(paper['id'])}" data-status="{paper['status']}">
      <div class="paper-meta"><span class="paper-year">{paper['year']}</span>{bi(STATUS[paper['status']], class_='status ' + paper['status'])}{bi(paper['topic'], class_='paper-topic')}</div>
      <h3>{title}</h3><p class="authors">{authors(paper)}</p>
      <p class="venue">{E(paper['venue'])}</p>{note}<div class="paper-actions">{link}{citation}</div>
    </article>'''


nav = [("about", "关于", "About"), ("research", "研究", "Research"), ("publications", "论文", "Publications"), ("software", "开源", "Software"), ("experience", "经历", "Experience")]
nav_html = "".join(f'<a href="#{key}">{label(zh,en)}</a>' for key, zh, en in nav)
interests = "".join(f'<article class="interest"><span class="index">{x["number"]}</span>{bi(x["title"],"h3")}{bi(x["text"],"p")}</article>' for x in P["interests"])
papers_html = "".join(paper_html(x) for x in P["papers"])
projects = "".join(f'''<article class="project"><p class="eyebrow">{E(x['label'])}</p>{bi(x['title'],'h3')}{bi(x['text'],'p')}{f'<a class="text-link" href="{E(x["url"],quote=True)}" target="_blank" rel="noopener noreferrer">'+label('阅读论文 ↗','Read paper ↗')+'</a>' if x.get('url') else ''}</article>''' for x in P["projects"])
software = "".join(f'''<a class="software-row" href="https://github.com/{P['github']}/{x['repo']}" target="_blank" rel="noopener noreferrer"><div><h3>{E(x['name'])}</h3>{bi(x['text'],'p')}</div><span class="software-arrow" aria-hidden="true">↗</span></a>''' for x in P["software"])
experience = "".join(f'<article class="timeline-row"><p class="timeline-date">{E(x["period"])}</p><div>{bi(x["role"],"h3")}{bi(x["organization"],"p",class_="organization")}{bi(x["text"],"p",class_="experience-note")}</div></article>' for x in P["experience"])
honors = "".join(bi(x,"li") for x in P["honors"])
filters = "".join(f'<button type="button" class="filter{ " active" if key == "all" else ""}" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label(zh,en)}</button>' for key,zh,en in [("all","全部","All"),("published","已发表","Published"),("under-review","在投","Under review"),("withdrawn","撤稿与后续计划","Withdrawn & planned")])

page = f'''<!doctype html>
<html lang="zh-CN" data-language="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>Yongjian Wang · 王永健</title>
  <meta name="description" content="Yongjian Wang / 王永健 — spiking neural networks, reinforcement learning, AI for science, and healthcare AI. UCAS / Institute of Automation, CAS.">
  <meta property="og:title" content="Yongjian Wang · 王永健">
  <meta property="og:description" content="Brain-inspired intelligence, scientific reasoning, and AI for healthcare.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{HOMEPAGE}">
  <meta property="og:image" content="{HOMEPAGE}assets/portrait.png">
  <link rel="canonical" href="{HOMEPAGE}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
  <script src="assets/main.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">{label('跳转到正文','Skip to content')}</a>
  <header class="topbar"><a class="wordmark" href="#about" aria-label="Yongjian Wang, home"><span class="monogram">yw.</span><span class="wordmark-caption">RESEARCH & ENGINEERING</span></a>
    <nav aria-label="Main navigation">{nav_html}</nav>
    <button class="language-switch" type="button" aria-label="Switch to English" hidden>EN <span aria-hidden="true">↗</span></button>
  </header>
  <div class="page-layout">
    <aside class="identity" aria-label="Profile">
      <div class="portrait-wrap"><img src="assets/portrait.png" width="253" height="304" alt="Yongjian Wang / 王永健" fetchpriority="high"><span class="portrait-caption">BEIJING, CHINA</span></div>
      <h1>Yongjian<br>Wang<span class="chinese-name">王永健</span></h1>
      <div class="identity-details">{bi(P['education']['degree'],'p',class_='degree')}{bi(P['education']['institution'],'p')}{bi(P['education']['institute'],'p')}<p class="education-period">{P['education']['period']}</p></div>
      <div class="contact-links"><a href="mailto:{P['email']}"><span aria-hidden="true">✉</span> {P['email']}</a><a href="https://github.com/{P['github']}" target="_blank" rel="noopener noreferrer">GitHub <span aria-hidden="true">↗</span></a><a href="{P['openreview']}" target="_blank" rel="noopener noreferrer">OpenReview <span aria-hidden="true">↗</span></a></div>
      <p class="identity-footnote">{label('从研究想法，到可运行的系统。','From research ideas to working systems.')}</p>
    </aside>
    <main id="main">
      <section class="intro section" id="about"><p class="eyebrow">ABOUT / {label('关于我','A LITTLE ABOUT ME')}</p>
        {bi(P['intro'],'h2',class_='intro-title')}{bi(P['about'],'p',class_='intro-text')}
        <a class="intro-cta" href="mailto:{P['email']}">{label('交流研究与合作','Let’s talk research')} <span aria-hidden="true">↗</span></a>
        <div class="research-strip"><span>NEURO AI</span><span class="strip-dot" aria-hidden="true">·</span><span>AI FOR SCIENCE</span><span class="strip-dot" aria-hidden="true">·</span><span>HEALTHCARE AI</span></div>
      </section>
      <section class="section" id="research"><div class="section-heading"><h2>{label('研究方向','Research interests')}</h2><span class="section-number">01 /</span></div><div class="interests">{interests}</div>
        <div class="project-heading"><h3>{label('代表研究与项目','Selected research & projects')}</h3><span class="small-note">{label('从结构、机制到应用','Structure, mechanism, application')}</span></div><div class="projects">{projects}</div>
      </section>
      <section class="section" id="publications"><div class="section-heading"><h2>{label('论文与研究稿件','Publications & manuscripts')}</h2><span class="section-number">02 /</span></div>
        <p class="section-description">{label('在投稿件与已发表论文分别标注；撤稿论文的后续计划见条目说明。','Submission status is shown for each manuscript; plans for withdrawn work are stated in its entry.')}</p>
        <div class="filters" role="group" aria-label="Filter by publication status" hidden>{filters}</div>
        <p class="filter-result sr-only" role="status" aria-live="polite"></p><div class="paper-list">{papers_html}</div>
      </section>
      <section class="section" id="software"><div class="section-heading"><h2>{label('开源工具','Open-source software')}</h2><span class="section-number">03 /</span></div><p class="section-description">{label('为更可复现、更可检查的研究流程写一些工具。','Small tools for more reproducible, inspectable research workflows.')}</p>{software}<a class="text-link more-software" href="https://github.com/{P['github']}?tab=repositories" target="_blank" rel="noopener noreferrer">{label('查看全部公开仓库 ↗','All public repositories ↗')}</a></section>
      <section class="section" id="experience"><div class="section-heading"><h2>{label('经历与教育','Experience & education')}</h2><span class="section-number">04 /</span></div><div class="timeline">{experience}</div><div class="honors"><h3>{label('部分荣誉','Selected honors')}</h3><ul>{honors}</ul></div><p class="skills">{E(P['skills'])}</p></section>
      <footer class="footer"><p>© {P['updated'][:4]} Yongjian Wang <span aria-hidden="true">/</span> {label('最近更新','Updated')} <time datetime="{P['updated']}">{P['updated']}</time></p><a href="#about">{label('回到顶部 ↑','Back to top ↑')}</a></footer>
    </main>
  </div>
</body>
</html>
'''
(SITE / "index.html").write_text(page)


def readme(lang):
    zh = lang == "zh"
    title = "王永健 | Yongjian Wang" if zh else "Yongjian Wang | 王永健"
    lines = [f"# {title}", "", P["intro"][lang], "", P["about"][lang], "",
             f"**{P['education']['degree'][lang]}** · {P['education']['institution'][lang]} / {P['education']['institute'][lang]} · 2023–2026", "",
             f"[{'个人主页' if zh else 'Homepage'}]({HOMEPAGE}) · [Email](mailto:{P['email']}) · [OpenReview]({P['openreview']})", "",
             f"[{'English' if zh else '中文'}]({'README.md' if zh else 'README.zh-CN.md'})", "",
             f"## {'论文与研究稿件' if zh else 'Publications & manuscripts'}", ""]
    for status, heading in [("published", "已发表" if zh else "Published"), ("under-review", "在投" if zh else "Under review"), ("withdrawn", "撤稿与后续计划" if zh else "Withdrawn & planned")]:
        lines += [f"### {heading}", ""]
        for paper in P["papers"]:
            if paper["status"] != status:
                continue
            title = f'[{paper["title"]}]({paper["url"]})' if paper.get("url") else paper["title"]
            names = []
            for name in paper["authors"]:
                text = f"**{name}**" if name in (P["name"], P["name_zh"]) else name
                if name in paper.get("equal_contribution", []):
                    text += "†"
                names.append(text)
            lines += [f"- **{title}**  ", "  " + ", ".join(names) + ".  ", f"  {paper['venue']} · {paper['year']}." + (" " + paper["note"][lang] if paper.get("note") else ""), ""]
    lines += [f"## {'开源工具' if zh else 'Open-source software'}", ""]
    for item in P["software"]:
        lines += [f"- [{item['name']}](https://github.com/{P['github']}/{item['repo']}) — {item['text'][lang]}"]
    lines += ["", f"## {'研究与工程' if zh else 'Research & engineering'}", ""]
    lines += [f"- **{item['title'][lang]}** — {item['text'][lang]}" for item in P["projects"]]
    lines += ["", f"---\n\n{'最近更新' if zh else 'Updated'}: {P['updated']}", ""]
    return "\n".join(lines)


(ROOT / "profile/README.md").write_text(readme("en"))
(ROOT / "profile/README.zh-CN.md").write_text(readme("zh"))
print("Rendered docs/index.html and profile/README{,.zh-CN}.md")
