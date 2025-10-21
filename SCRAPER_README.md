# LinkedIn Posts Scraper

A Python-based scraper to extract all posts from a LinkedIn profile URL using authenticated session cookies.

## Features

- Authenticates using session cookies (no username/password needed)
- Fetches all posts from a given LinkedIn profile
- Extracts comprehensive post data:
  - Post text/content
  - Posted date and time
  - Likes count
  - Comments count
  - Shares count
  - Post URL
  - Total engagement metrics
- Exports data to CSV and Excel formats
- Handles pagination automatically
- Rate limiting protection
- Displays summary statistics

## Installation

1. Install Python 3.7 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Getting Your LinkedIn Session Cookies

You need to export your LinkedIn session cookies to authenticate the scraper. Here's how:

### Method 1: Using Browser Developer Tools (Chrome/Edge)

1. Log in to LinkedIn in your browser
2. Open Developer Tools (F12 or Right-click > Inspect)
3. Go to the "Application" tab (Chrome) or "Storage" tab (Firefox)
4. In the left sidebar, expand "Cookies" and click on "https://www.linkedin.com"
5. You'll see a list of cookies. You need these important ones:
   - `li_at` (most important - authentication token)
   - `JSESSIONID` (CSRF token)
   - `li_a`
   - Any other cookies present

6. Create a `cookies.json` file in one of these formats:

**Format 1 - Simple dictionary (recommended):**
```json
{
  "li_at": "your_li_at_cookie_value",
  "JSESSIONID": "your_jsessionid_value",
  "li_a": "your_li_a_value"
}
```

**Format 2 - Array format:**
```json
[
  {
    "name": "li_at",
    "value": "your_li_at_cookie_value",
    "domain": ".linkedin.com",
    "path": "/"
  },
  {
    "name": "JSESSIONID",
    "value": "your_jsessionid_value",
    "domain": ".linkedin.com",
    "path": "/"
  }
]
```

### Method 2: Using Browser Extensions

1. Install a cookie export extension:
   - Chrome: "Get cookies.txt" or "EditThisCookie"
   - Firefox: "Cookie Quick Manager"

2. Log in to LinkedIn
3. Export cookies for linkedin.com
4. Save as `cookies.json`

## Usage

### Basic Usage

```bash
python linkedin_scraper.py cookies.json "https://www.linkedin.com/in/username/" 100
```

### Parameters

1. `cookies_file.json` - Path to your cookies JSON file
2. `profile_url` - Full LinkedIn profile URL (e.g., https://www.linkedin.com/in/username/)
3. `max_posts` (optional) - Maximum number of posts to fetch (default: 100)

### Examples

Fetch 50 posts:
```bash
python linkedin_scraper.py my_cookies.json "https://www.linkedin.com/in/johndoe/" 50
```

Fetch 200 posts:
```bash
python linkedin_scraper.py session.json "https://www.linkedin.com/in/janedoe/" 200
```

## Output

The scraper generates two files:

1. **linkedin_posts.csv** - CSV file with all posts data
2. **linkedin_posts.xlsx** - Excel file with all posts data

### Output Columns

| Column | Description |
|--------|-------------|
| post_id | Unique post identifier |
| post_url | Direct URL to the post |
| text | Post content/text |
| posted_date | Date and time when posted |
| likes | Number of likes |
| comments | Number of comments |
| shares | Number of shares |
| total_engagement | Total engagement (likes + comments + shares) |

### Sample Output

```
==================================================
POSTS SUMMARY
==================================================
   post_id  post_url          text               posted_date          likes  comments  shares  total_engagement
0  urn:...  https://...      Excited to share...  2024-01-15 10:30:00   245      12       5         262
1  urn:...  https://...      Great meeting...     2024-01-10 14:20:00   180       8       3         191
...

==================================================
Total Posts: 50
Total Likes: 5420
Total Comments: 342
Total Shares: 89
Average Engagement: 117.02
```

## Programmatic Usage

You can also use the scraper as a Python module:

```python
from linkedin_scraper import LinkedInScraper

# Initialize scraper with cookies
scraper = LinkedInScraper('cookies.json')

# Fetch posts
posts = scraper.fetch_posts('https://www.linkedin.com/in/username/', max_posts=100)

# Export to CSV
df = scraper.export_to_csv(posts, 'output.csv')

# Export to Excel
scraper.export_to_excel(posts, 'output.xlsx')

# Work with pandas DataFrame
print(df.head())
print(df.describe())
```

## Troubleshooting

### "No posts found or unable to fetch posts"
- Verify your cookies are valid and not expired
- Make sure you're logged in to LinkedIn in your browser
- Re-export fresh cookies
- Check if the profile URL is correct

### "Profile not found"
- Ensure the profile URL is correct
- Check if the profile is public or you're connected with them
- Some profiles may have privacy settings that prevent scraping

### Rate Limiting
- The scraper includes automatic rate limiting (1 second between requests)
- If you hit LinkedIn's rate limits, the scraper will wait 60 seconds
- Consider reducing the number of posts or spreading requests over time

### Cookie Expiration
- LinkedIn cookies typically expire after some time
- If scraping stops working, export fresh cookies
- The `li_at` cookie is the most important one

## Important Notes

- **Respect LinkedIn's Terms of Service**: Use this tool responsibly
- **Rate Limits**: Don't make excessive requests in short periods
- **Privacy**: Only scrape public profiles or profiles you have permission to access
- **Cookie Security**: Keep your cookies file secure - it contains your session data
- **Legal**: Ensure your use case complies with applicable laws and regulations

## Limitations

- Requires valid LinkedIn session cookies
- Subject to LinkedIn's rate limiting
- May break if LinkedIn changes their API structure
- Cannot access private posts or restricted profiles
- Post text may be truncated for very long posts

## License

This tool is for educational and research purposes only.
