
from pathlib import Path

from resume_parser import extract_resume_text
from matcher import analyze_resume


def main():
    print("=" * 45)
    print(" AI RESUME ANALYZER & JOB MATCHER")
    print("=" * 45)

    pdf_path = input(
        "Enter the full path to your resume PDF: "
    ).strip().strip('"')

    if not Path(pdf_path).is_file():
        print("Error: Resume file not found.")
        return

    job_path = Path("data/sample_job.txt")

    if not job_path.is_file():
        print("Error: Job description file not found.")
        return

    try:
        resume_text = extract_resume_text(pdf_path)
        job_text = job_path.read_text(encoding="utf-8")

        result = analyze_resume(resume_text, job_text)

        print("\n--- ANALYSIS RESULTS ---")
        print(
            f"Text similarity: "
            f"{result['similarity_score']}%"
        )

        print("\nResume skills:")
        print(", ".join(result["resume_skills"]) or "None found")

        print("\nMatching skills:")
        print(", ".join(result["matching_skills"]) or "None found")

        print("\nMissing skills:")
        print(", ".join(result["missing_skills"]) or "None found")

    except (ValueError, RuntimeError, OSError) as error:
        print(f"Could not analyze resume: {error}")


if __name__ == "__main__":
    main()
