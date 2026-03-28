# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Recent scheduler improvements include:

- Automatic time ordering for schedule entries, even when tasks are added out of order.
- Task filtering by completion status and by pet name.
- Lightweight conflict detection that returns warnings for overlapping times instead of crashing.
- Recurring task rollover: completing daily or weekly tasks can auto-create the next occurrence using timedeltas.

## Features

- Chronological sorting algorithm: schedule entries are ordered by datetime, even if added out of order.
- Conflict-pair detection: overlapping entries are grouped by timestamp and expanded into pairwise conflicts.
- Non-blocking conflict warnings: overlapping times return human-readable warnings while still allowing scheduling.
- Recurrence rollover logic: completing a daily or weekly task auto-generates the next occurrence using timedeltas.
- Task filtering pipeline: tasks can be filtered by completion status and pet name (case-insensitive matching for pet names).
- Relationship integrity checks: scheduling validates owner-pet-task consistency to prevent invalid cross-pet assignments.
- Upcoming schedule extraction: future-facing entries can be retrieved from a provided date onward, then sorted.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the automated tests with:

```bash
python -m pytest
```

The test suite covers core scheduling behavior, including chronological sorting of scheduled entries, recurring task rollover for daily tasks, and duplicate-time conflict detection. It also checks related behavior such as non-recurring completion, conflict warnings, and task state updates. My Condifence Level is around 4 out of 5 stars based on reliability and passing my 11 test cases.

### Demo
![Screenshot 1](<PawPal #1.png>)
![Screenshot 2](<PawPal #2.png>)
![Screenshot 3](<PawPal #3.png>)