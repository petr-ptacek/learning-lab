import { CatalogList }   from "./CatalogList.tsx";
import type { Category } from "./types";

export default function App() {
  const categoriesStore: Category[][] = [
    [{
      id: "1",
      name: "Nápoje",
      products: [{ id: "p1", name: "Voda", inStock: true }, { id: "p2", name: "Limonáda", inStock: false }]
    }],
    [
      { id: "1", name: "Nápoje", products: [] },
      { id: "2", name: "Pečivo", products: [{ id: "p3", name: "Chleba", inStock: true }] }
    ],
    []
  ];


  return (
    <div>
      {
        categoriesStore.map((categories, idx) =>
          <CatalogList key={ idx } categories={ categories } />
        )
      }
    </div>
  );
}