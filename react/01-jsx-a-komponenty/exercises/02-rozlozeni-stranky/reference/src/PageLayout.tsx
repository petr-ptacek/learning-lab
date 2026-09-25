interface PageLayoutProps {
  header: React.ReactNode
  children: React.ReactNode
  footer: React.ReactNode
}

export function PageLayout({ header, children, footer }: PageLayoutProps) {
  return (
    <div>
      <header>{header}</header>
      <main>{children}</main>
      <footer>{footer}</footer>
    </div>
  )
}
