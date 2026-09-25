import { TaskList }  from "./TaskList.tsx";
import type { Task } from "./types";

export default function App() {
  const tasksStore: Task[][] = [
    [{ id: "1", title: "Nakoupit", done: false }, { id: "2", title: "Uklidit", done: true }],
    [{ id: "1", title: "Zaplatit účty", done: false }],
    [],
    [{ id: "1", title: "Nakoupit", done: true }, { id: "2", title: "Uklidit", done: true }]
  ];

  return (
    <div>
      {
        tasksStore.map((tasks, idx) =>
          <TaskList key={ idx } tasks={ tasks } />
        )
      }
    </div>
  );
}