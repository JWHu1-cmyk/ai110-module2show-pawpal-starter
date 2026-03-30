from pawpal_system import CareTask, Pet


def test_mark_complete_changes_status():
    """Verify that calling mark_complete() changes the task's completed status."""
    task = CareTask(title="Morning walk", category="Exercise", duration_minutes=30, priority=5)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Buddy", species="Dog")
    assert len(pet.list_tasks()) == 0

    task = CareTask(title="Feed breakfast", category="Feeding", duration_minutes=10, priority=4)
    pet.add_care_task(task)
    assert len(pet.list_tasks()) == 1

    task2 = CareTask(title="Evening walk", category="Exercise", duration_minutes=20, priority=3)
    pet.add_care_task(task2)
    assert len(pet.list_tasks()) == 2
