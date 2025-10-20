export interface Product {
  id: number;
  name: string;
  price: number;
  description: string | null;
  stock: number;
}

export interface ProductCreate {
  name: string;
  price: number;
  description?: string | null;
  stock?: number;
}

export interface ProductUpdate {
  name?: string;
  price?: number;
  description?: string | null;
  stock?: number;
}

export interface CartItem {
  id: number;
  product_id: number;
  product_name: string;
  product_price: number;
  quantity: number;
  total_price: number;
}

export interface AddToCart {
  product_id: number;
  quantity: number;
}

