from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from itertools import combinations
from typing import Any


@dataclass
class Task:
	type: str
	description: str
	frequency: str
	completed: bool = False
	pet: Pet | None = field(default=None, repr=False)

	def edit(self, new_data: dict[str, Any]) -> None:
		"""Update task fields using validated input data."""
		allowed_fields = {"type", "description", "frequency", "completed"}
		for key, value in new_data.items():
			if key not in allowed_fields:
				raise ValueError(f"Unsupported task field: {key}")
			if key == "completed":
				if not isinstance(value, bool):
					raise ValueError("Task field 'completed' must be a boolean")
			else:
				if not isinstance(value, str) or not value.strip():
					raise ValueError(f"Task field '{key}' must be a non-empty string")
				value = value.strip()
			setattr(self, key, value)

	def get_details(self) -> str:
		"""Return a formatted summary of this task."""
		status = "✓ Done" if self.completed else "○ Pending"
		return f"{self.type}: {self.description} ({self.frequency}) [{status}]"

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		if self.completed:
			return
		self.completed = True

	def mark_incomplete(self) -> None:
		"""Mark this task as not completed."""
		self.completed = False


@dataclass
class Pet:
	name: str
	species: str
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Assign a task to this pet."""
		if task.pet is not None and task.pet is not self:
			raise ValueError("Task already belongs to another pet")
		if task in self.tasks:
			raise ValueError("Task is already assigned to this pet")
		task.pet = self
		self.tasks.append(task)

	def edit_task(self, task: Task, new_data: dict[str, Any]) -> None:
		"""Edit an existing task owned by this pet."""
		if task not in self.tasks:
			raise ValueError("Task is not assigned to this pet")
		task.edit(new_data)

	def remove_task(self, task: Task) -> None:
		"""Remove a task from this pet."""
		if task not in self.tasks:
			raise ValueError("Task is not assigned to this pet")
		self.tasks.remove(task)
		task.pet = None

	def get_tasks(self) -> list[Task]:
		"""Return a copy of this pet's tasks."""
		return list(self.tasks)

	def get_task_by_type(self, task_type: str) -> Task | None:
		"""Find the first task matching the given type."""
		target_type = task_type.lower()
		for task in self.tasks:
			if task.type.lower() == target_type:
				return task
		return None

	def get_pending_tasks(self) -> list[Task]:
		"""Return all incomplete tasks for this pet."""
		return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
	name: str
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner."""
		if pet in self.pets:
			raise ValueError("Pet is already assigned to this owner")
		self.pets.append(pet)

	def remove_pet(self, pet: Pet) -> None:
		"""Remove a pet from this owner."""
		if pet not in self.pets:
			raise ValueError("Pet is not assigned to this owner")
		self.pets.remove(pet)

	def get_pets(self) -> list[Pet]:
		"""Return a copy of all pets owned."""
		return list(self.pets)

	def get_all_tasks(self) -> list[Task]:
		"""Return all tasks across this owner's pets."""
		return [task for pet in self.pets for task in pet.get_tasks()]

	def get_pending_tasks(self) -> list[Task]:
		"""Return all incomplete tasks across this owner's pets."""
		return [task for task in self.get_all_tasks() if not task.completed]

	def get_pet_by_name(self, pet_name: str) -> Pet | None:
		"""Find a pet by name, case-insensitively."""
		for pet in self.pets:
			if pet.name.lower() == pet_name.lower():
				return pet
		return None


@dataclass
class Scheduler:
	owner: Owner
	entries: list[tuple[Pet, Task, datetime]] = field(default_factory=list)

	def has_time_conflict(self, date_time: datetime) -> bool:
		"""Check whether at least two scheduled entries share the same datetime.

		This uses an early-exit scan so it stops as soon as the second match is found.
		"""
		matches = 0
		for entry in self.entries:
			if entry[2] != date_time:
				continue
			matches += 1
			if matches >= 2:
				return True
		return False

	def detect_time_conflicts(
		self,
	) -> list[
		tuple[
			tuple[Pet, Task, datetime],
			tuple[Pet, Task, datetime],
		]
	]:
		"""Return all pairs of entries that occur at the exact same datetime.

		Entries are grouped by timestamp first, then pairwise combinations are generated
		inside each timestamp group.
		"""
		entries_by_time: dict[datetime, list[tuple[Pet, Task, datetime]]] = {}
		for entry in self.entries:
			entries_by_time.setdefault(entry[2], []).append(entry)

		conflicts: list[
			tuple[
				tuple[Pet, Task, datetime],
				tuple[Pet, Task, datetime],
			]
		] = []
		for same_time_entries in entries_by_time.values():
			if len(same_time_entries) < 2:
				continue
			conflicts.extend(combinations(same_time_entries, 2))

		return conflicts

	def sort_by_time(
		self,
		entries: list[tuple[Pet, Task, datetime]] | None = None,
	) -> list[tuple[Pet, Task, datetime]]:
		"""Return entries ordered by datetime. Defaults to all scheduler entries."""
		if entries is None:
			entries = self.entries
		return sorted(entries, key=lambda entry: entry[2])

	def add_entry(self, pet: Pet, task: Task, date_time: datetime) -> tuple[Pet, Task, datetime]:
		"""Add a scheduled task entry for a pet at a specific time."""
		if pet not in self.owner.pets:
			raise ValueError("Pet does not belong to this scheduler's owner")
		if task not in pet.tasks:
			raise ValueError("Task is not assigned to the provided pet")
		if task.pet is not pet:
			raise ValueError("Task-pet relationship is inconsistent")

		entry = (pet, task, date_time)
		self.entries.append(entry)
		return entry

	def get_conflict_warning(self, pet: Pet, date_time: datetime) -> str | None:
		"""Build a human-readable warning when a new entry would overlap in time.

		Returns None when no overlap exists, allowing callers to keep scheduling logic
		non-blocking while still surfacing conflicts.
		"""
		overlapping_entries = [entry for entry in self.entries if entry[2] == date_time]
		if not overlapping_entries:
			return None

		overlap_summaries = [f"{entry[0].name}:{entry[1].type}" for entry in overlapping_entries]
		formatted_time = date_time.strftime("%Y-%m-%d %H:%M")
		return (
			f"Scheduling warning: {pet.name} has an overlap at {formatted_time}. "
			f"Existing tasks at this time: {', '.join(overlap_summaries)}"
		)

	def add_entry_with_warning(
		self,
		pet: Pet,
		task: Task,
		date_time: datetime,
	) -> tuple[tuple[Pet, Task, datetime], str | None]:
		"""Schedule an entry and return an optional conflict warning.

		Unlike hard validation, this method never rejects overlaps. It is intended for a
		lightweight UX where conflicts are reported as warnings instead of exceptions.
		"""
		warning = self.get_conflict_warning(pet, date_time)
		entry = self.add_entry(pet, task, date_time)
		return entry, warning

	def remove_entry(self, entry: tuple[Pet, Task, datetime]) -> None:
		"""Remove an existing scheduled entry."""
		if entry not in self.entries:
			raise ValueError("Scheduler entry does not exist")
		self.entries.remove(entry)

	def mark_task_complete(self, entry: tuple[Pet, Task, datetime]) -> tuple[Pet, Task, datetime] | None:
		"""Complete a scheduled task and auto-create the next recurring occurrence.

		For daily tasks, the next entry is scheduled at +1 day; for weekly tasks, +1 week.
		Non-recurring tasks are simply marked complete and return None.
		"""
		if entry not in self.entries:
			raise ValueError("Scheduler entry does not exist")

		pet, task, scheduled_time = entry
		task.mark_complete()

		frequency = task.frequency.strip().lower()
		if frequency == "daily":
			next_scheduled_time = scheduled_time + timedelta(days=1)
		elif frequency == "weekly":
			next_scheduled_time = scheduled_time + timedelta(weeks=1)
		else:
			return None

		next_task = Task(
			type=task.type,
			description=task.description,
			frequency=task.frequency,
		)
		pet.add_task(next_task)
		next_entry = (pet, next_task, next_scheduled_time)
		self.entries.append(next_entry)
		return next_entry

	def view_scheduler(self) -> list[tuple[Pet, Task, datetime]]:
		"""Return all scheduler entries ordered by time."""
		return self.sort_by_time()

	def get_all_tasks(self) -> list[Task]:
		"""Return all tasks available through this scheduler."""
		return self.owner.get_all_tasks()

	def get_pending_tasks(self) -> list[Task]:
		"""Return all incomplete tasks available through this scheduler."""
		return self.owner.get_pending_tasks()

	def filter_tasks(self, completed: bool | None = None, pet_name: str | None = None) -> list[Task]:
		"""Return tasks filtered by optional completion status and pet name.

		If neither filter is provided, all tasks across all pets are returned.
		"""
		normalized_pet_name = pet_name.lower() if pet_name is not None else None
		matching_pets = [
			pet
			for pet in self.owner.pets
			if normalized_pet_name is None or pet.name.lower() == normalized_pet_name
		]
		return [
			task
			for pet in matching_pets
			for task in pet.tasks
			if completed is None or task.completed is completed
		]

	def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
		"""Return all tasks for the specified pet."""
		if pet not in self.owner.pets:
			raise ValueError("Pet does not belong to this scheduler's owner")
		return pet.get_tasks()

	def get_pending_tasks_for_pet(self, pet: Pet) -> list[Task]:
		"""Return all incomplete tasks for the specified pet."""
		if pet not in self.owner.pets:
			raise ValueError("Pet does not belong to this scheduler's owner")
		return pet.get_pending_tasks()

	def get_scheduled_entries_for_pet(self, pet: Pet) -> list[tuple[Pet, Task, datetime]]:
		"""Return scheduled entries for one pet ordered by time."""
		if pet not in self.owner.pets:
			raise ValueError("Pet does not belong to this scheduler's owner")
		pet_entries = [entry for entry in self.entries if entry[0] is pet]
		return self.sort_by_time(pet_entries)

	def get_upcoming_entries(self, from_date: datetime | None = None) -> list[tuple[Pet, Task, datetime]]:
		"""Return scheduled entries from the given date onward."""
		if from_date is None:
			from_date = datetime.now()
		upcoming = [entry for entry in self.entries if entry[2] >= from_date]
		return self.sort_by_time(upcoming)