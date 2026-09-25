import { useState, type ChangeEvent, type FormEvent } from 'react'
import type { Task } from './types'

interface TaskItemProps {
  task: Task
  onToggleDone: (id: string) => void
  onDelete: (id: string) => void
}

export function TaskItem({ task, onToggleDone, onDelete }: TaskItemProps) {
  return (
    <li>
      {task.done ? <s>{task.title}</s> : task.title}
      <button onClick={() => onToggleDone(task.id)}>{task.done ? 'Vrátit' : 'Hotovo'}</button>
      <button onClick={() => onDelete(task.id)}>Smazat</button>
    </li>
  )
}

export function TaskManager() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState('')

  function handleTitleChange(e: ChangeEvent<HTMLInputElement>) {
    setTitle(e.target.value)
  }

  function handleAdd(e: FormEvent) {
    e.preventDefault()

    const newTask: Task = { id: crypto.randomUUID(), title, done: false }
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
        <button type="submit">Přidat</button>
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
