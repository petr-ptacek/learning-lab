interface ProfileCardProps {
  name: string
  role: string
  email: string
}

export function ProfileCard({ name, role, email }: ProfileCardProps) {
  return (
    <div>
      <p>{name}</p>
      <p>{role}</p>
      <p>{email}</p>
    </div>
  )
}
