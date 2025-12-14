# Extension Troubleshooting Steps

## Issue: No popup shown when visiting phishing URLs

### Step 1: Reload the Extension

**IMPORTANT**: You must reload the extension after making changes!

1. Open Chrome and go to: `chrome://extensions/`
2. Find **"Phishing Detector"**
3. Click the **🔄 Reload** button (circular arrow icon)
4. Check that version shows **2.1.0**

### Step 2: Verify Permissions

Make sure these permissions are granted:
- ✅ Read and change all your data on all websites
- ✅ Storage
- ✅ Active Tab

If you see a warning about new permissions, click **"Allow"**

### Step 3: Check API Server

The API must be running for the extension to work:

```bash
# Check if API is responding
curl http://localhost:5000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "ml_models_loaded": true/false,
  "version": "2.0.0"
}
```

### Step 4: Test the Extension

Open Chrome DevTools Console (F12) and check for errors:

1. Go to `chrome://extensions/`
2. Find "Phishing Detector"
3. Click **"service worker"** link (under "Inspect views")
4. This opens the background script console
5. Try visiting a suspicious URL
6. Look for console messages

### Step 5: Manual Test

Try these URLs (they should trigger warnings):

**Test 1: IP Address**
```
http://192.168.1.1/paypal/login
```

**Test 2: Suspicious TLD**
```
http://test-verify.tk
```

**Test 3: Local Test File**
```
file:///c:/Users/priya/OneDrive/Desktop/PhishingModel/extension/test_phishing_page.html
```

### Step 6: Check Background Script

Open background script console:
1. `chrome://extensions/`
2. Click "service worker" under Phishing Detector
3. You should see console logs when navigating

### Common Issues

#### Issue: "service worker (inactive)"
**Solution**: Click on "service worker" to activate it, or reload the extension

#### Issue: No console logs
**Solution**: The background script might not be running. Reload the extension.

#### Issue: "Failed to fetch" error
**Solution**: 
- Make sure API server is running: `python api/app.py`
- Check API URL in extension settings
- Verify CORS is enabled

#### Issue: Warning shows but then disappears
**Solution**: This is normal - the warning should stay until you click a button

#### Issue: Extension icon not showing
**Solution**: Pin the extension to toolbar (puzzle piece icon → pin)

### Debug Mode

To see detailed logs:

1. Open background script console
2. Navigate to a suspicious URL
3. Check for these messages:
   - "Quick check found suspicious patterns"
   - "Checking URL before navigation"
   - "Showing blocking warning"

### Test with Browser Console

Open any page and paste this in console:

```javascript
chrome.runtime.sendMessage({
    action: 'checkPhishing',
    data: { url: 'http://secure-paypal-verify.tk' }
}, (response) => {
    console.log('API Response:', response);
});
```

### If Still Not Working

1. **Remove and Re-add Extension**:
   - Go to `chrome://extensions/`
   - Click "Remove" on Phishing Detector
   - Click "Load unpacked"
   - Select: `c:\Users\priya\OneDrive\Desktop\PhishingModel\extension`

2. **Check Manifest Version**:
   - Open `extension/manifest.json`
   - Verify version is "2.1.0"
   - Verify permissions include "webNavigation" and "scripting"

3. **Restart Chrome**:
   - Close all Chrome windows
   - Reopen Chrome
   - Reload extension

### Expected Behavior

When you navigate to `http://secure-paypal-verify.tk`:

1. Background script detects navigation
2. Quick check identifies suspicious TLD (.tk)
3. API call is made to check URL
4. If risk > 70, blocking warning appears
5. You see full-screen overlay with warning

### Contact Points

If warning still doesn't show:
- Check background script console for errors
- Verify API is returning high risk score
- Make sure webNavigation permission is granted
- Try with a different suspicious URL
