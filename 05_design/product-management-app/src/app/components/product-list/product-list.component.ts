import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { CartService } from '../../services/cart.service';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './product-list.component.html',
  styleUrl: './product-list.component.scss'
})
export class ProductListComponent implements OnInit {
  private productService = inject(ProductService);
  private cartService = inject(CartService);
  private router = inject(Router);

  products = signal<Product[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.loading.set(true);
    this.error.set(null);
    
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.products.set(products);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Failed to load products. Please try again.');
        this.loading.set(false);
        console.error('Error loading products:', err);
      }
    });
  }

  getStockStatus(stock: number): 'high' | 'medium' | 'low' {
    if (stock > 50) return 'high';
    if (stock > 10) return 'medium';
    return 'low';
  }

  deleteProduct(id: number, event: Event): void {
    event.stopPropagation();
    
    if (confirm('Are you sure you want to delete this product?')) {
      this.productService.deleteProduct(id).subscribe({
        next: () => {
          this.loadProducts();
        },
        error: (err) => {
          alert('Failed to delete product. Please try again.');
          console.error('Error deleting product:', err);
        }
      });
    }
  }

  editProduct(id: number, event: Event): void {
    event.stopPropagation();
    this.router.navigate(['/products/edit', id]);
  }

  viewProduct(id: number): void {
    this.router.navigate(['/products', id]);
  }

  addNewProduct(): void {
    this.router.navigate(['/products/new']);
  }

  addToCart(productId: number, event: Event): void {
    event.stopPropagation();
    
    this.cartService.addToCart({ product_id: productId, quantity: 1 }).subscribe({
      next: (cartItem) => {
        console.log('Product added to cart successfully:', cartItem);
        // Refresh products to show updated stock
        this.loadProducts();
      },
      error: (err) => {
        console.error('Error adding to cart:', err);
        console.error('Error status:', err.status);
        console.error('Error message:', err.error);
        
        if (err.status === 400) {
          alert(err.error.detail || 'Not enough stock available');
        } else if (err.status === 404) {
          alert('Product not found');
        } else {
          alert(`Failed to add product to cart: ${err.error?.detail || err.message || 'Unknown error'}`);
        }
      }
    });
  }
}
