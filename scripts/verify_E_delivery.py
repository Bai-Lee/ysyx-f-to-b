"""Read-only integrity verification for the completed E engineering delivery.

This checks retained results, source bindings and package contents. It does not
rerun the long simulations or claim new physical/visual acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import tarfile
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_ROOT = "/workspace/projects/ysyx_f_to_b/"
CORE_COUNTS = {"E5": 17, "E6": 22, "E7": 30, "E8": 10}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def digest(stream):
    h = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(block)
    return h.hexdigest()


def sha(path):
    with Path(path).open("rb") as stream:
        return digest(stream)


def local_path(path):
    text = str(path).replace("\\", "/")
    if text.startswith(ORIGINAL_ROOT):
        return ROOT / text[len(ORIGINAL_ROOT):]
    p = Path(text)
    return p if p.is_absolute() else ROOT / p


def safe_member(name):
    p = PurePosixPath(name)
    require(not p.is_absolute() and ".." not in p.parts and "\\" not in name,
            f"Unsafe archive name: {name}")
    return p


def check_file(path, expected):
    require(Path(path).is_file(), f"Missing file: {path}")
    require(sha(path) == expected, f"SHA-256 mismatch: {path}")


def verify_tar(path, rows, prefix="", extras=()):
    expected = {row["path"]: row for row in rows}
    require(len(expected) == len(rows), f"Duplicate expected tar entries: {path}")
    seen = set()
    with tarfile.open(path, "r|gz") as archive:
        for member in archive:
            safe_member(member.name)
            if not member.isfile():
                continue
            require(member.name.startswith(prefix), f"Wrong tar prefix: {member.name}")
            name = member.name[len(prefix):]
            require(name not in seen, f"Duplicate tar entry: {name}")
            seen.add(name)
            if name in extras:
                continue
            require(name in expected, f"Unexpected tar entry: {name}")
            row = expected[name]
            if "bytes" in row:
                require(member.size == row["bytes"], f"Tar size mismatch: {name}")
            with archive.extractfile(member) as stream:
                require(digest(stream) == row["sha256"], f"Tar SHA-256 mismatch: {name}")
    require(seen == set(expected) | set(extras), f"Missing tar entries: {path}")
    return len(expected)


def check_zip_members(archive, rows, extras=()):
    names = archive.namelist()
    require(len(names) == len(set(names)), "Duplicate ZIP entries")
    for name in names:
        safe_member(name)
    require(set(names) == {r["path"] for r in rows} | set(extras), "ZIP entry set mismatch")
    for row in rows:
        info = archive.getinfo(row["path"])
        require(info.file_size == row["bytes"], f"ZIP size mismatch: {row['path']}")
        with archive.open(info) as stream:
            require(digest(stream) == row["sha256"], f"ZIP SHA-256 mismatch: {row['path']}")
    require(archive.testzip() is None, "ZIP CRC mismatch")


def checker_controls():
    payload = b"E delivery integrity positive control\n"
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("fixture.txt", payload)
    row = {"path": "fixture.txt", "bytes": len(payload),
           "sha256": hashlib.sha256(payload).hexdigest()}
    with zipfile.ZipFile(buffer) as archive:
        check_zip_members(archive, [row])
        try:
            check_zip_members(archive, [{**row, "sha256": "0" * 64}])
        except ValueError as error:
            require("SHA-256 mismatch" in str(error), "Wrong negative-control failure")
        else:
            raise ValueError("Corrupt digest was accepted")
    try:
        safe_member("../escape.txt")
    except ValueError:
        pass
    else:
        raise ValueError("Traversal name was accepted")
    return {"valid_archive_accepted": True, "corrupt_digest_rejected": True,
            "traversal_name_rejected": True}


def markdown_links(external=False):
    docs = [ROOT / "README.md", ROOT / "reports/E_REPORT.md", ROOT / "reports/E_TASKS.md",
            ROOT / "E/offline/README.md", ROOT / "E/E9/SCOPE.md"]
    for stage in range(5, 9):
        docs.append(ROOT / f"reports/E{stage}_REPORT.md")
        docs.extend(sorted((ROOT / f"E/E{stage}").glob("*.md")))
    count = 0
    outside = []
    for path in sorted(set(docs)):
        require(path.is_file(), f"Missing authored document: {path}")
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf8"), flags=re.S)
        for match in re.finditer(r"!?\[[^\]]*\]\(([^\n)]+)\)", text):
            link = match.group(1).strip().strip("<>")
            if not link or link.startswith(("#", "http:", "https:", "mailto:")):
                continue
            target = Path(unquote(link.split("#", 1)[0]))
            target = target if target.is_absolute() else path.parent / target
            target = target.resolve()
            if not target.is_relative_to(ROOT.resolve()):
                outside.append(str(target))
                if not external:
                    continue
            require(target.exists(), f"Broken Markdown link: {path}: {link}")
            count += 1
    return {"documents": len(set(docs)), "resolved_local_links": count,
            "external_reference_paths": sorted(set(outside)),
            "scope": "File-target resolution only; not a full Markdown/math renderer test"}


def verify_project(external=False, require_final=True):
    result = {"status": "PASS", "verification_kind": "read-only retained-evidence integrity",
              "checker_controls": checker_controls()}
    stages = {}
    for stage in range(1, 9):
        path = ROOT / f"reports/E{stage}_AUDIT.json"
        data = load(path)
        require(data["status"] == "PASS", f"Stage audit is not PASS: E{stage}")
        if stage >= 3:
            require(data["stage_complete"] is True, f"Stage incomplete: E{stage}")
        stages[f"E{stage}"] = {"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)}
    result["stage_audits"] = stages
    require(len(load(ROOT / "reports/E3_AUDIT.json")["declared_exceptions"]) == 6,
            "E3 declared exception count changed")
    state = load(ROOT / "config/task_status.json")
    tasks = {r["id"]: r for r in state["tasks"]}
    require(len(tasks) == len(state["tasks"]), "Duplicate task IDs")
    remaining = load(ROOT / "reports/E_remaining_results.json")
    records = {r["id"]: r for r in remaining["records"]}
    frozen = load(ROOT / "E/runtime/course_specs.json")
    require(set(records) == {r["id"] for r in frozen["tasks"]} and len(records) == 96,
            "E5-E9 scope does not match its frozen 96 requirements")
    require(len(records) == len(remaining["records"]), "Duplicate E5-E9 result IDs")
    for stage, total in CORE_COUNTS.items():
        for number in range(1, total + 1):
            key = f"{stage}-M{number:03}"
            require(records[key]["status"].startswith("PASS"), f"Required task not passed: {key}")
    evidence_paths = set()
    for key, row in records.items():
        require(tasks[key]["status"] == row["status"], f"Task/result disagreement: {key}")
        require(row["evidence"], f"No evidence or scope explanation: {key}")
        for item in row["evidence"]:
            path = local_path(item)
            require(path.exists(), f"Missing evidence for {key}: {path}")
            if path.is_dir():
                require(next(path.iterdir(), None) is not None, f"Empty evidence directory: {path}")
            evidence_paths.add(str(path))
    for key in ("E9-M001", "E9-M002", "E9-O001"):
        require(records[key]["status"] == "EXCLUDED_SCOPE", f"Personal-scope policy changed: {key}")
    require(state["current_stage"] == "E" and state["stage_status"] ==
            "COMPLETE_ENGINEERING_WITH_DECLARED_ADAPTATIONS", "Final task state mismatch")
    require(load(ROOT / "config/execution_policy.json")["stop_after"] == "E", "Stage boundary changed")
    result["scope"] = {"E5_E8_core_passed": sum(CORE_COUNTS.values()),
                       "E5_E9_records": len(records), "evidence_paths": len(evidence_paths),
                       "status_counts": dict(Counter(r["status"] for r in records.values()))}
    snapshots = []
    for stage, field in (("E5", "runtime_snapshot"), ("E6", "snapshot"), ("E7", "snapshot")):
        for row in load(ROOT / f"reports/{stage}_AUDIT.json")[field]:
            check_file(local_path(row["path"]), row["sha256"])
            snapshots.append({"stage": stage, **row})
    result["frozen_snapshot_files"] = len(snapshots)
    front = load(ROOT / "reports/E8_front_audit.json")
    require(front["status"] == "PASS" and front["synthesis_rtl_matches_current"] is True,
            "Final synthesis frontend audit failed")
    for row in front["rtl_files"]:
        check_file(ROOT / row["path"], row["sha256"])
    result["current_physical_candidate_rtl_files"] = len(front["rtl_files"])
    for row in frozen["sources"]:
        check_file(local_path(row["copy"]), row["sha256"])
        if external:
            check_file(Path(row["source"]), row["sha256"])
    if external:
        archive_root = ROOT.parents[1] / "YSYX_F_B_Archive"
        check_file(Path(state["source"]), state["source_sha256"])
        raw_sources = {r["source"]["raw"]: r["source"]["source_sha256"]
                       for r in tasks.values() if re.match(r"E[1-9]-", r["id"])}
        for path, expected in raw_sources.items():
            check_file(archive_root / path, expected)
        result["external_original_sources_verified"] = len(raw_sources) + 6
    result["frozen_requirement_copies_verified"] = len(frozen["sources"])
    source_lock = load(ROOT / "reports/E_offline_sources.json")
    require(source_lock["status"] == "PASS", "Offline source export failed")
    for row in source_lock["repositories"]:
        check_file(ROOT / row["delivery_path"], row["sha256"])
    check_file(ROOT / source_lock["provided_klib"]["path"], source_lock["provided_klib"]["sha256"])
    result["offline_source_archives"] = len(source_lock["repositories"]) + 1
    tar_counts = {}
    for report, field in (("E_runtime_export", "members"), ("E7_batch_export", "members"),
                          ("E8_native_evidence_export", "files")):
        data = load(ROOT / f"reports/{report}.json")
        require(data["status"] == "PASS", f"Export report failed: {report}")
        path = ROOT / data["archive"]
        check_file(path, data["sha256"])
        tar_counts[report] = verify_tar(path, data[field])
    export = load(ROOT / "reports/E8_signoff_export.json")
    require(export["status"] == "PASS", "Signoff export failed")
    manifest = load(ROOT / "E/E8/signoff/manifest.json")
    check_file(ROOT / export["archive"], export["sha256"])
    rows = [{"path": r["destination"], "sha256": r["sha256"], "bytes": r["size_bytes"]}
            for r in manifest["files"]]
    tar_counts["E8_signoff_export"] = verify_tar(ROOT / export["archive"], rows,
                                               prefix="cpu_baseline_signoff_package/",
                                               extras=("README.md", "manifest.json", "summary.json"))
    with tarfile.open(ROOT / export["archive"]) as archive:
        for filename in ("manifest.json", "summary.json"):
            with archive.extractfile("cpu_baseline_signoff_package/" + filename) as stream:
                require(digest(stream) == sha(ROOT / "E/E8/signoff" / filename),
                        f"Signoff metadata differs from package: {filename}")
    audit8 = load(ROOT / "reports/E8_AUDIT.json")
    require(audit8["constraint_frequency_mhz"] == 50 and len(audit8["timing_corners"]) == 13,
            "Final physical qualification changed")
    require(all(x["state"] == "pass" for x in audit8["quality_gates"].values()), "Signoff gate failed")
    initial = next(x for x in manifest["files"] if x["role"] == "initial.verilog")
    require(initial["sha256"] == audit8["source_netlist_sha256"], "Physical candidate changed")
    baseline = next(x for x in load(ROOT / "reports/E7_synthesis.json")["variants"]
                    if x["variant"] == "baseline")
    require(initial["sha256"] == baseline["netlist_sha256"] and
            baseline["rtl_sha256"] == front["combined_sha256"],
            "RTL/synthesis/physical input provenance mismatch")
    summary = export["summary"]
    require(summary["checks"]["home_checklist"]["blocked"] == 0 and
            summary["checks"]["home_checklist"]["unavailable"] == 0, "Unresolved signoff blocker")
    result["verified_tar_members"] = tar_counts
    visual_count = 0
    for stage in ("E7", "E8"):
        review = load(ROOT / f"reports/{stage}_visual_review.json")
        require(review["status"] == "PASS", f"Visual review incomplete: {stage}")
        path_field = "file" if stage == "E7" else "path"
        for row in review["images"]:
            check_file(local_path(row[path_field]), row["sha256"])
            visual_count += 1
    result["retained_visual_image_hashes"] = visual_count
    result["markdown"] = markdown_links(external)
    result["limits"] = ["Prior functional and visual results are retained acceptance, not rerun here.",
                        "No SDF transient timing, manufactured silicon, formal all-input proof, or official admission claim."]
    if require_final:
        final = load(ROOT / "reports/E_AUDIT.json")
        require(final["status"] == "PASS" and final["stage_complete"] is True, "Whole-E audit incomplete")
        require(final["verification"]["stage_audits"] == stages, "Stage audit changed after whole-E acceptance")
    return result


def verify_delivery(path):
    path = Path(path)
    receipt = load(ROOT / "reports/E_delivery_archive.json")
    require(receipt["status"] == "PASS", "Delivery receipt failed")
    check_file(path, receipt["sha256"])
    require(path.with_suffix(".zip.sha256").read_text().split()[0] == receipt["sha256"],
            "ZIP SHA-256 sidecar mismatch")
    manifest_name = "reports/E_delivery_manifest.json"
    with zipfile.ZipFile(path) as archive:
        manifest_bytes = archive.read(manifest_name)
        require(hashlib.sha256(manifest_bytes).hexdigest() == receipt["manifest_sha256"],
                "Packaged manifest digest mismatch")
        manifest = json.loads(manifest_bytes)
        check_zip_members(archive, manifest["entries"], extras=(manifest_name,))
        for row in manifest["entries"]:
            check_file(ROOT / row["path"], row["sha256"])
    return {"status": "PASS", "archive": str(path), "sha256": receipt["sha256"],
            "verified_entries": len(manifest["entries"]) + 1, "crc_and_all_sha256": True,
            "current_project_matches_archive": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", action="store_true", help="Also check original archive files at their locked paths")
    parser.add_argument("--archive", type=Path, help="Also verify every ZIP entry, CRC, sidecar and current local file")
    args = parser.parse_args()
    result = verify_project(external=args.external)
    if args.archive:
        result["delivery"] = verify_delivery(args.archive)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
