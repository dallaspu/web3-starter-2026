#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""就地刷新本仓库 README 里写死的 ★星数 与最后推送日期。⛔ 只改数字，不动一个字正文。

    python3 .github/refresh_numbers.py --check    # 只报差异
    python3 .github/refresh_numbers.py --apply    # 写盘

🔴 为什么必须有这个：
   本文的整个论点是"过期的清单会害人"，而它自己写死了几十处 `★N · YYYY-MM-DD`。
   ⇒ 一篇批判过期清单的文章自己过期，是最难看的失败形态。
   实测：上线后**一天**就漂了 14 处。

🔴 覆盖率是本脚本的核心判据：
   一个只覆盖 33/35 处的替换器会**安静地**留下 2 个过期数字，
   而所有输出都显示"已刷新" ⇒ 比不刷新更糟（你以为它是新的）。
   ⇒ 所以先做**全覆盖断言**：每个 ★ 必须被某条规则接住或在显式豁免名单里，
     否则直接退出，⛔ 不部分执行。

⚠️ 这个文件是 CI 版（跑在 GitHub Actions 里）：
   token 从 `GITHUB_TOKEN` 环境变量取，⛔ 不走代理、⛔ 不读本地密钥文件。
   本地那份在 `web3/refresh_numbers.py`（走 :19002，同时处理两份文件）。
"""
import argparse, json, os, re, sys, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "README.md")

# 三种写法都要接住：
#   A: **[owner/repo](url)** ★1,234 · 2026-09-24
#   B: **[Name](url)** (★1,234 · 2026-09-24)
#   C: **[Name](url)** (★1,234)                 ← 无日期
RULES = [
    re.compile(r"github\.com/(?P<full>[\w.-]+/[\w.-]+)\)\*\*\s*★(?P<stars>[\d,]+)"
               r"(?P<mid>\s*·\s*)(?P<date>20\d\d-\d\d-\d\d)"),
    re.compile(r"github\.com/(?P<full>[\w.-]+/[\w.-]+)\)\*\*\s*\(★(?P<stars>[\d,]+)"
               r"(?P<mid>\s*·\s*)(?P<date>20\d\d-\d\d-\d\d)\)"),
    re.compile(r"github\.com/(?P<full>[\w.-]+/[\w.-]+)\)\*\*\s*\(★(?P<stars>[\d,]+)\)"),
]

# 🔴 显式豁免：这些 ★ 是**反面证据**，⛔ 不刷新。
#    「已停更」表里写的是"星数很高、但某个日期之后没人推过代码"——
#    ⭐ 那个星数存在的意义恰恰是"高星≠还活着"，刷新它等于把论据改掉；
#    ⚠️ 日期更不能动：`no push since 2024-08` 是论点的支撑，
#       自动改成今天就是**把一句真话改成假话**。
#    ⇒ 豁免必须显式列举，⛔ 不能靠"正则碰巧没匹配到"（那是安静的）。
EXEMPT = [
    "crytic/awesome-ethereum-security",
    "smartcontractkit/full-blockchain-solidity-course-js",
]
EXEMPT_RE = re.compile(
    r"`(?:" + "|".join(re.escape(e) for e in EXEMPT) + r")`\s*\|\s*★[\d,]+")

_cache = {}


def live(full, tok):
    if full in _cache:
        return _cache[full]
    h = {"Accept": "application/vnd.github+json", "User-Agent": "refresh-numbers"}
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    try:
        d = json.load(urllib.request.urlopen(
            urllib.request.Request(f"https://api.github.com/repos/{full}", headers=h),
            timeout=25))
        # ⚠️ 用 pushed_at（最后一次推代码），⛔ 不用 updated_at ——
        #    后者会被改描述、加 topic 这类无关动作刷新，那不是"还活着"的证据。
        r = (d["stargazers_count"], (d.get("pushed_at") or "")[:10])
    except urllib.error.HTTPError as e:
        print(f"    ::warning::{full} HTTP {e.code}"
              + ("（仓库可能已删/改名，是要处理的发现）" if e.code == 404 else ""))
        r = None
    except Exception as e:
        print(f"    ::warning::{full} {e}")
        r = None
    _cache[full] = r
    return r


def audit(src, label):
    """🔴 全覆盖断言。豁免与命中分开报数，⛔ 不让豁免数悄悄增长。"""
    total = len(re.findall(r"★", src))
    marked = EXEMPT_RE.sub("<EXEMPT>", src)
    exempted = total - len(re.findall(r"★", marked))
    for rule in RULES:
        marked = rule.sub("<HIT>", marked)
    left = len(re.findall(r"★", marked))
    if left:
        print(f"::error::{label}: {total} 处 ★ 里有 {left} 处既没规则接住、也没在豁免名单")
        for m in re.finditer(r".{0,80}★[\d,]+.{0,40}", marked):
            print("  … " + " ".join(m.group(0).split()))
        print("⇒ 要么补 RULES，要么加进 EXEMPT（并写清为什么不该刷新）")
        sys.exit(2)
    return total - left - exempted, exempted


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    tok = os.environ.get("GITHUB_TOKEN", "")
    if not tok:
        print("::warning::无 GITHUB_TOKEN，走匿名（60 次/小时，可能不够 36 个仓库）")

    src = open(TARGET, encoding="utf-8").read()
    covered, exempted = audit(src, "README.md")
    print(f"  {covered} 处待刷新 + {exempted} 处豁免（反面证据）= 全覆盖")

    changes, gone = [], 0

    def sub(m):
        nonlocal gone
        full, cur_s = m.group("full"), m.group("stars")
        got = live(full, tok)
        if not got:
            gone += 1
            return m.group(0)
        new_s, new_d = got
        out = m.group(0)
        old_n = int(cur_s.replace(",", ""))
        if old_n != new_s:
            changes.append((full, f"★{old_n:,}", f"★{new_s:,}"))
            out = out.replace(f"★{cur_s}", f"★{new_s:,}")
        try:
            cur_d = m.group("date")
        except IndexError:
            cur_d = None
        if cur_d and new_d and cur_d != new_d:
            changes.append((full, cur_d, new_d))
            out = out.replace(cur_d, new_d)
        return out

    new = src
    for rule in RULES:
        new = rule.sub(sub, new)

    for full, o, n in changes:
        print(f"    {full:44s} {o:>10s} -> {n}")
    if not changes:
        print("    （无漂移）")

    # 🔴 行数不能变 —— 只换数字，⛔ 不该动结构
    if len(new.splitlines()) != len(src.splitlines()):
        print("::error::行数变了 ⇒ 改到了正文，⛔ 拒绝写盘")
        sys.exit(3)
    # 🔴 抹掉所有数字后必须逐字节相同 ⇒ 证明只动了数字
    if re.sub(r"\d", "#", new) != re.sub(r"\d", "#", src):
        print("::error::非数字内容发生变化 ⇒ ⛔ 拒绝写盘")
        sys.exit(3)

    if a.apply and new != src:
        open(TARGET, "w", encoding="utf-8").write(new)
        # ⭐ 回读断言：判据取自产物，⛔ 不取自"我刚写过"
        back = open(TARGET, encoding="utf-8").read()
        assert back == new, "🔴 回读与预期不符"
        audit(back, "README.md（回读）")
        print("  已写盘并回读校验")
    elif a.apply:
        print("  内容未变，不写盘")

    if gone:
        print(f"::warning::{gone} 个仓库取不到数据，那几处保持原样 —— ⛔ 没有用猜的值填上")
    return 0


if __name__ == "__main__":
    sys.exit(main())
