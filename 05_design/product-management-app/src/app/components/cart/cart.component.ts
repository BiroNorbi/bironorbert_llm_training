import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CartService } from '../../services/cart.service';
import { CartItem } from '../../models/product.model';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.scss'
})
export class CartComponent implements OnInit {
  private cartService = inject(CartService);

  cartItems = this.cartService.cartItems;
  isExpanded = signal(false);

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart(): void {
    this.cartService.getCart().subscribe({
      error: (err) => {
        console.error('Error loading cart:', err);
      }
    });
  }

  toggleCart(): void {
    this.isExpanded.set(!this.isExpanded());
  }

  removeItem(cartItemId: number): void {
    this.cartService.removeFromCart(cartItemId).subscribe({
      error: (err) => {
        console.error('Error removing item from cart:', err);
        alert('Failed to remove item from cart');
      }
    });
  }

  clearCart(): void {
    if (confirm('Are you sure you want to clear the cart?')) {
      this.cartService.clearCart().subscribe({
        error: (err) => {
          console.error('Error clearing cart:', err);
          alert('Failed to clear cart');
        }
      });
    }
  }

  getTotalPrice(): number {
    return this.cartItems().reduce((sum, item) => sum + item.total_price, 0);
  }

  getTotalItems(): number {
    return this.cartItems().reduce((sum, item) => sum + item.quantity, 0);
  }
}
