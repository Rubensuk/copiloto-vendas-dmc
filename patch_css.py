import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Define the responsive CSS we want to inject right before </style>
    responsive_css = """
        /* Score 5 Responsive Adjustments */
        .score5-top-grid, .score5-agg-grid {
            display: grid;
            gap: 0.6rem;
            margin-top: 1rem;
        }
        
        .score5-top-grid { grid-template-columns: repeat(4, 1fr); }
        .score5-agg-grid { grid-template-columns: repeat(4, 1fr); }

        .pdv-list-header {
            display: flex; 
            padding: 10px 15px; 
            background: rgba(0,0,0,0.1); 
            font-weight: bold; 
            font-size: 0.9rem; 
            border-bottom: 2px solid rgba(255,255,255,0.1); 
            margin-bottom: 5px;
        }
        .pdv-summary {
            padding: 12px 15px; 
            cursor: pointer; 
            display: flex; 
            align-items: center; 
            list-style: none;
        }

        @media (max-width: 768px) {
            .score5-top-grid, .score5-agg-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .pdv-list-header {
                font-size: 0.75rem;
                padding: 10px 5px;
            }
            .pdv-summary {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.4rem;
                padding: 10px 10px;
            }
            .pdv-summary > div {
                text-align: left !important;
                width: 100%;
            }
        }
    </style>"""

    html = html.replace('</style>', responsive_css)

    # Replace the inline grid styles for the top metrics
    old_top_grid = 'style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-top: 1rem;"'
    html = html.replace(old_top_grid, 'class="score5-top-grid"')
    
    # Replace the inline grid styles for aggregated metrics
    # Since they are identical in the HTML, we can just replace them both
    # Wait, the first replacement replaced BOTH if they were identical! Let's check how many there are.
    # We can just do a regex if needed, but let's just let it replace all occurrences.

    # Also fix the JS template string for the PDV header and summary
    # Old header:
    old_header = '<div style="display:flex; padding:10px 15px; background:var(--table-header-bg, rgba(0,0,0,0.1)); font-weight:bold; font-size:0.9rem; border-bottom:2px solid var(--table-border, rgba(255,255,255,0.1)); margin-bottom:5px;">'
    new_header = '<div class="pdv-list-header">'
    html = html.replace(old_header, new_header)

    old_summary = '<summary class="pdv-summary" style="padding: 12px 15px; cursor: pointer; display: flex; align-items: center; list-style: none;">'
    new_summary = '<summary class="pdv-summary">'
    html = html.replace(old_summary, new_summary)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
