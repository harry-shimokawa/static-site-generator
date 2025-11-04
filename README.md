# Static Site Generator

A custom-built static site generator written in Python that converts Markdown content into fully-featured HTML websites. This project demonstrates the complete pipeline from raw markdown files to a live website deployed on GitHub Pages.

## 🌟 Features

- **Markdown to HTML Conversion**: Complete support for all standard markdown syntax
- **Template System**: HTML templates with placeholder replacement
- **Recursive Page Generation**: Automatically processes entire directory structures
- **Static Asset Management**: Copies and manages CSS, images, and other static files
- **GitHub Pages Deployment**: Built-in support for subdirectory hosting
- **Inline Markdown Support**: Bold, italic, code, links, images, blockquotes
- **Block-level Elements**: Headers, paragraphs, lists (ordered/unordered), code blocks

## 🚀 Live Demo

Visit the deployed site: **[Tolkien Fan Club](https://harry-shimokawa.github.io/static-site-generator/)**

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.6 or higher
- Git (for deployment)

### Local Development
```bash
# Clone the repository
git clone https://github.com/harry-shimokawa/static-site-generator.git
cd static-site-generator

# Run the generator locally
python3 src/main.py

# Start local server for testing
python3 -m http.server 8888 -d docs
```

## 📁 Project Structure

```
static-site-generator/
├── src/                    # Source code
│   ├── main.py            # Main application entry point
│   ├── htmlnode.py        # HTML node classes and tree structure
│   ├── textnode.py        # Text node classes and markdown parsing
│   └── markdown.py        # Markdown processing and conversion
├── content/               # Markdown content files
│   ├── index.md          # Homepage content
│   ├── contact/          # Contact page
│   └── blog/             # Blog posts directory
├── static/               # Static assets (CSS, images)
├── docs/                 # Generated HTML files (for GitHub Pages)
├── template.html         # HTML template
├── build.sh             # Production build script
└── main.sh              # Development build script
```

## 📝 Usage

### Local Development
```bash
# Generate site for local development
python3 src/main.py

# Start local server
python3 -m http.server 8888 -d docs
```

### Production Build
```bash
# Build for GitHub Pages deployment
./build.sh
```

### Adding Content
1. Create markdown files in the `content/` directory
2. Add any images to `static/images/`
3. Run the generator to build HTML files
4. The generator maintains directory structure automatically

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
./test.sh

# Individual test suites
python3 -m unittest src/test_htmlnode.py
python3 -m unittest src/test_textnode.py  
python3 -m unittest src/test_markdown.py
```

**Test Coverage**: 99+ tests covering all functionality

## 🔧 Technical Implementation

### Core Components

1. **HTMLNode System** (`htmlnode.py`)
   - Base HTMLNode class for tree structure
   - LeafNode for content elements (text, images, etc.)
   - ParentNode for container elements (divs, lists, etc.)

2. **TextNode System** (`textnode.py`)
   - TextNode class representing inline markdown elements
   - TextType enum for different content types
   - Conversion functions to HTMLNode objects

3. **Markdown Processing** (`markdown.py`)
   - Block-level parsing (headers, paragraphs, lists, etc.)
   - Inline parsing (bold, italic, links, code, images)
   - Regex-based link and image extraction
   - Recursive text processing pipeline

### Key Algorithms

- **Delimiter Splitting**: Processes markdown delimiters (`**`, `_`, `` ` ``)
- **Block Type Detection**: Identifies 6 block types (paragraph, heading, code, quote, unordered_list, ordered_list)
- **Recursive Generation**: Crawls content directories and maintains structure
- **Template Processing**: Replaces placeholders with dynamic content

## 🌐 Deployment

### GitHub Pages Setup

1. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Set source to "Deploy from a branch"
   - Select branch: `main`, folder: `/ (root)`

2. **Build for Production**:
   ```bash
   ./build.sh
   git add docs/
   git commit -m "Deploy site"
   git push origin main
   ```

3. **Custom Domain** (optional):
   - Add CNAME file to docs/ directory
   - Configure DNS settings

### Basepath Configuration

The generator supports configurable basepaths for subdirectory hosting:

```bash
# Local development (root path)
python3 src/main.py

# GitHub Pages (subdirectory)
python3 src/main.py "/static-site-generator/"
```

## 📚 Example Content

The included demo site features:
- **Homepage**: Overview with navigation
- **Blog Posts**: Multiple articles about Tolkien's works
- **Contact Page**: Author information
- **Rich Content**: Headers, lists, quotes, code blocks, images, links

## 🤝 Contributing

This project was built as part of the [Boot.dev](https://www.boot.dev) "Build a Static Site Generator" course. Feel free to:

- Fork the repository
- Submit pull requests
- Report issues
- Suggest improvements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Learning Outcomes

This project demonstrates proficiency in:
- **Python Programming**: Object-oriented design, file I/O, regex processing
- **Web Development**: HTML generation, CSS integration, static site concepts
- **Software Engineering**: Testing, documentation, project structure
- **DevOps**: Git workflow, automated deployment, CI/CD concepts
- **Text Processing**: Markdown parsing, template systems, recursive algorithms

## 🙋‍♂️ Author

Built by Harry Shimokawa as part of the Boot.dev curriculum.

- **GitHub**: [@harry-shimokawa](https://github.com/harry-shimokawa)
- **Live Demo**: [Tolkien Fan Club](https://harry-shimokawa.github.io/static-site-generator/)

---

*Generated with a custom static site generator - because sometimes you need to build the tools to build the thing!* 🛠️