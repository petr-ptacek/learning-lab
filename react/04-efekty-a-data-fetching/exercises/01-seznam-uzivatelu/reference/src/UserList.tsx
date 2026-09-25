import { useEffect, useState } from 'react'
import type { User } from './types'

export function UserList() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let ignore = false

    async function loadUsers() {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch('https://jsonplaceholder.typicode.com/users')
        const data: User[] = await response.json()
        if (!ignore) setUsers(data)
      } catch (err) {
        if (!ignore) setError(err instanceof Error ? err.message : 'Neznámá chyba')
      } finally {
        if (!ignore) setLoading(false)
      }
    }

    loadUsers()

    return () => {
      ignore = true
    }
  }, [])

  if (loading) return <p>Načítám...</p>
  if (error) return <p>Chyba: {error}</p>

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
