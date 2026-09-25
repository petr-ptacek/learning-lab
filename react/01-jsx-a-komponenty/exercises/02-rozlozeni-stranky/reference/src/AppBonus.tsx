import { Alert } from './Alert'
import { PageLayout } from './PageLayout'

export default function AppBonus() {
  return (
    <PageLayout header={<h1>Blog</h1>} footer={<small>&copy; 2026</small>}>
      <Alert icon="✅">Uloženo.</Alert>
    </PageLayout>
  )
}
