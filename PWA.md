# Installable portal and offline behavior

The manifest and root service worker provide standalone installation where supported by the browser. The Install app button appears only when the browser offers installation. Other browsers may provide Add to Home Screen through their own menu. Production hosting requires HTTPS; localhost is suitable for local development.

The worker caches only the public offline fallback and its icon. It deliberately never caches authenticated pages, grades, user details, API responses or uploaded files. An unavailable server/network shows a Russian/Kazakh/English offline page. Offline submission and editing are not supported or silently queued. A successful network response, including an authentication redirect or server error, is preserved.

The public shell cache is versioned. A new worker activates after previous controlled tabs close; old AITU shell caches are removed on activation. No other application's caches are removed.

Verification: inspect Application → Manifest and Service Workers in browser developer tools. Load the site once online, enable Offline, then navigate to a course: the fallback must appear. Inspect Cache Storage: only offline.html and pwa-icon.svg may exist. Restore network and use Try again. Installation availability must be tested in the target browser; a manifest alone is not a claim that every browser offers installation.
