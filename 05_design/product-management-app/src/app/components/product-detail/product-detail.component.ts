import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute, RouterModule } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './product-detail.component.html',
  styleUrl: './product-detail.component.scss'
})
export class ProductDetailComponent implements OnInit {
  private productService = inject(ProductService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  product = signal<Product | null>(null);
  loading = signal(true);
  error = signal<string | null>(null);

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.loadProduct(id);
    } else {
      this.error.set('Invalid product ID');
      this.loading.set(false);
    }
  }

  loadProduct(id: number): void {
    this.loading.set(true);
    this.error.set(null);
    
    this.productService.getProductById(id).subscribe({
      next: (product) => {
        this.product.set(product);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Failed to load product. Product may not exist.');
        this.loading.set(false);
        console.error('Error loading product:', err);
      }
    });
  }

  getStockStatus(stock: number): { text: string; class: string } {
    if (stock > 50) return { text: '✓ In Stock', class: 'high' };
    if (stock > 10) return { text: '⚠ Low Stock', class: 'medium' };
    if (stock > 0) return { text: '⚠ Very Low Stock', class: 'low' };
    return { text: '✗ Out of Stock', class: 'out' };
  }

  getTotalValue(): number {
    const p = this.product();
    return p ? p.price * p.stock : 0;
  }

  editProduct(): void {
    const p = this.product();
    if (p) {
      this.router.navigate(['/products/edit', p.id]);
    }
  }

  deleteProduct(): void {
    const p = this.product();
    if (!p) return;

    if (confirm(`Are you sure you want to delete "${p.name}"?`)) {
      this.productService.deleteProduct(p.id).subscribe({
        next: () => {
          this.router.navigate(['/products']);
        },
        error: (err) => {
          alert('Failed to delete product. Please try again.');
          console.error('Error deleting product:', err);
        }
      });
    }
  }

  goBack(): void {
    this.router.navigate(['/products']);
  }
}
