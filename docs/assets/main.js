"use strict";
(() => {
  const root = document.documentElement;
  const languageButton = document.querySelector(".language-switch");
  const filters = [...document.querySelectorAll(".filter")];
  const papers = [...document.querySelectorAll(".paper")];
  const result = document.querySelector(".filter-result");
  let activeFilter = "all";
  let language = "zh";
  try {
    language = localStorage.getItem("yw-language") === "en" ? "en" : "zh";
  } catch { /* The page also works when storage is unavailable. */ }

  function announceCount() {
    const count = papers.filter(paper => !paper.hidden).length;
    result.textContent = language === "zh" ? `显示 ${count} 篇论文或稿件` : `${count} publications or manuscripts shown`;
  }

  function setLanguage(next) {
    language = next;
    root.dataset.language = next;
    root.lang = next === "zh" ? "zh-CN" : "en";
    languageButton.innerHTML = next === "zh" ? 'EN <span aria-hidden="true">↗</span>' : '中文 <span aria-hidden="true">↗</span>';
    languageButton.setAttribute("aria-label", next === "zh" ? "Switch to English" : "切换至中文");
    document.querySelector("nav").setAttribute("aria-label", next === "zh" ? "主导航" : "Main navigation");
    document.querySelector(".identity").setAttribute("aria-label", next === "zh" ? "个人简介" : "Profile");
    document.querySelector(".filters").setAttribute("aria-label", next === "zh" ? "按论文状态筛选" : "Filter by publication status");
    try { localStorage.setItem("yw-language", next); } catch { /* Optional preference. */ }
    announceCount();
  }

  languageButton.hidden = false;
  languageButton.addEventListener("click", () => setLanguage(language === "zh" ? "en" : "zh"));
  setLanguage(language);
  document.querySelector(".filters").hidden = false;
  filters.forEach(button => button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    filters.forEach(item => {
      const active = item === button;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    papers.forEach(paper => { paper.hidden = activeFilter !== "all" && paper.dataset.status !== activeFilter; });
    announceCount();
  }));

  if ("IntersectionObserver" in window) {
    const navLinks = [...document.querySelectorAll("nav a")];
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        navLinks.forEach(link => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      }
    }, {rootMargin: "-10% 0px -65% 0px", threshold: 0});
    document.querySelectorAll("main > section[id]").forEach(section => observer.observe(section));
  }
})();
