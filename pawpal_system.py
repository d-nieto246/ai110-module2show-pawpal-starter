from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Task:
	type: str
	description: str
	frequency: str

	def edit(self, new_data: dict[str, Any]) -> None:
		pass

	def get_details(self) -> str:
		pass


@dataclass
class Pet:
	name: str
	species: str
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def edit_task(self, task: Task, new_data: dict[str, Any]) -> None:
		pass

	def remove_task(self, task: Task) -> None:
		pass

	def get_tasks(self) -> list[Task]:
		pass


@dataclass
class Owner:
	name: str
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		pass

	def remove_pet(self, pet: Pet) -> None:
		pass

	def get_pets(self) -> list[Pet]:
		pass


@dataclass
class ScheduleEntry:
	task: Task
	date_time: datetime


@dataclass
class Schedule:
	owner: Owner
	entries: list[ScheduleEntry] = field(default_factory=list)

	def add_entry(self, task: Task, date_time: datetime) -> None:
		pass

	def remove_entry(self, entry: ScheduleEntry) -> None:
		pass

	def view_schedule(self) -> list[ScheduleEntry]:
		pass
