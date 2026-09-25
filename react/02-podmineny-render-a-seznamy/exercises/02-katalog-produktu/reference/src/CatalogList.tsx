export interface Product {
  id: string
  name: string
  inStock: boolean
}

export interface Category {
  id: string
  name: string
  products: Product[]
}

interface CatalogListProps {
  categories: Category[]
}

export function CatalogList({ categories }: CatalogListProps) {
  if (categories.length === 0) {
    return <p>Žádné kategorie.</p>
  }

  return (
    <div>
      {categories.map((category) => (
        <section key={category.id}>
          <h2>{category.name}</h2>
          {category.products.length === 0 ? (
            <p>Žádné produkty v této kategorii.</p>
          ) : (
            <ul>
              {category.products.map((product) => (
                <li key={product.id}>
                  {product.inStock ? product.name : <s>{product.name} (vyprodáno)</s>}
                </li>
              ))}
            </ul>
          )}
        </section>
      ))}
    </div>
  )
}
