# Frontend Application Guidelines for AI Agents

## Project Overview

This is a modern React 18 frontend application built with TypeScript 5.x and Vite as the build tool. The application follows current best practices for performance, type safety, and developer experience.

### Core Technologies
- **Frontend Framework**: React 18.x with concurrent features
- **Build Tool**: Vite 6.0+ with modern bundling
- **Language**: TypeScript 5.x with strict mode
- **Package Manager**: pnpm (preferred) / npm / yarn
- **Styling**: CSS Modules / Styled Components / Tailwind CSS
- **Testing**: Vitest + React Testing Library

## Development Workflow and Git Requirements

### Git Workflow Constraints
- **CRITICAL**: Do not create new branches - work on current branch only
- **REQUIRED**: Commit all changes using `git add . && git commit -m "message"`
- **REQUIRED**: Check git status after changes to ensure clean worktree
- **FORBIDDEN**: Do not modify or amend existing commits
- **FORBIDDEN**: Do not use git rebase or force push

### File Citations Required
- Use `F:file_path†L<line>` format when referencing specific code lines
- Include terminal output citations using chunk_id for command results
- Cite modified files in summaries using `F:` format
- Always reference AGENTS.md files when following guidelines

### Development Commands
```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Run tests
pnpm test

# Build for production
pnpm build

# Lint code
pnpm lint

# Format code
pnpm format

# Type check
pnpm type-check
```

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── atoms/         # Basic components (Button, Input, etc.)
│   │   ├── molecules/     # Composite components (Form, Card, etc.)
│   │   └── organisms/     # Complex components (Header, Sidebar, etc.)
│   ├── pages/             # Route components
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API integration and external services
│   ├── store/             # State management (Redux/Zustand/Context)
│   ├── types/             # TypeScript type definitions
│   ├── utils/             # Utility functions
│   ├── styles/            # Global styles and theme
│   ├── assets/            # Static assets (images, icons, etc.)
│   ├── App.tsx            # Main application component
│   ├── main.tsx           # Application entry point
│   └── vite-env.d.ts      # Vite environment types
├── public/                # Static public assets
├── dist/                  # Build output (generated)
├── tests/                 # Test files and utilities
├── vite.config.ts         # Vite configuration
├── tsconfig.json          # TypeScript configuration
├── package.json           # Dependencies and scripts
└── README.md              # Project documentation
```

## React 18 Development Guidelines

### Component Architecture
- **REQUIRED**: Use functional components with hooks exclusively
- **REQUIRED**: Apply React 18's `createRoot` API (not legacy `ReactDOM.render`)
- **REQUIRED**: Implement proper TypeScript interfaces for all component props
- **PREFERRED**: Use composition over inheritance patterns
- **PREFERRED**: Keep components small and focused on single responsibility

```tsx
// ✅ Correct - Modern React 18 component pattern
import React from 'react';

interface ButtonProps {
  variant: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  variant, 
  children, 
  onClick, 
  disabled = false 
}) => {
  return (
    <button 
      className={`btn btn--${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
```

### React 18 Concurrent Features
- **Use `useTransition`** for non-urgent state updates to maintain UI responsiveness
- **Use `useDeferredValue`** for expensive rendering operations
- **Use `useId`** for generating unique IDs (accessibility and SSR)
- **Use `useSyncExternalStore`** for external state management integration

```tsx
// ✅ Correct - Using concurrent features
import { useTransition, useDeferredValue, useId } from 'react';

function SearchResults({ query }: { query: string }) {
  const [isPending, startTransition] = useTransition();
  const deferredQuery = useDeferredValue(query);
  const searchId = useId();

  const handleSearch = (newQuery: string) => {
    startTransition(() => {
      // Non-urgent update
      setResults(performSearch(deferredQuery));
    });
  };

  return (
    <div>
      <input id={searchId} onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <Results data={results} />
    </div>
  );
}
```

### Performance Optimization
- **Use `React.memo`** selectively for expensive components
- **Use `useCallback`** for functions passed to memoized components
- **Use `useMemo`** for expensive calculations only
- **Implement code splitting** with `React.lazy` and `Suspense`
- **Use virtualization** for lists with 100+ items

### State Management
- **Local state**: Use `useState` for component-specific state
- **Complex state**: Use `useReducer` for complex state logic
- **Global state**: Use Context API, Redux Toolkit, or Zustand
- **Server state**: Use React Query or SWR for API data

## TypeScript 5.x Configuration

### TypeScript Configuration (tsconfig.json)
```json
{
  "compilerOptions": {
    "target": "ES2023",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true
  },
  "include": ["src", "tests"],
  "exclude": ["node_modules", "dist"]
}
```

### TypeScript Best Practices
- **REQUIRED**: Enable strict mode with all strict flags
- **REQUIRED**: Use type-only imports with `import type`
- **REQUIRED**: Define explicit interfaces for all props and API responses
- **PREFERRED**: Use template literal types for string manipulation
- **PREFERRED**: Leverage utility types: `Pick`, `Omit`, `Partial`, `Required`

```tsx
// ✅ Correct - TypeScript best practices
import type { User, ApiResponse } from './types';
import { validateUser } from './utils';

interface UserCardProps {
  user: User;
  onEdit: (userId: string) => void;
  onDelete: (userId: string) => void;
}

type UserActions = Pick<UserCardProps, 'onEdit' | 'onDelete'>;

export const UserCard: React.FC<UserCardProps> = ({ user, onEdit, onDelete }) => {
  // Component implementation
};
```

### TypeScript 5.x Features Usage
- **Use new decorators syntax** (not experimental decorators)
- **Use `const` type parameters** for better literal type inference
- **Use `satisfies` operator** for type validation without assertion
- **Use import attributes** with `with { type: 'json' }` syntax

## Vite Configuration

### Vite Setup (vite.config.ts)
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    target: 'esnext',
    sourcemap: false,
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return 'vendor'
          }
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@hooks': path.resolve(__dirname, 'src/hooks'),
      '@utils': path.resolve(__dirname, 'src/utils')
    }
  }
})
```

### Vite Best Practices
- **REQUIRED**: Use absolute paths for all file operations
- **REQUIRED**: Configure proxy for API calls to avoid CORS issues
- **PREFERRED**: Use path aliases sparingly to avoid complex resolution
- **PREFERRED**: Enable code splitting with manual chunks for better caching

### Asset Handling
```typescript
// ✅ Correct - Asset import patterns
import logoUrl from './logo.svg?url'          // Gets URL to asset
import logoRaw from './logo.svg?raw'          // Gets raw content
import logoInline from './logo.svg?inline'    // Inlines as data URL

// Dynamic imports
const getAsset = (name: string) => new URL(`./assets/${name}`, import.meta.url)
```

## Code Style and Conventions

### Naming Conventions
- **Files**: kebab-case.tsx (e.g., `user-profile.tsx`)
- **Components**: PascalCase (e.g., `UserProfile`)
- **Interfaces**: PascalCase with descriptive names (e.g., `UserProfileProps`)
- **Types**: PascalCase (e.g., `UserRole`)
- **Functions/Variables**: camelCase (e.g., `getUserData`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)

### Import Organization
```tsx
// ✅ Correct - Import order
// 1. React and React-related
import React, { useState, useEffect } from 'react';

// 2. Third-party libraries
import { motion } from 'framer-motion';

// 3. Internal utilities and hooks
import { useApi } from '@hooks/useApi';
import { formatDate } from '@utils/date';

// 4. Type imports (separate)
import type { User, ApiResponse } from '@/types';

// 5. Local component imports
import { Button } from './Button';
```

### Component Structure Template
```tsx
// ✅ Correct - Component template
import React from 'react';
import type { ComponentProps } from './types';

interface Props extends ComponentProps {
  // Additional props
}

export const ComponentName: React.FC<Props> = ({ 
  prop1, 
  prop2,
  ...otherProps 
}) => {
  // 1. Hooks
  const [state, setState] = useState('');
  
  // 2. Derived state
  const computedValue = useMemo(() => {
    return expensiveCalculation(state);
  }, [state]);
  
  // 3. Event handlers
  const handleClick = useCallback(() => {
    // Handler logic
  }, []);
  
  // 4. Effects
  useEffect(() => {
    // Side effects
  }, []);
  
  // 5. Render
  return (
    <div className="component-name">
      {/* JSX content */}
    </div>
  );
};
```

## Testing Standards

### Testing Setup
- **Framework**: Vitest for unit and integration tests
- **React Testing**: React Testing Library for component testing
- **Coverage**: Maintain >80% test coverage
- **Mocking**: Mock external dependencies and APIs

```tsx
// ✅ Correct - Test pattern
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('should display user information correctly', async () => {
    // Arrange
    const mockUser = { id: '1', name: 'John Doe', email: 'john@example.com' };
    const mockOnEdit = vi.fn();
    
    // Act
    render(<UserProfile user={mockUser} onEdit={mockOnEdit} />);
    
    // Assert
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });
});
```

## Security and Performance

### Security Guidelines
- **Validate all user inputs** before processing
- **Sanitize data** before rendering in JSX
- **Use HTTPS** for all external API calls
- **Never expose sensitive data** in client-side code
- **Implement proper authentication** token handling

### Performance Guidelines
- **Code splitting**: Use dynamic imports for routes and large components
- **Bundle analysis**: Monitor bundle size and optimize chunks
- **Image optimization**: Use proper formats and lazy loading
- **Avoid inline styles**: Use CSS classes for better performance

```tsx
// ✅ Correct - Performance optimizations
import { lazy, Suspense } from 'react';

// Code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));

// Memoized component
const ExpensiveComponent = React.memo(({ data }) => {
  const processedData = useMemo(() => 
    data.filter(item => item.active).sort((a, b) => b.priority - a.priority),
    [data]
  );
  
  return <List data={processedData} />;
});

// Usage with Suspense
function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Dashboard />
    </Suspense>
  );
}
```

## Environment Configuration

### Environment Variables
- **Client-side variables**: Use `VITE_` prefix for variables exposed to client
- **Validation**: Check required environment variables at build time
- **Security**: Never expose API keys or secrets with `VITE_` prefix

```typescript
// ✅ Correct - Environment handling
if (!import.meta.env.VITE_API_URL) {
  throw new Error('VITE_API_URL is required');
}

// Type-safe environment variables
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_TITLE: string;
  readonly MODE: string;
  readonly DEV: boolean;
  readonly PROD: boolean;
}
```

## Error Handling and Debugging

### Error Boundaries
```tsx
// ✅ Correct - Error boundary implementation
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong.</div>;
    }
    return this.props.children;
  }
}
```

### Async Error Handling
```tsx
// ✅ Correct - Async operation with error handling
const useApiData = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await api.getData();
        if (!cancelled) {
          setData(result);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      cancelled = true;
    };
  }, []);

  return { data, error, loading };
};
```

## Code Quality and Linting

### ESLint Configuration
- **Extends**: React, TypeScript, and accessibility rules
- **Rules**: Enforce consistent code style and catch common issues
- **Plugins**: React hooks, accessibility, and import rules

### Prettier Configuration
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
```

## Build and Deployment

### Production Build
```bash
# Build for production
pnpm build

# Preview production build
pnpm preview

# Analyze bundle size
pnpm build --analyze
```

### Deployment Checklist
- [ ] Environment variables configured correctly
- [ ] API endpoints updated for production
- [ ] Bundle size optimized and analyzed
- [ ] Error tracking configured
- [ ] Performance monitoring enabled
- [ ] HTTPS enabled
- [ ] Security headers configured

## Common Issues and Solutions

### Hydration Mismatches (SSR)
```tsx
// ✅ Correct - Handling SSR hydration
function ClientOnlyComponent() {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;
  
  return <div>{new Date().toLocaleString()}</div>;
}
```

### Memory Leaks Prevention
```tsx
// ✅ Correct - Cleanup subscriptions
useEffect(() => {
  const subscription = eventEmitter.subscribe(handleEvent);
  
  return () => {
    subscription.unsubscribe();
  };
}, []);
```

## Pull Request Guidelines

### PR Title Format
`[ComponentName/Feature] Brief description of changes`

### PR Description Template
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project conventions
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] No new TypeScript errors
- [ ] Bundle size impact verified
```

## Additional Resources

- [React 18 Documentation](https://react.dev/)
- [TypeScript 5.x Handbook](https://www.typescriptlang.org/docs/)
- [Vite Documentation](https://vitejs.dev/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Vitest Documentation](https://vitest.dev/)

## Key Reminders for AI Agents

1. **Always commit changes** after modifications using git
2. **Follow React 18 concurrent patterns** for performance
3. **Use TypeScript strict mode** with proper typing
4. **Implement proper error boundaries** and cleanup
5. **Test all changes** with appropriate test coverage
6. **Cite files and terminal outputs** as required
7. **Check AGENTS.md compliance** for all modifications
8. **Use absolute paths** for reliable file operations
