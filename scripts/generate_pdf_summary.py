#!/usr/bin/env python3
"""
Generate PDF Summary from Executive Summary
Creates a print-ready one-page document for academic binders
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import markdown
        from weasyprint import HTML, CSS
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("\nInstall required packages:")
        print("  pip install markdown weasyprint")
        return False


def generate_pdf():
    """Generate PDF from executive summary"""

    # Paths
    root_dir = Path(__file__).parent.parent
    exec_summary = root_dir / 'EXECUTIVE_SUMMARY.md'
    output_pdf = root_dir / 'docs' / 'ONE_PAGE_SUMMARY.pdf'

    # Ensure docs directory exists
    output_pdf.parent.mkdir(exist_ok=True)

    # Read markdown
    print(f"Reading: {exec_summary}")
    with open(exec_summary, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert to HTML with custom CSS
    import markdown
    from weasyprint import HTML, CSS

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    html_content = md.convert(content)

    # Custom CSS for print-ready formatting
    css = CSS(string="""
        @page {
            size: letter;
            margin: 0.5in 0.75in;
        }

        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 9pt;
            line-height: 1.3;
            color: #000;
        }

        h1 {
            font-size: 16pt;
            font-weight: bold;
            margin-top: 0;
            margin-bottom: 8pt;
            text-align: center;
            border-bottom: 2px solid #000;
            padding-bottom: 4pt;
        }

        h2 {
            font-size: 11pt;
            font-weight: bold;
            margin-top: 10pt;
            margin-bottom: 4pt;
            border-bottom: 1px solid #666;
        }

        h3 {
            font-size: 10pt;
            font-weight: bold;
            margin-top: 6pt;
            margin-bottom: 3pt;
        }

        p {
            margin: 3pt 0;
            text-align: justify;
        }

        ul, ol {
            margin: 3pt 0;
            padding-left: 20pt;
        }

        li {
            margin: 2pt 0;
        }

        code {
            font-family: 'Courier New', monospace;
            font-size: 8pt;
            background-color: #f5f5f5;
            padding: 1pt 3pt;
        }

        pre {
            font-family: 'Courier New', monospace;
            font-size: 7pt;
            background-color: #f5f5f5;
            padding: 4pt;
            margin: 4pt 0;
            border: 1px solid #ccc;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
            margin: 6pt 0;
        }

        th, td {
            border: 1px solid #666;
            padding: 3pt 5pt;
            text-align: left;
        }

        th {
            background-color: #e0e0e0;
            font-weight: bold;
        }

        hr {
            border: none;
            border-top: 1px solid #999;
            margin: 8pt 0;
        }

        .metadata {
            font-size: 8pt;
            text-align: center;
            margin-bottom: 8pt;
            color: #666;
        }

        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        /* Checkmarks */
        li:has(> input[type="checkbox"]:checked) {
            list-style: none;
            margin-left: -15pt;
        }

        li:has(> input[type="checkbox"]:checked)::before {
            content: "✓ ";
            font-weight: bold;
        }

        /* Print-specific adjustments */
        @media print {
            body {
                font-size: 9pt;
            }

            h1 {
                page-break-after: avoid;
            }

            h2, h3 {
                page-break-after: avoid;
            }

            pre, table {
                page-break-inside: avoid;
            }
        }
    """)

    # Build complete HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Capstone Hub - Executive Summary</title>
    </head>
    <body>
        <div class="metadata">
            Harry L. Stearns, Inc. | MBA Capstone Project | University of Oregon | October 2025
        </div>
        {html_content}
        <hr>
        <div class="metadata">
            Repository: https://github.com/yourusername/capstone-hub | Version: v0.36.3 | Status: Production-Ready
        </div>
    </body>
    </html>
    """

    # Generate PDF
    print(f"Generating: {output_pdf}")
    HTML(string=full_html).write_pdf(output_pdf, stylesheets=[css])

    print(f"\n✓ PDF generated successfully!")
    print(f"  Location: {output_pdf}")
    print(f"  Size: {output_pdf.stat().st_size / 1024:.1f} KB")
    print(f"\nReady for printing and inclusion in capstone binder.")


def main():
    """Main entry point"""
    print("="*70)
    print("Capstone Hub - PDF Summary Generator")
    print("="*70)
    print()

    if not check_dependencies():
        return 1

    try:
        generate_pdf()
        return 0
    except Exception as e:
        print(f"\n✗ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
