export type Product = {
  id: string;
  name: string;
  inStock: boolean;
}

export type Category = {
  id: string;
  name: string;
  products: Product[];
}