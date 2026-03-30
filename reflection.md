# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

- Enter or update basic owner and pet information so the assistant knows who is caring for which animal.
- Add and edit care tasks (walks, feeding, medication, enrichment, grooming, and similar) with enough detail—such as duration and priority—for the system to weigh tradeoffs.
- Generate a daily plan that respects constraints and priorities, view the schedule clearly, and read a short explanation of why the assistant chose that ordering.

**a. Initial design**

The initial UML design has four classes:

- **Owner** — Represents the pet owner. Stores their name, how many minutes they have available per day, and a preferences dictionary. Responsible for updating its own profile via `update_profile()`.
- **CareTask** (dataclass) — A single care activity such as a walk, feeding, or grooming session. Each task has a title, category, duration in minutes, and a priority level. It can edit its own fields and compare priority against another task.
- **Pet** (dataclass) — Represents one pet owned by the Owner. Holds a name, species, optional notes, and a list of CareTask objects. Responsible for adding tasks and listing them.
- **Planner** — The scheduling engine. It reads constraints from the Owner (available time, preferences), selects and orders CareTask objects for a given Pet, and produces a daily plan. It also generates a human-readable explanation of its reasoning. A private helper `_fits_within_budget()` checks whether a set of tasks fits the owner's time budget.

Relationships: Owner owns zero-or-more Pets; each Pet has zero-or-more CareTasks; Planner depends on all three to build a plan.

**b. Design changes**

Yes. After reviewing the skeleton against the UML, I noticed that the `Owner` class had no `pets` field even though the UML specifies an `Owner "1" --> "0..*" Pet` relationship. I added a `pets: list[Pet]` field to `Owner` so that the one-to-many ownership relationship is represented directly in code, matching the UML diagram. Without this, there would be no way to navigate from an Owner to their Pets without passing them around separately.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler uses a **greedy priority-first** algorithm: it sorts all tasks by priority (highest first) and adds them one by one until the owner's time budget is full. This means a high-priority task is always chosen over a lower-priority one, even if skipping it would allow two smaller tasks to fit and cover more total care. For example, a 45-minute walk (priority 5) will be chosen over a 20-minute feeding + 20-minute grooming (priority 4 each), even though the two smaller tasks together provide broader coverage.

This tradeoff is reasonable because in pet care, missing a critical task (like medication or a walk for a high-energy dog) is worse than missing two lower-priority ones. The owner can always adjust priorities if they disagree with the plan. A more optimal knapsack-style algorithm would be harder to understand and explain, which conflicts with the app's goal of providing clear reasoning for its choices.

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
