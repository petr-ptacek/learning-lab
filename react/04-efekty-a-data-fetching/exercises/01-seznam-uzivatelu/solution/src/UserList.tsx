import { useEffect, useState } from "react";

interface User {
  id: number;
  name: string;
}

export function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => void fetchUsers(), []);

  async function fetchUsers() {
    setLoading(true);

    try {
      const response = await fetch("https://jsonplaceholder.typicode.com/users");
      const data = (await response.json()) as User[];

      setUsers(() => data);
    } catch ( e ) {
      setError(e as Error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Uzivatele</h1>
      <button disabled={loading} onClick={ fetchUsers }>Znovu nacist</button>


      { loading && <h2>Nacitani</h2> }

      { !loading && error && <h2>Nastala chyba { error.message }</h2> }

      { !loading && !error &&
        <ul>
          { users.map(user => <li key={ user.id }>#{ user.id }&nbsp;{ user.name }</li>) }
        </ul>
      }
    </div>
  );
}