import { useEffect, useState } from 'react'
import type { User } from './types'

export function UserListWithRetry() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function loadUsers() {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('https://jsonplaceholder.typicode.com/users')
      const data: User[] = await response.json()
      setUsers(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Neznámá chyba')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadUsers()
  }, [])

  return (
    <div>
      <button onClick={loadUsers} disabled={loading}>
        Znovu načíst
      </button>

      {loading && <p>Načítám...</p>}
      {!loading && error && <p>Chyba: {error}</p>}
      {!loading && !error && (
        <ul>
          {users.map((user) => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      )}
    </div>
  )
}
