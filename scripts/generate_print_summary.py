#!/usr/bin/env python3
"""
Generate Print-Ready HTML Summary from Executive Summary
Creates a formatted HTML document suitable for printing to PDF or inclusion in binders
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def generate_print_html():
    """Generate print-ready HTML from executive summary"""

    # Paths
    root_dir = Path(__file__).parent.parent
    exec_summary = root_dir / 'EXECUTIVE_SUMMARY.md'
    output_html = root_dir / 'docs' / 'ONE_PAGE_SUMMARY.html'

    # Ensure docs directory exists
    output_html.parent.mkdir(exist_ok=True)

    # Read markdown
    print(f"Reading: {exec_summary}")
    with open(exec_summary, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert markdown to HTML
    try:
        import markdown
        md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
        html_body = md.convert(content)
    except ImportError:
        print("Note: markdown package not installed, using basic conversion")
        # Simple markdown conversion
        html_body = content.replace('\n\n', '</p><p>')
        html_body = f'<p>{html_body}</p>'
        # Convert headers
        for i in range(6, 0, -1):
            html_body = html_body.replace('#' * i + ' ', f'</p><h{i}>')
            html_body = html_body.replace('\n', f'</h{i}><p>')

    # Build complete HTML document with print-optimized CSS
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capstone Hub - Executive Summary</title>
    <style>
        /* Print-optimized styles */
        @page {{
            size: letter;
            margin: 0.5in 0.75in;
        }}

        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #000;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.5in;
            background: white;
        }}

        /* Header styling */
        .metadata {{
            font-size: 9pt;
            text-align: center;
            margin-bottom: 12pt;
            color: #444;
            border-bottom: 1px solid #ccc;
            padding-bottom: 6pt;
        }}

        h1 {{
            font-size: 18pt;
            font-weight: bold;
            margin-top: 0;
            margin-bottom: 12pt;
            text-align: center;
            border-bottom: 2px solid #000;
            padding-bottom: 6pt;
        }}

        h2 {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 14pt;
            margin-bottom: 6pt;
            border-bottom: 1px solid #666;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 11pt;
            font-weight: bold;
            margin-top: 10pt;
            margin-bottom: 4pt;
            page-break-after: avoid;
        }}

        h4 {{
            font-size: 10pt;
            font-weight: bold;
            margin-top: 8pt;
            margin-bottom: 3pt;
        }}

        p {{
            margin: 4pt 0;
            text-align: justify;
        }}

        ul, ol {{
            margin: 6pt 0;
            padding-left: 24pt;
        }}

        li {{
            margin: 3pt 0;
        }}

        /* Code and pre blocks */
        code {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 9pt;
            background-color: #f5f5f5;
            padding: 2pt 4pt;
            border: 1px solid #ddd;
        }}

        pre {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 8pt;
            background-color: #f5f5f5;
            padding: 8pt;
            margin: 8pt 0;
            border: 1px solid #ccc;
            white-space: pre-wrap;
            word-wrap: break-word;
            page-break-inside: avoid;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 9pt;
            margin: 8pt 0;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #666;
            padding: 4pt 6pt;
            text-align: left;
        }}

        th {{
            background-color: #e0e0e0;
            font-weight: bold;
        }}

        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 1px solid #999;
            margin: 12pt 0;
        }}

        /* Strong and emphasis */
        strong {{
            font-weight: bold;
        }}

        em {{
            font-style: italic;
        }}

        /* Links */
        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        /* Blockquotes */
        blockquote {{
            margin: 8pt 24pt;
            padding: 6pt 12pt;
            border-left: 3px solid #ccc;
            background-color: #f9f9f9;
            font-style: italic;
        }}

        /* Footer */
        .footer {{
            font-size: 8pt;
            text-align: center;
            margin-top: 20pt;
            padding-top: 10pt;
            border-top: 1px solid #ccc;
            color: #666;
        }}

        /* Print-specific adjustments */
        @media print {{
            body {{
                padding: 0;
                font-size: 9pt;
            }}

            h1 {{
                page-break-after: avoid;
            }}

            h2, h3, h4 {{
                page-break-after: avoid;
            }}

            table, pre, blockquote {{
                page-break-inside: avoid;
            }}

            a {{
                color: #000;
                text-decoration: none;
            }}

            .no-print {{
                display: none;
            }}
        }}

        /* Screen-only: print button */
        @media screen {{
            .print-button {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 10px 20px;
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}

            .print-button:hover {{
                background-color: #0052a3;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-button no-print" onclick="window.print()">🖨️ Print to PDF</button>

    <div class="metadata">
        <strong>Harry L. Stearns, Inc.</strong> | MBA Capstone Project | University of Oregon<br>
        Generated: {datetime.now().strftime('%B %d, %Y')} | Version: v0.36.3 | Status: Production-Ready
    </div>

    {html_body}

    <div class="footer">
        <hr>
        <p>
            <strong>Repository:</strong> https://github.com/yourusername/capstone-hub<br>
            <strong>Live Demo:</strong> https://mabbottmbacapstone.up.railway.app<br>
            <strong>Contact:</strong> security@hlstearns.local | privacy@hlstearns.local
        </p>
        <p style="margin-top: 8pt; font-style: italic;">
            This document is intended for academic review and evaluation. For complete technical documentation,
            see the repository README.md, SECURITY.md, and PRIVACY.md files.
        </p>
    </div>
</body>
</html>
"""

    # Write HTML file
    print(f"Generating: {output_html}")
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"\n[OK] Print-ready HTML generated successfully!")
    print(f"  Location: {output_html}")
    print(f"  Size: {output_html.stat().st_size / 1024:.1f} KB")
    print(f"\nTo create PDF:")
    print(f"  1. Open {output_html.name} in your browser")
    print(f"  2. Click 'Print to PDF' button (or Ctrl+P / Cmd+P)")
    print(f"  3. Save as docs/ONE_PAGE_SUMMARY.pdf")
    print(f"\nAlternatively, open in browser and use File -> Print -> Save as PDF")


def main():
    """Main entry point"""
    print("="*70)
    print("Capstone Hub - Print Summary Generator")
    print("="*70)
    print()

    try:
        generate_print_html()
        return 0
    except Exception as e:
        print(f"\n[ERROR] Error generating HTML: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
