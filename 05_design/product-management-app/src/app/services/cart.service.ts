import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, switchMap, catchError, of } from 'rxjs';
import { CartItem, AddToCart } from '../models/product.model';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost/cart';

  // Signal to track cart items count
  cartItemsCount = signal<number>(0);
  cartItems = signal<CartItem[]>([]);

  getCart(): Observable<CartItem[]> {
    return this.http.get<CartItem[]>(this.apiUrl).pipe(
      tap(items => {
        this.cartItems.set(items);
        this.cartItemsCount.set(items.reduce((sum, item) => sum + item.quantity, 0));
      })
    );
  }

  addToCart(data: AddToCart): Observable<CartItem> {
    return this.http.post<CartItem>(`${this.apiUrl}/add`, data).pipe(
      tap({
        next: (cartItem) => {
          console.log('Cart item added:', cartItem);
          // Update local cart state immediately
          const currentItems = this.cartItems();
          const existingIndex = currentItems.findIndex(item => item.product_id === cartItem.product_id);
          
          if (existingIndex >= 0) {
            // Update existing item
            const updatedItems = [...currentItems];
            updatedItems[existingIndex] = cartItem;
            this.cartItems.set(updatedItems);
          } else {
            // Add new item
            this.cartItems.set([...currentItems, cartItem]);
          }
          
          // Update count
          this.cartItemsCount.set(this.cartItems().reduce((sum, item) => sum + item.quantity, 0));
        },
        error: (err) => console.error('Error in addToCart:', err)
      }),
      catchError((err) => {
        console.error('Failed to add to cart:', err);
        throw err;
      })
    );
  }

  removeFromCart(cartItemId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${cartItemId}`).pipe(
      tap({
        next: () => {
          // Update local cart state immediately
          const updatedItems = this.cartItems().filter(item => item.id !== cartItemId);
          this.cartItems.set(updatedItems);
          this.cartItemsCount.set(updatedItems.reduce((sum, item) => sum + item.quantity, 0));
        },
        error: (err) => console.error('Error removing from cart:', err)
      })
    );
  }

  clearCart(): Observable<void> {
    return this.http.delete<void>(this.apiUrl).pipe(
      tap(() => {
        this.cartItems.set([]);
        this.cartItemsCount.set(0);
      })
    );
  }
}
