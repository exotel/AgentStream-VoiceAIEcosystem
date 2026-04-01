#!/usr/bin/env python3
"""
Docs runtime checker (broken links + invariants) with NDJSON logging.

Writes to: /Users/saurabh.sharma/Desktop/Voice AI Ecosystem /.cursor/debug-2ef34b.log
Session: 2ef34b

Do not log secrets.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse


LOG_PATH = Path("/Users/saurabh.sharma/Desktop/Voice AI Ecosystem /.cursor/debug-2ef34b.log")
SESSION_ID = "2ef34b"


def log(hypothesis_id: str, location: str, message: str, data: dict) -> None:
    payload = {
        "sessionId": SESSION_ID,
        "runId": os.environ.get("DOCS_DEBUG_RUN_ID", "pre-fix"),
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def is_external(href: str) -> bool:
    href = href.strip()
    return href.startswith(("http://", "https://", "mailto:"))


def normalize_href(href: str) -> str:
    href = href.strip()
    if "#" in href:
        href = href.split("#", 1)[0]
    return href


def resolve_relative(md_path: Path, href: str, repo_root: Path) -> Path | None:
    href = normalize_href(href)
    if not href:
        return None
    if is_external(href):
        return None
    if href.startswith("#"):
        return None
    target = (md_path.parent / href).resolve()
    return target


def iter_md_files(repo_root: Path) -> list[Path]:
    md_files: list[Path] = []
    for p in repo_root.rglob("*.md"):
        parts = set(p.parts)
        if ".venv-xlsx" in parts or ".venv" in parts or "venv" in parts:
            continue
        if "site-packages" in parts:
            continue
        md_files.append(p)
    return md_files


def check_links(repo_root: Path, md_files: list[Path]) -> dict[str, int]:
    broken = 0
    outside = 0
    total_links = 0
    root = repo_root.resolve()
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except Exception as e:
            log("H_READ", f"{md}", "failed_to_read_markdown", {"error": str(e)})
            continue
        for _, href in MD_LINK_RE.findall(text):
            total_links += 1
            if is_external(href):
                if href.startswith(("http://", "https://")):
                    u = urlparse(href)
                    if not u.scheme or not u.netloc:
                        log("H_LINK", f"{md}", "malformed_external_url", {"href": href})
                continue
            target = resolve_relative(md, href, repo_root)
            if target is None:
                continue
            try:
                target.resolve().relative_to(root)
            except Exception:
                outside += 1
                log("H_LINK", f"{md}", "relative_link_points_outside_repo", {"href": href, "resolved": str(target)})
                continue
            if not target.exists():
                broken += 1
                log("H_LINK", f"{md}", "broken_relative_link", {"href": href, "resolved": str(target)})
    return {"total_links": total_links, "broken": broken, "outside": outside}


def check_invariants(repo_root: Path) -> dict[str, int]:
    """
    H_INV1: Quickstarts exist.
    H_INV2: Quickstarts contain standard headings.
    H_INV3: Docs avoid '200 calls/minute' wording.
    H_INV4: Provider support docs include an Applicability line.
    H_INV5: Support docs avoid ambiguous '200 CPM' (prefer '200 requests/minute').
    """
    inv_fail = 0

    quickstarts = list(repo_root.rglob("integrations/exotel-vsip/QUICKSTART.md"))
    if not quickstarts:
        inv_fail += 1
        log("H_INV1", "repo", "no_quickstarts_found", {})
    else:
        required_heads = ["## Prereqs", "## Outbound", "## Inbound", "## If calls fail", "## Links"]
        for qs in quickstarts:
            txt = qs.read_text(encoding="utf-8", errors="replace")
            missing = [h for h in required_heads if h not in txt]
            if missing:
                inv_fail += 1
                log("H_INV2", f"{qs}", "quickstart_missing_headings", {"missing": missing})

    md_files = iter_md_files(repo_root)
    for md in md_files:
        txt = md.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\b200\s*calls\s*/\s*minute\b", txt, flags=re.IGNORECASE):
            inv_fail += 1
            log("H_INV3", f"{md}", "found_200_calls_per_minute_wording", {})

    support_dir = repo_root / "docs" / "support"
    if support_dir.exists():
        for md in sorted(support_dir.glob("exotel-*-sip-trunk.md")):
            txt = md.read_text(encoding="utf-8", errors="replace")
            head = "\n".join(txt.splitlines()[:40])
            if not re.search(r"\bApplicability\b", head, flags=re.IGNORECASE):
                inv_fail += 1
                log("H_INV4", f"{md}", "missing_applicability_block", {})
            if re.search(r"\b200\s*CPM\b", txt):
                inv_fail += 1
                log("H_INV5", f"{md}", "found_200_CPM_ambiguous", {})

    return {"failures": inv_fail, "quickstarts": len(quickstarts)}


def main() -> int:
    repo_root = Path("/Users/saurabh.sharma/Desktop/Voice AI Ecosystem ").resolve()
    if not repo_root.exists():
        log("H_READ", "repo", "repo_root_missing", {"repo_root": str(repo_root)})
        return 2

    md_files = iter_md_files(repo_root)
    log("H_READ", "repo", "md_inventory", {"count": len(md_files)})

    link_stats = check_links(repo_root, md_files)
    log("H_LINK", "repo", "link_check_summary", link_stats)

    inv_stats = check_invariants(repo_root)
    log("H_INV", "repo", "invariants_summary", inv_stats)

    if link_stats["broken"] or link_stats["outside"] or inv_stats["failures"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

