# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- I designed the system around four main classes: Owner, Pet, Task, and Scheduler;
- Owner is responsible for storing the owner's name and managing the list of pets they care for.
- Pet represents an individual animal, stores its basic information such as name and species, and manages that pet's care tasks.
- Task represents a specific care activity, such as feeding, walking, or grooming, and stores the details needed to describe how often and how it should be done.
- Scheduler is responsible for organizing tasks into dated entries so the owner can view upcoming pet care activities in order.

**b. Design changes**

- My design changed during implementation.
- One important change was updating the scheduling model so each schedule entry stores both a specific pet and a specific task, instead of storing only a task. I made this change to avoid ambiguity when multiple pets can have similar tasks (for example, both pets having a "feeding" task), and to enforce accurate ownership relationships.
- I also added validation rules so tasks cannot be assigned to multiple pets and schedules cannot include tasks that do not belong to the selected pet/owner. This made the system more reliable, easier to reason about, and less likely to break as more pets and tasks are added.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler primarily considers time and ownership consistency.
- Time is used for ordering entries chronologically and for identifying overlaps when two tasks are scheduled at the same datetime.
- Ownership consistency is enforced so a task must belong to the selected pet, and that pet must belong to the active owner before the task can be scheduled.
- I also considered completion state and frequency. Completion state supports filtering views (pending vs completed), and frequency supports recurrence behavior for daily and weekly tasks.
- I decided these constraints mattered most because they directly affect correctness for a real pet owner: tasks must be attached to the right pet, shown in the right order, and repeated reliably when recurring care is needed.

**b. Tradeoffs**

- One tradeoff my scheduler makes is prioritizing simple, readable algorithms (straightforward filtering, and built-in sorting) over more complex data structures like indexed lookup tables or heaps. For example, conflict checks and task filtering are done by scanning current entries/tasks rather than maintaining extra caches.
- This is reasonable for this scenario because PawPal+ is a small, user-facing planning app with relatively low data volume per owner. The simpler approach is easier to debug, test, and extend, and the runtime cost is still fast enough for typical usage while reducing implementation risk.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- I tested core behaviors including task completion state changes, adding tasks to pets, chronological ordering of schedule entries, recurrence logic for daily tasks, and conflict detection for duplicate times.
- I also tested non-recurring completion behavior (no follow-up task created), warning behavior for overlap scheduling, and empty-task edge behavior for pets with no tasks.
- These tests were important because they cover both happy paths and high-risk edge cases. The happy-path tests confirm normal user flows work end to end, while edge-case tests reduce the chance of silent failures when data is missing or when users schedule overlapping events.

**b. Confidence**

- I am confident at about 4 out of 5 stars based on passing 11 tests and manually checking the Streamlit workflow.
- If I had more time, I would add tests for multiple simultaneous conflicts at the same timestamp (more than two entries), recurrence behavior across month/year boundaries, and validation around editing tasks after they are already scheduled.
- I would also add integration-style tests for the UI flow to verify that conflict warnings, filtering controls, and one-based display numbering remain correct after future refactors.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with how the class responsibilities stayed clear while the system grew. Owner, Pet, Task, and Scheduler each kept a focused role, which made it easier to add features like conflict warnings and recurrence without rewriting everything.

**b. What you would improve**

- In another iteration, I would introduce a dedicated ScheduleEntry data class instead of tuple-based entries to improve readability and reduce indexing mistakes.
- I would also add explicit task priority and duration fields, then build a smarter planner that can suggest time slots automatically instead of relying only on user-entered schedule times.

**c. Key takeaway**

- A key takeaway is that AI is most useful when I treat it as a collaborator, not an autopilot. The best results came from asking targeted questions, verifying suggestions with tests, and iterating on design decisions based on actual behavior.
