# Full Stack Web Architecture & Performance

## Server-Side Rendering (SSR) vs Client-Side Rendering (CSR)
Client-Side Rendering (CSR) downloads a minimal HTML shell and executes JavaScript in the browser to build the DOM dynamically (e.g. standard React SPA). Advantages include fast subsequent page transitions and rich interactive client states. Disadvantages include slow initial page load (FCP/LCP) and potential SEO crawling challenges.

Server-Side Rendering (SSR) executes component rendering logic on the server per request, generating fully populated HTML before sending it to the browser. Advantages include immediate content visibility, superior SEO, and lower device processing requirements. Next.js leverages SSR, Static Site Generation (SSG), and Incremental Static Regeneration (ISR) to balance performance.

## State Management & Re-rendering Optimization
React applications manage local component state, context state, and global store states. To prevent unnecessary component re-renders:
1. Memoize expensive sub-trees using React.memo.
2. Memoize calculated callbacks and values using useCallback and useMemo.
3. Keep state co-located near the components that consume it rather than pushing all transient UI state into global stores.
