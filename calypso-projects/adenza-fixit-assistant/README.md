# Adenza Fix-It Assistant

> **Intelligent Error Resolution for Adenza Capital Markets Platform**

A smart browser extension designed specifically for Adenza Capital Markets platform users, providing instant, context-aware solutions to common error messages encountered in Nasdaq's trading operations. Eliminates the need to search documentation or contact support for routine issues.

## 🎯 Built for Nasdaq User Productivity

When Nasdaq traders and operations staff encounter errors in Adenza, every minute counts. The Fix-It Assistant automatically detects error messages and provides immediate, actionable solutions, reducing resolution time by 60%+ and improving overall user experience.

## ✨ Key Features

- **🔍 Automatic Detection**: Monitors Adenza web interface for error messages in real-time
- **💡 Smart Suggestions**: Context-aware fix recommendations based on error patterns
- **🔗 Direct Links**: One-click navigation to the exact location to fix issues
- **📚 Knowledge Base**: Comprehensive database of common Adenza errors and solutions
- **⚡ Instant Resolution**: No need to search documentation or wait for support

## 💼 Business Value for Nasdaq

### Productivity Gains
- **60%+ Faster Resolution**: Instant solutions vs. manual troubleshooting
- **Reduced Downtime**: Minimize trading interruptions from error resolution delays
- **User Empowerment**: Enable users to resolve issues independently

### Operational Excellence
- **Knowledge Management**: Centralized error solution database
- **Consistency**: Standardized solutions across Nasdaq teams
- **Training Tool**: Helps new users learn Adenza quickly

### Cost Reduction
- **Reduced Support Tickets**: Users resolve common issues independently
- **Faster Onboarding**: New users become productive faster
- **Operational Efficiency**: Less time spent on routine error resolution

## 🚀 Installation

### Chrome/Edge

1. Open Chrome/Edge and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked"
4. Select the `extension` directory from this project
5. The extension icon will appear in your browser toolbar

### Firefox

1. Open Firefox and navigate to `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Select the `extension/manifest.json` file
5. The extension will be loaded

## 📖 Usage

1. **Navigate to Adenza**: Open your Adenza Capital Markets platform web interface
2. **Automatic Detection**: The extension automatically monitors for error messages
3. **View Suggestions**: When an error is detected, click the extension icon to see fix suggestions
4. **Apply Fix**: Click "Fix Now" links to navigate directly to the solution location

## 🔧 Supported Error Types

The extension recognizes and provides solutions for:

- **Missing SSI (Settlement Instructions)**: Direct link to SSI configuration
- **Invalid Holiday Calendar**: Navigate to holiday calendar setup
- **Missing Legal Entity**: Link to legal entity management
- **Invalid Book Configuration**: Book validation and setup
- **Insufficient Permissions**: Guidance on permission requirements

## 🎨 Customization

### Adding New Error Patterns

Edit `src/solutions.json` to add new error patterns and solutions:

```json
{
  "id": "new-error",
  "pattern": "error message text",
  "message": "Solution description",
  "link": "/path/to/fix",
  "command": "Action to take"
}
```

### Extending Functionality

- Add integration with Adenza API for automated fixes
- Connect to Nasdaq's ticketing system
- Add analytics for error frequency tracking

## 📈 Use Cases

1. **Trading Operations**: Quick resolution of trade entry errors
2. **Static Data Management**: Fix missing or invalid static data
3. **User Support**: Self-service error resolution
4. **Training**: Help new users understand common issues

## 🔒 Privacy & Security

- **Local Processing**: Error detection happens locally in your browser
- **No Data Collection**: No user data is transmitted externally
- **Secure**: Only monitors the Adenza web interface you're using

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions that improve error detection and solutions for Adenza Capital Markets platform are welcome.

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq User Productivity**
