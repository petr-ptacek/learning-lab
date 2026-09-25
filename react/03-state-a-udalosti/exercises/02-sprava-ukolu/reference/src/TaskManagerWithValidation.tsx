import { useState, type ChangeEvent, type FormEvent } from 'react'
import type { Task } from './types'
import { TaskItem } from './TaskManager'

export function TaskManagerWithValidation() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState('')

  const canAdd = title.trim().length > 0

  function handleTitleChange(e: ChangeEvent<HTMLInputElement>) {
    setTitle(e.target.value)
  }

  function handleAdd(e: FormEvent) {
    e.preventDefault()

    if (!canAdd) {
      return
    }

    const newTask: Task = { id: crypto.randomUUID(), title: title.trim(), done: false }
    setTasks((tasks) => [...tasks, newTask])
    setTitle('')
  }

  function handleToggleDone(id: string) {
    setTasks((tasks) => tasks.map((task) => (task.id === id ? { ...task, done: !task.done } : task)))
  }

  function handleDelete(id: string) {
    setTasks((tasks) => tasks.filter((task) => task.id !== id))
  }

  return (
    <div>
      <form onSubmit={handleAdd}>
        <input value={title} onChange={handleTitleChange} />
        <button type="submit" disabled={!canAdd}>
          Přidat
        </button>
      </form>

      {tasks.length === 0 ? (
        <p>Žádné úkoly.</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <TaskItem key={task.id} task={task} onToggleDone={handleToggleDone} onDelete={handleDelete} />
          ))}
        </ul>
      )}
    </div>
  )
}
