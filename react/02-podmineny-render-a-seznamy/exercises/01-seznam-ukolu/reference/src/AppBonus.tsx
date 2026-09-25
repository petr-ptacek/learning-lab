import { TaskList, type Task } from './TaskList'

const tasks: Task[] = [
  { id: '1', title: 'Nakoupit', done: true },
  { id: '2', title: 'Uklidit', done: true },
]

export default function AppBonus() {
  return <TaskList tasks={tasks} />
}
