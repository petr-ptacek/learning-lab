import { Fragment } from 'react'
import type { Category } from './CatalogList'

interface CatalogOverviewProps {
  categories: Category[]
}

export function CatalogOverview({ categories }: CatalogOverviewProps) {
  if (categories.length === 0) {
    return null
  }

  return (
    <dl>
      {categories.map((category) => (
        <Fragment key={category.id}>
          <dt>{category.name}</dt>
          <dd>{category.products.length} produktů</dd>
        </Fragment>
      ))}
    </dl>
  )
}
