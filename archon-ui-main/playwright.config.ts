import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: '__tests__',
  testMatch: /.*\.spec\.ts/,
  timeout: 30000,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    timeout: 120000,
    reuseExistingServer: !process.env.CI,
  },
})
