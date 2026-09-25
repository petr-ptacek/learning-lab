import { CatalogList, type Category } from './CatalogList'
import { CatalogOverview } from './CatalogOverview'

const categories: Category[] = [
  {
    id: '1',
    name: 'Nápoje',
    products: [
      { id: 'p1', name: 'Voda', inStock: true },
      { id: 'p2', name: 'Limonáda', inStock: false },
    ],
  },
]

export default function AppBonus() {
  return (
    <>
      <CatalogOverview categories={categories} />
      <CatalogList categories={categories} />
    </>
  )
}
