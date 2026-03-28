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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

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

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
