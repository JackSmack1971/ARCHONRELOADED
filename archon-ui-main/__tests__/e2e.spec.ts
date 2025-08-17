import { test } from '@playwright/test'

test.skip('homepage loads', async ({ page }) => {
  await page.goto('/')
})
