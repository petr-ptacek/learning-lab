import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import AppBonus from './AppBonus.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppBonus />
  </StrictMode>,
)
