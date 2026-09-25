import { TaskList, type Task } from './TaskList'

const tasks: Task[] = [
  { id: '1', title: 'Nakoupit', done: false },
  { id: '2', title: 'Uklidit', done: true },
]

export default function App() {
  return <TaskList tasks={tasks} />
}
