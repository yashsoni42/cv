#!/usr/bin/env python3
"""
LinkedIn Posts Scraper
Scrapes all posts from a given LinkedIn profile URL using session cookies.
"""

import json
import requests
import pandas as pd
import time
import re
from urllib.parse import urlparse, quote
from datetime import datetime
from typing import Dict, List, Optional


class LinkedInScraper:
    """Scraper for LinkedIn posts using authenticated session cookies."""

    def __init__(self, cookies_file: str):
        """
        Initialize the scraper with session cookies.

        Args:
            cookies_file: Path to JSON file containing session cookies
        """
        self.session = requests.Session()
        self.load_cookies(cookies_file)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/vnd.linkedin.normalized+json+2.1',
            'Accept-Language': 'en-US,en;q=0.9',
            'x-li-lang': 'en_US',
            'x-restli-protocol-version': '2.0.0',
            'csrf-token': self.get_csrf_token()
        }

    def load_cookies(self, cookies_file: str):
        """Load cookies from JSON file into session."""
        with open(cookies_file, 'r') as f:
            cookies_data = json.load(f)

        # Handle both cookie array format and dict format
        if isinstance(cookies_data, list):
            for cookie in cookies_data:
                self.session.cookies.set(
                    cookie.get('name'),
                    cookie.get('value'),
                    domain=cookie.get('domain', '.linkedin.com'),
                    path=cookie.get('path', '/')
                )
        elif isinstance(cookies_data, dict):
            for name, value in cookies_data.items():
                self.session.cookies.set(name, value, domain='.linkedin.com')

    def get_csrf_token(self) -> str:
        """Extract CSRF token from cookies."""
        return self.session.cookies.get('JSESSIONID', '').strip('"')

    def extract_profile_id(self, profile_url: str) -> str:
        """
        Extract profile identifier from LinkedIn URL.

        Args:
            profile_url: LinkedIn profile URL (e.g., https://www.linkedin.com/in/username/)

        Returns:
            Profile identifier/username
        """
        # Extract username from URL patterns like:
        # https://www.linkedin.com/in/username/
        # https://linkedin.com/in/username
        match = re.search(r'/in/([^/]+)/?', profile_url)
        if match:
            return match.group(1)
        raise ValueError(f"Could not extract profile ID from URL: {profile_url}")

    def get_profile_urn(self, profile_id: str) -> Optional[str]:
        """
        Get the profile URN from profile ID.

        Args:
            profile_id: LinkedIn profile identifier (username)

        Returns:
            Profile URN needed for API calls
        """
        try:
            url = f"https://www.linkedin.com/voyager/api/identity/profiles/{profile_id}/profileView"
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            # Extract profile URN
            if 'profile' in data:
                profile_urn = data['profile'].get('entityUrn', '')
                return profile_urn

            return None
        except Exception as e:
            print(f"Error getting profile URN: {e}")
            return None

    def fetch_posts(self, profile_url: str, max_posts: int = 100) -> List[Dict]:
        """
        Fetch all posts from a LinkedIn profile.

        Args:
            profile_url: LinkedIn profile URL
            max_posts: Maximum number of posts to fetch

        Returns:
            List of post dictionaries
        """
        profile_id = self.extract_profile_id(profile_url)
        print(f"Fetching posts for profile: {profile_id}")

        posts = []
        start = 0
        count = 20  # Posts per request

        while len(posts) < max_posts:
            try:
                # LinkedIn Voyager API endpoint for profile posts
                url = (
                    f"https://www.linkedin.com/voyager/api/identity/profileUpdatesV2"
                    f"?count={count}"
                    f"&moduleKey=PROFILE_TOP_CARD"
                    f"&numComments=0"
                    f"&numLikes=0"
                    f"&q=memberShareFeed"
                    f"&start={start}"
                    f"&profileUrn=urn:li:fsd_profile:{profile_id}"
                )

                response = self.session.get(url, headers=self.headers)

                if response.status_code == 404:
                    print(f"Profile not found or no more posts available.")
                    break

                response.raise_for_status()
                data = response.json()

                # Extract posts from response
                elements = data.get('elements', [])

                if not elements:
                    print("No more posts found.")
                    break

                for element in elements:
                    post_data = self.parse_post(element)
                    if post_data:
                        posts.append(post_data)

                print(f"Fetched {len(posts)} posts so far...")

                # Check if there are more posts
                paging = data.get('paging', {})
                if not paging.get('links', []):
                    break

                start += count
                time.sleep(1)  # Rate limiting

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print("Rate limited. Waiting 60 seconds...")
                    time.sleep(60)
                else:
                    print(f"HTTP Error: {e}")
                    break
            except Exception as e:
                print(f"Error fetching posts: {e}")
                break

        print(f"Total posts fetched: {len(posts)}")
        return posts[:max_posts]

    def parse_post(self, element: Dict) -> Optional[Dict]:
        """
        Parse a single post element from API response.

        Args:
            element: Post element from API response

        Returns:
            Dictionary containing post data
        """
        try:
            # Navigate through the nested structure
            update = element.get('value', {})

            # Get share/post content
            share = update.get('updateMetadata', {}).get('update', {})

            # Extract post URN and ID
            share_urn = share.get('*updateMetadata', '')

            # Get commentary (post text)
            commentary = share.get('commentary', {})
            post_text = commentary.get('text', {}).get('text', '') if isinstance(commentary, dict) else ''

            # Get timestamp
            created_time = update.get('created', {}).get('time', 0)
            post_date = datetime.fromtimestamp(created_time / 1000) if created_time else None

            # Get engagement metrics
            social_detail = share.get('socialDetail', {})
            likes_count = social_detail.get('totalSocialActivityCounts', {}).get('numLikes', 0)
            comments_count = social_detail.get('totalSocialActivityCounts', {}).get('numComments', 0)
            shares_count = social_detail.get('totalSocialActivityCounts', {}).get('numShares', 0)

            # Get post URL
            post_url = share.get('permalink', '')

            return {
                'post_id': share_urn,
                'post_url': post_url,
                'text': post_text,
                'posted_date': post_date.strftime('%Y-%m-%d %H:%M:%S') if post_date else '',
                'likes': likes_count,
                'comments': comments_count,
                'shares': shares_count,
                'total_engagement': likes_count + comments_count + shares_count
            }

        except Exception as e:
            print(f"Error parsing post: {e}")
            return None

    def export_to_csv(self, posts: List[Dict], output_file: str = 'linkedin_posts.csv'):
        """
        Export posts to CSV file.

        Args:
            posts: List of post dictionaries
            output_file: Output CSV filename
        """
        df = pd.DataFrame(posts)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Exported {len(posts)} posts to {output_file}")
        return df

    def export_to_excel(self, posts: List[Dict], output_file: str = 'linkedin_posts.xlsx'):
        """
        Export posts to Excel file.

        Args:
            posts: List of post dictionaries
            output_file: Output Excel filename
        """
        df = pd.DataFrame(posts)
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Exported {len(posts)} posts to {output_file}")
        return df


def main():
    """Main function to run the scraper."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python linkedin_scraper.py <cookies_file.json> <profile_url> [max_posts]")
        print("Example: python linkedin_scraper.py cookies.json https://www.linkedin.com/in/username/ 100")
        sys.exit(1)

    cookies_file = sys.argv[1]
    profile_url = sys.argv[2]
    max_posts = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    # Initialize scraper
    scraper = LinkedInScraper(cookies_file)

    # Fetch posts
    posts = scraper.fetch_posts(profile_url, max_posts)

    if not posts:
        print("No posts found or unable to fetch posts.")
        return

    # Export to CSV
    df = scraper.export_to_csv(posts)

    # Also export to Excel
    try:
        scraper.export_to_excel(posts)
    except Exception as e:
        print(f"Could not export to Excel: {e}")

    # Display summary
    print("\n" + "="*50)
    print("POSTS SUMMARY")
    print("="*50)
    print(df.to_string(max_colwidth=50))
    print("\n" + "="*50)
    print(f"Total Posts: {len(posts)}")
    print(f"Total Likes: {df['likes'].sum()}")
    print(f"Total Comments: {df['comments'].sum()}")
    print(f"Total Shares: {df['shares'].sum()}")
    print(f"Average Engagement: {df['total_engagement'].mean():.2f}")


if __name__ == '__main__':
    main()
