# How to Add Screenshot to README

## Steps:

1. **Take a Screenshot** of your application running at http://localhost:3000

2. **Save the screenshot** as `screenshot.png` in the root directory of your project

3. **The README is already configured** to display the screenshot automatically

## Alternative: If you want to use a different filename

If your screenshot has a different name (e.g., `interface.png`), update the README.md line:

```markdown
![Hyderabad House Price Predictor](screenshot.png)
```

Change `screenshot.png` to your filename.

## Recommended Screenshot Size

- **Width**: 1200-1400 pixels
- **Format**: PNG or JPG
- **Quality**: High resolution for better display on GitHub

## What to Capture

Take a screenshot showing:
- The header with statistics
- The property details form
- Preferably with some fields filled in
- The overall grey and cream color scheme

## After Adding Screenshot

Commit and push:
```bash
git add screenshot.png README.md
git commit -m "Add interface screenshot to README"
git push
```

The screenshot will automatically appear in your GitHub repository!
