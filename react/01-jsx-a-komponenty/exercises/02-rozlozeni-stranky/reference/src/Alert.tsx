interface AlertProps {
  icon: React.ReactNode
  children: React.ReactNode
}

export function Alert({ icon, children }: AlertProps) {
  return (
    <div>
      {icon} {children}
    </div>
  )
}
