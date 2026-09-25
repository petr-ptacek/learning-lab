import { PageLayout } from './PageLayout'

export default function App() {
  return (
    <PageLayout header={<h1>Blog</h1>} footer={<small>&copy; 2026</small>}>
      <p>Vítej na blogu!</p>
    </PageLayout>
  )
}
