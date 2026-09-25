import type { Category, Product } from "./types";

export interface CatalogListProps {
  categories: Category[];
}

export function ProductItem({ product }: { product: Product }) {
  if ( !product.inStock ) {
    return (
      <li>
        <del>{ product.name }</del>
        &nbsp;(Vyprodáno)
      </li>
    );
  }

  return (
    <li>{ product.name }</li>
  );
}

export function ProductsList({ products }: { products: Product[] }) {
  return (
    <ul>
      {
        products.map(product =>
          <li key={ product.id }>{ product.name }</li>
        )
      }
    </ul>
  );
}

export function CatalogList({ categories }: CatalogListProps) {
  if ( !categories.length ) {
    return (
      <h1>Žádné kategorie.</h1>
    );
  }

  return (
    <div>
      {
        categories.map(category => {
          return (
            <div key={ category.id }>
              <h1>
                <span>{ category.name }</span>
                <span> / { category.products.length } produktu</span>
              </h1>
              {
                category.products.length > 0 ?
                <ProductsList products={ category.products } />
                                             : <h2>Žádné produkty v této kategorii.</h2>
              }
            </div>
          );
        })
      }
    </div>
  );
}