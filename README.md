# Google Ads API Setup Guide

To use the Google Ads Wrapper, you need to obtain specific credentials. Follow these steps:

## 1. Prerequisites

- A **Google Ads Manager Account** (Standard access or higher is preferred, but Test Access works for development).
- A **Google Cloud Project**.

## 2. Get Developer Token

1. Log in to your [Google Ads Manager Account](https://ads.google.com/).
2. Navigate to **Admin** > **API Center** (or Tools & Settings > Setup > API Center).
3. Copy the **Developer Token**.
   - _Note: If you have "Test Account" access, you can only make calls to Test Google Ads Accounts._

## 3. Get Client ID and Client Secret

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Select your project.
3. Navigate to **APIs & Services** > **Credentials**.
4. Click **Create Credentials** > **OAuth client ID**.
5. Application type: **Desktop app** (or Web application if you have a callback URL setup).
6. Give it a name (e.g., "GenSEO Agent").
7. Copy the **Client ID** and **Client Secret**.

## 4. Get Refresh Token

The easiest way to get a refresh token for development is using the **OAuth 2.0 Playground**:

1. Go to [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground).
2. Click the **Gear icon** (top right).
   - Check **Use your own OAuth credentials**.
   - Enter your **Client ID** and **Client Secret**.
   - Click **Close**.
3. In "Step 1 - Select & authorize APIs":
   - Input your own scope: `https://www.googleapis.com/auth/adwords`
   - Click **Authorize APIs**.
4. Log in with the Google Account that has access to the Google Ads Manager Account.
5. Click **Exchange authorization code for tokens**.
6. Copy the **Refresh Token**.

## 5. Get Customer ID

1. Log in to your Google Ads account.
2. The **Customer ID** is the 10-digit number in the top right corner (format: `123-456-7890`).
3. For the API, use the **Login Customer ID** (usually your Manager Account ID) if you are authenticating as a manager.

## 6. Update .env

Update your `.env` file with these values:

```env
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token
GOOGLE_ADS_CLIENT_ID=your_client_id
GOOGLE_ADS_CLIENT_SECRET=your_client_secret
GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token
GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890
```
