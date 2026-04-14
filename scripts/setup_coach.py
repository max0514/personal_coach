#!/usr/bin/env python3
"""
Interactive coach setup script.

Guides you through creating a new coach by:
1. Asking for author/coach details
2. Creating the coach directory
3. Generating config and progress files from templates

Usage:
    python scripts/setup_coach.py
    python scripts/setup_coach.py --id dan-koe --author "Dan Koe" --topic "personal mastery"
"""

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
COACHES_DIR = PROJECT_ROOT / "coaches"


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text


def prompt_input(prompt: str, default: str = "") -> str:
    """Get input with optional default."""
    if default:
        result = input(f"{prompt} [{default}]: ").strip()
        return result if result else default
    return input(f"{prompt}: ").strip()


def create_coach(
    coach_id: str,
    author: str,
    topic: str,
    style: str = "",
    principles: list[str] | None = None,
    user_name: str = "",
    goal: str = "",
):
    """Create a new coach from templates."""
    coach_dir = COACHES_DIR / coach_id
    coach_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    coach_name = f"{author} Coach"

    # Generate config
    config_template = (TEMPLATES_DIR / "coach-config.template.md").read_text()
    config = config_template.replace("{{COACH_NAME}}", coach_name)
    config = config.replace("{{AUTHOR_NAME}}", author)
    config = config.replace("{{TOPIC}}", topic)
    config = config.replace("{{COACH_ID}}", coach_id)
    config = config.replace("{{NOTEBOOK_IDS}}", "(to be filled after NotebookLM setup)")
    config = config.replace("{{STYLE_DESCRIPTION}}", style or "(to be defined)")

    if principles:
        for i, p in enumerate(principles, 1):
            config = config.replace(f"{{{{PRINCIPLE_{i}}}}}", p)
    # Clean remaining placeholders
    config = re.sub(r"\{\{[^}]+\}\}", "(to be filled)", config)

    (coach_dir / "config.md").write_text(config)

    # Generate progress
    progress_template = (TEMPLATES_DIR / "progress.template.md").read_text()
    progress = progress_template.replace("{{COACH_NAME}}", coach_name)
    progress = progress_template.replace("{{AUTHOR_NAME}}", author)
    progress = progress_template.replace("{{DATE}}", today)
    progress = progress_template.replace("{{USER_NAME}}", user_name or "(your name)")
    progress = progress_template.replace("{{PRIMARY_GOAL}}", goal or "(to be defined)")
    progress = re.sub(r"\{\{[^}]+\}\}", "(to be filled)", progress)

    (coach_dir / "progress.md").write_text(progress)

    print(f"\nCoach '{coach_name}' created at: coaches/{coach_id}/")
    print(f"  - Config: coaches/{coach_id}/config.md")
    print(f"  - Progress: coaches/{coach_id}/progress.md")
    print("\nNext steps:")
    print(f"  1. Edit coaches/{coach_id}/config.md to refine the personality")
    print("  2. Set up NotebookLM notebooks and add the notebook IDs")
    print(f"  3. Edit coaches/{coach_id}/progress.md with your goals")
    print('  4. Say "coach" to Claude Code to start your first session!')


def interactive_setup():
    """Run interactive setup wizard."""
    print("=" * 50)
    print("  Knowledge Coach - New Coach Setup")
    print("=" * 50)
    print()

    author = prompt_input("Author name (e.g., Dan Koe)")
    coach_id = prompt_input("Coach ID (slug)", slugify(author))
    topic = prompt_input("Core topic (e.g., personal mastery, fitness)")
    style = prompt_input("Communication style (e.g., direct, zero-fluff)", "")

    print("\nCore principles (enter up to 5, empty to skip):")
    principles = []
    for i in range(1, 6):
        p = input(f"  Principle {i}: ").strip()
        if not p:
            break
        principles.append(p)

    print("\nYour info (for progress tracking):")
    user_name = prompt_input("Your name", "")
    goal = prompt_input("Primary goal", "")

    create_coach(
        coach_id=coach_id,
        author=author,
        topic=topic,
        style=style,
        principles=principles if principles else None,
        user_name=user_name,
        goal=goal,
    )


def main():
    parser = argparse.ArgumentParser(description="Set up a new Knowledge Coach")
    parser.add_argument("--id", help="Coach ID (slug)")
    parser.add_argument("--author", help="Author name")
    parser.add_argument("--topic", help="Core topic")
    parser.add_argument("--style", help="Communication style")
    parser.add_argument("--name", help="Your name")
    parser.add_argument("--goal", help="Your primary goal")

    args = parser.parse_args()

    if args.id and args.author and args.topic:
        create_coach(
            coach_id=args.id,
            author=args.author,
            topic=args.topic,
            style=args.style or "",
            user_name=args.name or "",
            goal=args.goal or "",
        )
    else:
        interactive_setup()


if __name__ == "__main__":
    main()
