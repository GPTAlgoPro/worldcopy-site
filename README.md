# WorldCopy / 摹界

Public product and support website for WorldCopy on iOS and macOS.

**Website:** https://gptalgopro.github.io/worldcopy-site/

| Page | 简体中文 | English |
|---|---|---|
| Overview | [产品介绍](https://gptalgopro.github.io/worldcopy-site/) | [Overview](https://gptalgopro.github.io/worldcopy-site/en/) |
| iOS | [iOS 版](https://gptalgopro.github.io/worldcopy-site/ios/) | [For iOS](https://gptalgopro.github.io/worldcopy-site/en/ios/) |
| Mac | [Mac 版](https://gptalgopro.github.io/worldcopy-site/mac/) | [For Mac](https://gptalgopro.github.io/worldcopy-site/en/mac/) |
| Support | [支持](https://gptalgopro.github.io/worldcopy-site/support/) | [Support](https://gptalgopro.github.io/worldcopy-site/en/support/) |
| Privacy | [隐私政策](https://gptalgopro.github.io/worldcopy-site/privacy/) | [Privacy](https://gptalgopro.github.io/worldcopy-site/en/privacy/) |
| Terms | [使用条款](https://gptalgopro.github.io/worldcopy-site/terms/) | [Terms](https://gptalgopro.github.io/worldcopy-site/en/terms/) |

Support: **sunkai4u@gmail.com**. Do not post private models or photos in public issues.

## Maintain the site

This repository contains only public website materials, not the app source or model weights.
The website is a static documentation site. It has no login, payment processing, analytics, third-party fonts or embedded media.

- Edit product content in `scripts/build.py`, policy source in `content/`, and design in `style.css`.
- Update `content/site.json` for the support contact.
- Run `python3 scripts/build.py` then `python3 scripts/verify.py`.
- Commit generated HTML together with its source. GitHub Pages publishes the root of `main`.
- Keep App Store availability accurate. Do not add download badges before the apps are available.
- Update privacy, purchase disclosures and support documentation when the shipped app changes.

## Brand icon

The website uses the complete light-appearance icon render (`assets/worldcopy-icon-light.png`), including the glass background and lens halo. The app asset catalog fallback PNG is not the composited app icon.

## Screenshots

Captured on September 20, 2026 from the actual WorldCopy 1.24.2 (227) apps:

- `assets/ios-model-zh.png`: physical iPhone, captured through QuickTime screen preview; AI-generated rabbit figurine, Chinese interface.
- `assets/mac-model-zh.png`: native Mac app, AI-generated ram figurine preview.
- `assets/mac-library-zh.png`: native Mac app, actual model library.

Images show actual app output; no generative image editing was applied. They are website illustrations, not the final App Store screenshot submission set. English pages identify the Chinese UI shown in screenshots. Replace the corresponding assets and rebuild to update the website.

The screenshots do not constitute a benchmark or guarantee of results. Device, input, resources and feature availability affect results.

## Rights

Website text, branding and screenshots © 2026 Kai Sun. Third-party license texts retain their original terms and notices. A public repository does not grant a license to redistribute app models or weights.
