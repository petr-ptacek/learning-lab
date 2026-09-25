export interface Task {
  id: string
  title: string
  done: boolean
}

interface TaskListProps {
  tasks: Task[]
}

export function TaskList({ tasks }: TaskListProps) {
  if (tasks.length === 0) {
    return <p>Žádné úkoly.</p>
  }

  const allDone = tasks.every((task) => task.done)

  return (
    <div>
      {allDone && <p>🎉 Vše hotovo!</p>}
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>{task.done ? <s>{task.title}</s> : task.title}</li>
        ))}
      </ul>
    </div>
  )
}
