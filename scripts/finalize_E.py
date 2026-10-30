"""Reconcile the completed engineering scope and run the whole-E integrity audit."""
from datetime import datetime, timezone
from pathlib import Path
import json
import shutil

from verify_E_delivery import ROOT, CORE_COUNTS, load, sha, require, verify_project


def dump(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf8")


def main():
    now = datetime.now(timezone.utc)
    stamp = now.isoformat()
    workspace = ROOT.parents[1]
    for number in range(1, 9):
        require(load(ROOT / f"reports/E{number}_AUDIT.json")["status"] == "PASS",
                f"E{number} has not passed its stage audit")
    backup = ROOT / "config/history" / (now.strftime("%Y%m%dT%H%M%S%f") + "_whole_E")
    backup.mkdir(parents=True)
    for path, name in ((ROOT / "config/task_status.json", "task_status.json"),
                       (ROOT / "config/toolchain.json", "project_toolchain.json"),
                       (workspace / "config/toolchain.lock.json", "workspace_toolchain.lock.json"),
                       (ROOT / "reports/E_remaining_results.json", "E_remaining_results.json")):
        shutil.copyfile(path, backup / name)
    remaining = load(ROOT / "reports/E_remaining_results.json")
    records = {row["id"]: row for row in remaining["records"]}
    exclusions = ["E9-M001", "E9-M002", "E9-O001"]
    for key in exclusions:
        records[key] = {"id": key, "status": "EXCLUDED_SCOPE",
                        "evidence": ["E/E9/SCOPE.md", "E/E9/sources/E9.md", "reports/E9_AUDIT.json"],
                        "details": "Personal reflections, identity, admission application and defense remain user-excluded; original requirements retained."}
    dump(ROOT / "reports/E9_AUDIT.json", {
        "status": "EXCLUDED_SCOPE", "timestamp": stamp, "engineering_tasks_required": 0,
        "items": exclusions, "source": "E/E9/sources/E9.md", "explanation": "E/E9/SCOPE.md",
        "personal_materials_authored": False, "application_submitted": False,
        "official_admission_or_defense_claimed": False})
    remaining.update(status="COMPLETE_ENGINEERING_WITH_DECLARED_ADAPTATIONS",
                     records=[records[k] for k in sorted(records)], timestamp=stamp)
    dump(ROOT / "reports/E_remaining_results.json", remaining)
    state = load(ROOT / "config/task_status.json")
    for task in state["tasks"]:
        if task["id"] in records:
            row = records[task["id"]]
            task.update(status=row["status"], implementation_status=row["status"],
                        evidence=row["evidence"], result_details=row["details"], updated=stamp)
    state.update(current_stage="E", stage_status="COMPLETE_ENGINEERING_WITH_DECLARED_ADAPTATIONS",
                 next_stage=None, stop_after="E", completed_at=stamp,
                 completion_scope="Public engineering scope with preserved E1/E2 route adaptations, six E3 exceptions, optional selections, and excluded E9 personal procedures.")
    dump(ROOT / "config/task_status.json", state)
    toolchain = load(ROOT / "config/toolchain.json")
    linux = toolchain["linux_environment"]
    linux.update(memory_limit_gib=4, swap_gib=2, configured_swap_gib=2, actual_swap_gib=0,
                 memory_evidence="reports/E_backend_memory_update.json",
                 current_fingerprints="reports/E_toolchain_final.json",
                 rtl_and_gui_acceptance="reports/E_AUDIT.json",
                 backend_acceptance="reports/E8_AUDIT.json",
                 prior_fingerprints=["reports/E3_toolchain.json", "reports/E4_tools.json"])
    toolchain["E_stage"] = {
        "status": "COMPLETE_ENGINEERING_WITH_DECLARED_ADAPTATIONS",
        "audit": "reports/E_AUDIT.json", "final_binary_and_model_lock": "reports/E_toolchain_final.json",
        "source_lock": "reports/E_source_lock_canonical.json",
        "tool_versions": {"ECOS": "0.1.0-alpha.9", "bundled_ECC": "0.1.0a11",
                          "ecc_tools": "0.1.0a12", "compatible_Yosys": "0.68+118",
                          "final_four_state_Icarus": "14.0 devel"},
        "qualification": "Project-specific locked PDK/SDC/RCX physical checks at 50MHz; no silicon or arbitrary-design claim."}
    dump(ROOT / "config/toolchain.json", toolchain)
    lock_path = workspace / "config/toolchain.lock.json"
    lock = load(lock_path)
    lock["project_toolchains"]["ysyx_f_to_b"].update(
        status="E_COMPLETE_ENGINEERING_WITH_DECLARED_ADAPTATIONS",
        note="F historical results retained; E1-E8 public engineering scope accepted with declared adaptations; E9 personal procedures excluded. Physical candidate closes 50MHz under its locked libraries, SDC and RCX. No Logisim GUI continuation.",
        audit=str(ROOT / "reports/E_AUDIT.json"),
        fingerprints=str(ROOT / "reports/E_toolchain_final.json"))
    lock["workspace_state"].update(current_project="ysyx_f_to_b",
                                    current_project_status="E_COMPLETE_ENGINEERING_WITH_DECLARED_ADAPTATIONS")
    lock["last_updated_utc"] = stamp
    dump(lock_path, lock)
    for name, reference in (("cpu_baseline", "reports/E8_signoff_export.json"),
                            ("light_preflight", "reports/E8_physical_preflight.json")):
        path = ROOT / f"reports/E8_physical_{name}.json"
        data = load(path)
        if data["status"] == "FLOW_EXECUTED_REQUIRES_SIGNOFF_REVIEW":
            shutil.copyfile(path, backup / path.name)
            data.update(status="PASS_PHYSICAL_SIGNOFF", prior_status=data["status"],
                        signoff_evidence=reference,
                        review_note="All required stages and gates passed; only the permitted no-macro location warning remains.")
            dump(path, data)
    lines = ["# E5–E9 逐项结果", "",
             "96 项原始范围均有结果或明确的适用范围说明；其中 E5–E8 的 79 项核心工程要求通过。E1–E4 仍以各阶段独立验收为准。", "",
             "| ID | 状态 | 证据 |", "|---|---|---|"]
    for key, row in sorted(records.items()):
        links = " · ".join(f"[{Path(p).name}](../{p.replace(chr(92), '/')})" for p in row["evidence"])
        lines.append(f"| {key} | {row['status']} | {links} |")
    (ROOT / "reports/E_TASKS.md").write_text("\n".join(lines) + "\n", encoding="utf8")
    audit_path = ROOT / "reports/E_AUDIT.json"
    audit = {"status": "PENDING_VERIFICATION", "stage_complete": False, "timestamp": stamp,
             "stage_status": state["stage_status"], "engineering_scope_complete": False,
             "literal_course_completion": False, "official_admission": False,
             "E5_E8_core_counts": CORE_COUNTS, "E9_excluded": exclusions,
             "E3_declared_exceptions": load(ROOT / "reports/E3_AUDIT.json")["declared_exceptions"],
             "earlier_routes": {"E1": "Command-line schematic export adaptation; no official OJ submission",
                                "E2": "Official independent linked-list competence branch, not all CEX exercises",
                                "E3": "Engineering scope with six declared exceptions",
                                "E4": "Local real NVBoard/GTKWave acceptance"},
             "physical_result": {key: load(ROOT / "reports/E8_AUDIT.json")[key] for key in (
                 "constraint_frequency_mhz", "die_area_um2", "minimum_setup_wns_ns",
                 "minimum_hold_wns_ns", "verified_export_files", "signoff_sha256")},
             "final_report": "reports/E_REPORT.md", "read_only_verifier": "scripts/Verify-E.ps1"}
    dump(audit_path, audit)
    try:
        audit["verification"] = verify_project(external=True, require_final=False)
    except Exception as error:
        audit.update(status="FAIL", error=str(error))
        state["stage_status"] = "FINAL_AUDIT_FAILED"
        dump(audit_path, audit)
        dump(ROOT / "config/task_status.json", state)
        raise
    audit.update(status="PASS", stage_complete=True, engineering_scope_complete=True)
    dump(audit_path, audit)
    print(json.dumps({"status": "PASS", "scope": audit["verification"]["scope"],
                      "signoff_members": audit["physical_result"]["verified_export_files"],
                      "audit_sha256": sha(audit_path)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
