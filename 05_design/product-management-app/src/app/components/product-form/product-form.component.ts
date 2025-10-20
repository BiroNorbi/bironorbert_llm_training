import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, ActivatedRoute, RouterModule } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-product-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './product-form.component.html',
  styleUrl: './product-form.component.scss'
})
export class ProductFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private productService = inject(ProductService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  productForm: FormGroup;
  isEditMode = signal(false);
  productId: number | null = null;
  loading = signal(false);
  submitting = signal(false);
  error = signal<string | null>(null);
  product = signal<Product | null>(null);

  constructor() {
    this.productForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      price: [null, [Validators.required, Validators.min(0.01)]],
      description: [''],
      stock: [null, [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode.set(true);
      this.productId = Number(id);
      this.loadProduct(this.productId);
    }
  }

  loadProduct(id: number): void {
    this.loading.set(true);
    this.productService.getProductById(id).subscribe({
      next: (product) => {
        this.product.set(product);
        this.productForm.reset({
          name: product.name,
          price: product.price,
          description: product.description || '',
          stock: product.stock
        });
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Failed to load product');
        this.loading.set(false);
        console.error('Error loading product:', err);
      }
    });
  }

  onSubmit(): void {
    // Trigger validation
    this.productForm.markAllAsTouched();
    
    if (this.productForm.invalid) {
      return;
    }

    this.submitting.set(true);
    this.error.set(null);

    const formValue = this.productForm.value;
    const productData = {
      name: formValue.name,
      price: Number(formValue.price),
      description: formValue.description || null,
      stock: Number(formValue.stock)
    };

    const operation = this.isEditMode()
      ? this.productService.updateProduct(this.productId!, productData)
      : this.productService.createProduct(productData);

    operation.subscribe({
      next: (product) => {
        this.submitting.set(false);
        this.router.navigate(['/products', product.id]);
      },
      error: (err) => {
        this.error.set(this.isEditMode() 
          ? 'Failed to update product. Please try again.' 
          : 'Failed to create product. Please try again.');
        this.submitting.set(false);
        console.error('Error saving product:', err);
      }
    });
  }

  onCancel(): void {
    if (this.productForm.dirty) {
      if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
        this.goBack();
      }
    } else {
      this.goBack();
    }
  }

  goBack(): void {
    if (this.isEditMode() && this.productId) {
      this.router.navigate(['/products', this.productId]);
    } else {
      this.router.navigate(['/products']);
    }
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();
    });
  }

  getFieldError(fieldName: string): string | null {
    const control = this.productForm.get(fieldName);
    if (control?.touched && control?.invalid) {
      if (control.errors?.['required']) {
        return 'This field is required';
      }
      if (control.errors?.['minLength']) {
        return `Minimum length is ${control.errors?.['minLength'].requiredLength}`;
      }
      if (control.errors?.['min']) {
        return `Minimum value is ${control.errors?.['min'].min}`;
      }
    }
    return null;
  }
}
