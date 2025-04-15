# PWA Icons

This directory contains placeholder files for the PWA icons. You need to replace these with real PNG images.

## Required Icons

You need to replace the following placeholder files with real PNG images:

- android-chrome-192x192.png (192x192 pixels)
- android-chrome-512x512.png (512x512 pixels)
- android-chrome-maskable-192x192.png (192x192 pixels)
- android-chrome-maskable-512x512.png (512x512 pixels)
- apple-touch-icon-152x152.png (152x152 pixels)
- apple-touch-icon-180x180.png (180x180 pixels)
- msapplication-icon-144x144.png (144x144 pixels)
- safari-pinned-tab.svg (SVG format)
- favicon-16x16.png (16x16 pixels)
- favicon-32x32.png (32x32 pixels)

## Generating Icons

You can use the SVG template in `icon-template.svg` as a starting point.

### Tools for generating icons:

1. **PWA Asset Generator**: https://github.com/onderceylan/pwa-asset-generator
   ```
   npx pwa-asset-generator ./icon-template.svg ./
   ```

2. **Favicon Generator**: https://realfavicongenerator.net/
   Upload your icon and download the generated package.

3. **Figma or Adobe XD**: Design your icon and export in multiple sizes.

## Icon Design Guidelines

- Use a simple, recognizable design that works at small sizes
- Ensure good contrast for visibility on different backgrounds
- For maskable icons, place important content within the safe zone (central 80%)
- Use SVG where possible for crisp rendering at all sizes
- Test icons on both light and dark backgrounds 