# Product Management Application# ProductManagementApp



A modern Angular 20 application for managing products, built with standalone components and connected to a FastAPI backend.This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 20.3.6.



## Features## Development server



- 📋 **Product List**: View all products in a responsive grid layoutTo start a local development server, run:

- 🔍 **Product Details**: View detailed information about each product

- ➕ **Create Products**: Add new products with validation```bash

- ✏️ **Edit Products**: Update existing product informationng serve

- 🗑️ **Delete Products**: Remove products with confirmation```

- 🎨 **Modern UI**: Purple gradient theme with smooth animations

- 📱 **Responsive Design**: Works seamlessly on mobile, tablet, and desktopOnce the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.



## Prerequisites## Code scaffolding



- Node.js (v18 or higher)Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

- npm (v9 or higher)

- Angular CLI (`npm install -g @angular/cli`)```bash

- FastAPI backend running on `http://localhost` (see `03_python_fastapi_project`)ng generate component component-name

```

## Installation

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

1. Navigate to the project directory:

```bash```bash

cd c:\ai_training\bironorbert_llm_training\05_design\product-management-appng generate --help

``````



2. Install dependencies:## Building

```bash

npm installTo build the project run:

```

```bash

## Running the Applicationng build

```

### Start the Backend (FastAPI)

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

First, ensure the FastAPI backend is running:

```bash## Running unit tests

cd c:\ai_training\bironorbert_llm_training\03_python_fastapi_project

# Follow the backend README to start the serverTo execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

# It should be accessible at http://localhost

``````bash

ng test

### Start the Frontend (Angular)```



```bash## Running end-to-end tests

npm start

```For end-to-end (e2e) testing, run:



The application will open automatically at `http://localhost:4200````bash

ng e2e

## Available Scripts```



- `npm start` - Start the development serverAngular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

- `npm run build` - Build for production

- `npm test` - Run unit tests## Additional Resources

- `npm run watch` - Build in watch mode

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.

## Project Structure

```
src/
├── app/
│   ├── components/
│   │   ├── product-list/       # Product listing with grid view
│   │   ├── product-detail/     # Detailed product view
│   │   └── product-form/       # Create/Edit product form
│   ├── models/
│   │   └── product.model.ts    # Product interfaces
│   ├── services/
│   │   └── product.service.ts  # HTTP service for API calls
│   ├── app.config.ts           # App configuration
│   ├── app.routes.ts           # Route definitions
│   └── app.ts                  # Root component
├── styles.scss                 # Global styles
└── index.html                  # HTML entry point
```

## API Endpoints

The application connects to the following FastAPI endpoints:

- `GET /products` - Get all products
- `GET /products/{id}` - Get product by ID
- `POST /products` - Create a new product
- `PUT /products/{id}` - Update a product
- `DELETE /products/{id}` - Delete a product

## Technologies Used

- **Angular 20**: Latest Angular with standalone components
- **TypeScript 5.9**: Type-safe development
- **SCSS**: Modern CSS preprocessing
- **RxJS 7.8**: Reactive programming
- **Signals**: Angular's new reactivity system
- **Zoneless**: Improved performance without Zone.js

## Development Notes

- The app uses **standalone components** (no NgModules)
- **Signals** are used for state management
- **Zoneless** change detection for better performance
- All forms include **validation** and error handling
- **Responsive design** with mobile-first approach

## Building for Production

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## License

This project is part of the AI Training curriculum.
