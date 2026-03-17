"""CLI for NemoClaw Governance Integration.

Usage:
    nemoclaw-gov validate <file>...         Validate blueprint or policy files
    nemoclaw-gov validate --all <dir>       Validate all YAML/JSON in directory
    nemoclaw-gov presets list               List available presets
    nemoclaw-gov presets show <name>        Show preset contents
    nemoclaw-gov presets path <name>        Print preset file path
    nemoclaw-gov version                    Print version
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import NoReturn

from nemoclaw_governance import __version__
from nemoclaw_governance.presets import get_preset_path, list_presets, load_preset
from nemoclaw_governance.validate import ValidationResult, validate_file


def _print_result(result: ValidationResult) -> None:
    """Print a validation result in human-readable format."""
    status = "PASS" if result.passed else "FAIL"
    path = result.file_path or "(data)"
    gate = result.gate_type or "unknown"

    print(f"  [{status}] {path} ({gate})")
    if not result.passed:
        for issue in result.issues:
            print(f"    - {issue}")


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate one or more NemoClaw config files."""
    files: list[str] = []

    if args.all:
        # Scan directory for YAML/JSON files, skip non-NemoClaw configs
        scan_dir = args.files[0] if args.files else "."
        skip_patterns = {"ci-workflow", ".github", "workflows"}
        for root, _dirs, filenames in os.walk(scan_dir):
            for fname in filenames:
                if not fname.endswith((".yaml", ".yml", ".json")):
                    continue
                # Skip CI workflow files and dotdirs
                if any(p in os.path.join(root, fname) for p in skip_patterns):
                    continue
                files.append(os.path.join(root, fname))
        if not files:
            print(f"No NemoClaw config files found in {scan_dir}")
            return 1
    else:
        files = args.files

    if not files:
        print("Error: no files specified")
        print("Usage: nemoclaw-gov validate <file>...")
        return 1

    results: list[ValidationResult] = []
    for path in files:
        try:
            result = validate_file(path)
            results.append(result)
        except ValueError as exc:
            results.append(
                ValidationResult(
                    passed=False,
                    issues=[str(exc)],
                    file_path=path,
                )
            )

    # Print results
    all_passed = all(r.passed for r in results)
    print()
    print(f"NemoClaw Governance Validation ({len(results)} file(s))")
    print("=" * 50)
    for result in results:
        _print_result(result)

    print()
    total_issues = sum(len(r.issues) for r in results)
    if all_passed:
        print(f"All {len(results)} file(s) passed validation.")
    else:
        failed = sum(1 for r in results if not r.passed)
        print(f"{failed}/{len(results)} file(s) failed with {total_issues} issue(s).")

    return 0 if all_passed else 1


def cmd_presets(args: argparse.Namespace) -> int:
    """Manage NemoClaw policy presets."""
    if args.preset_action == "list":
        presets = list_presets()
        print("Available presets:")
        for name in presets:
            print(f"  - {name}")
        return 0

    elif args.preset_action == "show":
        if not args.preset_name:
            print("Error: preset name required")
            return 1
        try:
            data = load_preset(args.preset_name)
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1
        import yaml

        print(yaml.dump(data, default_flow_style=False))
        return 0

    elif args.preset_action == "path":
        if not args.preset_name:
            print("Error: preset name required")
            return 1
        try:
            path = get_preset_path(args.preset_name)
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1
        print(path)
        return 0

    print(f"Unknown preset action: {args.preset_action}")
    return 1


def cmd_version(_args: argparse.Namespace) -> int:
    """Print version."""
    print(f"nemoclaw-governance {__version__}")
    return 0


def main(argv: list[str] | None = None) -> NoReturn:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="nemoclaw-gov",
        description="NemoClaw Governance Integration -- validate blueprints and policies",
    )
    subparsers = parser.add_subparsers(dest="command")

    # validate
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate NemoClaw blueprint or policy files",
    )
    validate_parser.add_argument(
        "files",
        nargs="*",
        help="Files to validate (YAML or JSON)",
    )
    validate_parser.add_argument(
        "--all",
        action="store_true",
        help="Scan directory for all YAML/JSON files",
    )

    # presets
    presets_parser = subparsers.add_parser(
        "presets",
        help="Manage NemoClaw policy presets",
    )
    presets_parser.add_argument(
        "preset_action",
        choices=["list", "show", "path"],
        help="Preset action",
    )
    presets_parser.add_argument(
        "preset_name",
        nargs="?",
        help="Preset name (for show/path)",
    )

    # version
    subparsers.add_parser("version", help="Print version")

    args = parser.parse_args(argv)

    if args.command == "validate":
        sys.exit(cmd_validate(args))
    elif args.command == "presets":
        sys.exit(cmd_presets(args))
    elif args.command == "version":
        sys.exit(cmd_version(args))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
