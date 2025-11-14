# BrowserStack Configuration

This document explains how to set up and use BrowserStack for cross-browser testing.

## Setup

1. **Get BrowserStack Account**
   - Sign up at https://www.browserstack.com/
   - Get your username and access key from Account Settings

2. **Set Environment Variables**

   **Windows PowerShell:**
   ```powershell
   $env:BROWSERSTACK_USERNAME="your_username"
   $env:BROWSERSTACK_ACCESS_KEY="your_access_key"
   ```

   **Windows CMD:**
   ```cmd
   set BROWSERSTACK_USERNAME=your_username
   set BROWSERSTACK_ACCESS_KEY=your_access_key
   ```

   **Linux/Mac:**
   ```bash
   export BROWSERSTACK_USERNAME="your_username"
   export BROWSERSTACK_ACCESS_KEY="your_access_key"
   ```

3. **Create .env file** (Optional)
   ```
   BROWSERSTACK_USERNAME=your_username
   BROWSERSTACK_ACCESS_KEY=your_access_key
   ```

## Running Tests on BrowserStack

### Manual Execution
```powershell
python scripts/run_browserstack.py
```

### GitHub Actions
Tests automatically run on BrowserStack when pushed to main branch if credentials are configured in repository secrets:

1. Go to GitHub repository Settings → Secrets and variables → Actions
2. Add secrets:
   - `BROWSERSTACK_USERNAME`
   - `BROWSERSTACK_ACCESS_KEY`

## Browser/OS Coverage

The default configuration tests on:
- Chrome on Windows 11
- Firefox on Windows 11
- Edge on Windows 11
- Safari on macOS Ventura
- Chrome on macOS Ventura

You can modify these in `scripts/run_browserstack.py`.

## Viewing Results

- BrowserStack Dashboard: https://automate.browserstack.com/
- View live tests, recordings, logs, and screenshots
- Access detailed network logs and console output

## Notes

- Full BrowserStack integration requires Playwright support
- Local testing requires BrowserStack Local binary
- Tests use the same test suite as local execution
- All test artifacts are available in BrowserStack dashboard
