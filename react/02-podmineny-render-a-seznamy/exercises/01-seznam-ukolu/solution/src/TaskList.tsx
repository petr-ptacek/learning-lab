import type { Task } from "./types";

export interface TaskListProps {
  tasks: Task[];
}

export function TaskList({ tasks }: TaskListProps) {
  if ( !tasks.length ) {
    return (
      <div>Zadne ukoly</div>
    );
  }

  const allTasksDone = tasks.every(task => task.done);

  return (
    <div>
      { allTasksDone && <h1>🎉 Vše hotovo!</h1> }

      <ul>
        {
          tasks.map(task => {
            return (
              task.done ?
              <li key={ task.id }><s>{ task.title }</s></li> :
              <li key={ task.id }>{ task.title }</li>
            );
          })
        }
      </ul>
    </div>
  );
}