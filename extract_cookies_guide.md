# How to Extract LinkedIn Session Cookies

This guide will help you extract your LinkedIn session cookies to use with the scraper.

## Why Do I Need Cookies?

LinkedIn requires authentication to access profile data. Instead of using your username and password directly (which is less secure and against LinkedIn's terms), we use session cookies - the same ones your browser uses when you're logged in.

## Step-by-Step Guide

### For Chrome/Edge Users

1. **Log in to LinkedIn**
   - Go to https://www.linkedin.com
   - Log in with your credentials

2. **Open Developer Tools**
   - Press `F12` on your keyboard, OR
   - Right-click anywhere on the page and select "Inspect", OR
   - Click the three dots menu → More tools → Developer tools

3. **Navigate to Cookies**
   - Click on the "Application" tab at the top of Developer Tools
   - In the left sidebar, expand "Storage" → "Cookies"
   - Click on "https://www.linkedin.com"

4. **Find Important Cookies**
   You'll see a table with many cookies. Look for these important ones:
   - **li_at** - This is the most important authentication cookie
   - **JSESSIONID** - CSRF token (often has quotes around it)
   - **li_a** - Additional auth token

5. **Copy Cookie Values**
   - Click on each cookie name
   - The "Value" field will show the cookie value
   - Double-click the value to select it, then copy (Ctrl+C / Cmd+C)

6. **Create cookies.json File**
   Create a file named `cookies.json` with this format:

```json
{
  "li_at": "paste_your_li_at_value_here",
  "JSESSIONID": "paste_your_jsessionid_value_here",
  "li_a": "paste_your_li_a_value_here"
}
```

**Important Notes:**
- Remove any quotes from the JSESSIONID value if present
- The li_at value is usually very long (100+ characters)
- Keep this file secure - it gives access to your LinkedIn account!

### For Firefox Users

1. **Log in to LinkedIn**
   - Go to https://www.linkedin.com
   - Log in with your credentials

2. **Open Developer Tools**
   - Press `F12` on your keyboard, OR
   - Right-click and select "Inspect Element"

3. **Navigate to Storage**
   - Click on the "Storage" tab
   - Expand "Cookies" in the left sidebar
   - Click on "https://www.linkedin.com"

4. **Copy Cookies**
   - Find and copy the same cookies mentioned above: `li_at`, `JSESSIONID`, `li_a`

5. **Create cookies.json**
   - Use the same JSON format as shown for Chrome

### Using Browser Extensions (Easier Method)

#### Chrome Extension: "EditThisCookie"

1. Install "EditThisCookie" from Chrome Web Store
2. Log in to LinkedIn
3. Click the extension icon
4. Click "Export" button
5. Save as `cookies.json`
6. You may need to convert the format - the extension exports in a different format

#### Alternative: "Get cookies.txt LOCALLY"

1. Install "Get cookies.txt LOCALLY" extension
2. Log in to LinkedIn
3. Click the extension icon while on linkedin.com
4. It will download a cookies.txt file
5. You'll need to convert this to JSON format

## Verifying Your Cookies

Your `cookies.json` should look like this:

```json
{
  "li_at": "AQEDATdm8FcBh0SkAAABjxXxX...(very long string)...xyzabc123",
  "JSESSIONID": "ajax:1234567890123456789",
  "li_a": "AQJ2PTEmc..."
}
```

**Check:**
- ✅ Valid JSON format (no syntax errors)
- ✅ All three cookies present
- ✅ No quotes around the actual cookie values (except the JSON structure)
- ✅ li_at value is very long (typically 100+ characters)

## Security Best Practices

1. **Never share your cookies.json file**
   - It's like sharing your password
   - Anyone with these cookies can access your LinkedIn account

2. **Keep it in .gitignore**
   - Don't commit it to Git repositories
   - The provided .gitignore already excludes it

3. **Cookies expire**
   - LinkedIn cookies typically last a few weeks
   - If the scraper stops working, get fresh cookies

4. **Use a secure location**
   - Store cookies.json in a secure folder
   - Delete it when you're done scraping

## Troubleshooting

### "Cookie not found" error
- Make sure you're logged in to LinkedIn
- Refresh the cookies list in Developer Tools
- Try logging out and back in to LinkedIn

### Cookies not working with scraper
- Verify the JSON format is correct
- Check there are no extra spaces or line breaks in cookie values
- Get fresh cookies (log out and back in to LinkedIn)
- Make sure you copied the entire cookie value

### JSESSIONID has quotes
LinkedIn's JSESSIONID often looks like: `"ajax:1234567890123456789"`

Remove the quotes when copying to cookies.json:
```json
{
  "JSESSIONID": "ajax:1234567890123456789"
}
```

NOT:
```json
{
  "JSESSIONID": "\"ajax:1234567890123456789\""
}
```

## Quick Test

After creating your `cookies.json`, test if it works:

```bash
python linkedin_scraper.py cookies.json "https://www.linkedin.com/in/your-profile/" 5
```

This will try to fetch just 5 posts. If successful, you're ready to scrape!

## Need Help?

If you're still having trouble:
1. Double-check the JSON format at https://jsonlint.com
2. Verify you copied the complete cookie values
3. Make sure you're logged in to LinkedIn in the same browser
4. Try using incognito/private mode and logging in fresh
