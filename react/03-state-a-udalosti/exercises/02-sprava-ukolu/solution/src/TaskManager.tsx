import { type ChangeEvent, useState } from "react";
import type { Task }                  from "./types";

export interface TaskManagerProps {
}

interface TaskItemProps {
  task: Task;

  onDelete(id: string): void;

  onToggleDone(id: string): void;
}

function TaskItem(props: TaskItemProps) {

  const toggleDone = () => {
    props.onToggleDone(props.task.id);
  };

  const handleDelete = () => {
    props.onDelete(props.task.id);
  };

  return (
    <li style={ { display: "inline-flex", gap: "4px" } }>
      {
        !props.task.done ? <div>{ props.task.title }</div> : <del>{ props.task.title }</del>
      }

      <button onClick={ handleDelete }>Smazat</button>

      <button onClick={ toggleDone }>
        {
          props.task.done ?
          "Vratit" :
          "Hotovo"
        }
      </button>
    </li>
  );
}

export function TaskManager(_props: TaskManagerProps) {
  const [title, setTitle] = useState<string>("");
  const [tasks, setTasks] = useState<Task[]>([]);

  const enableAddTask = !!title.trim().length;

  const handleSetTitle = (e: ChangeEvent<HTMLInputElement>) => {
    setTitle(e.target.value);
  };

  const handleTaskRemove = (id: string) => {
    setTasks(tasks => tasks.filter(t => t.id !== id));
  };

  const handleToggleDone = (id: string) => {
    setTasks(
      tasks => tasks.map(t => {
          if ( t.id === id ) {
            return {
              ...t,
              done: !t.done
            };
          }

          return t;
        }
      )
    );
  };

  const handleTaskAdd = () => {
    if ( !enableAddTask ) {
      return;
    }

    setTitle("");
    setTasks(tasks => {
      const task: Task = {
        id: window.crypto.randomUUID(),
        done: false,
        title: title.trim()
      };

      return [...tasks, task];
    });
  };

  return (
    <form
      onSubmit={ (e) => {
        e.preventDefault();
        handleTaskAdd();
      } }>
      <div>
        <input type="text" value={ title } onChange={ handleSetTitle } />
        <button disabled={ !enableAddTask } type="submit">Add task</button>
      </div>

      <h1>Tasks</h1>

      {
        !tasks.length ?
        "Zadne ukoly" :
        <ul style={ { display: "flex", flexDirection: "column", gap: "4px" } }>
          {
            tasks.map(
              t =>
                <TaskItem
                  key={ t.id }
                  task={ t }
                  onDelete={ handleTaskRemove }
                  onToggleDone={ handleToggleDone }
                />
            )
          }
        </ul>
      }


    </form>
  );
}