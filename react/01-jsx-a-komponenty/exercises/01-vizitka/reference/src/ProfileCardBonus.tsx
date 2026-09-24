interface ProfileCardProps {
  name: string
  role: string
  children: React.ReactNode
}

export function ProfileCard({ name, role, children }: ProfileCardProps) {
  return (
    <div>
      <p>{name}</p>
      <p>{role}</p>
      {children}
    </div>
  )
}

interface ContactInfoProps {
  email: string
}

export function ContactInfo({ email }: ContactInfoProps) {
  return <p>{email}</p>
}
