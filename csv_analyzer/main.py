import argparse
from pathlib import Path
import pandas as pd

def analyze_csv(file_path: Path, group_by: str | None, target: str | None, out: Path | None):
    if not file_path.exists():
        raise FileNotFoundError(f"CSV not found: {file_path}")

    df = pd.read_csv(file_path)

    lines = []
    lines.append(f"# CSV Report: {file_path.name}\n")

    lines.append("## Basic Info")
    lines.append(f"- Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    lines.append(f"- Columns: {', '.join(df.columns)}\n")

    lines.append("## Dtypes")
    lines.append(df.dtypes.to_string())
    lines.append("")

    lines.append("## Missing Values (count)")
    missing = df.isna().sum()
    lines.append(missing.to_string())
    lines.append("")

    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        lines.append("## Numeric Summary (describe)")
        lines.append(numeric_df.describe().to_string())
        lines.append("")
    else:
        lines.append("## Numeric Summary")
        lines.append("No numeric columns found.\n")

    if group_by:
        if group_by not in df.columns:
            raise ValueError(f"--group-by column not found: {group_by}")

        lines.append(f"## Group Summary by `{group_by}`")

        if target:
            if target not in df.columns:
                raise ValueError(f"--target column not found: {target}")

            if pd.api.types.is_numeric_dtype(df[target]):
                grouped = (
                    df.groupby(group_by)[target]
                    .agg(["count", "mean", "min", "max"])
                    .sort_values("mean", ascending=False)
                )
                lines.append(grouped.to_string())
            else:
                grouped = df.groupby(group_by)[target].value_counts().head(20)
                lines.append(grouped.to_string())
        else:
            grouped = df[group_by].value_counts()
            lines.append(grouped.to_string())

        lines.append("")

    report = "\n".join(lines)
    print(report)

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"\n✅ Saved report to: {out}")

def main():
    parser = argparse.ArgumentParser(description="Analyze a CSV file and print a report.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--group-by", default=None, help="Column to group by (optional)")
    parser.add_argument("--target", default=None, help="Column to summarize per group (optional)")
    parser.add_argument("--out", default=None, help="Output report path (optional), e.g. report.md")
    args = parser.parse_args()

    file_path = Path(args.file).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve() if args.out else None

    analyze_csv(file_path, args.group_by, args.target, out_path)

if __name__ == "__main__":
    main()
