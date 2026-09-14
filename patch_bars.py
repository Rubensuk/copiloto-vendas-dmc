import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update PDV-level bars
    old_pdv = r"let pct_int = meta_int > 0 \? \(real_int \/ meta_int \* 100\) : 0;\s*let pct_rgb = meta_rgb > 0 \? \(real_rgb \/ meta_rgb \* 100\) : 0;\s*let pct_300 = meta_300 > 0 \? \(real_300 \/ meta_300 \* 100\) : 0;"
    new_pdv = """let pct_int = meta_int > 0 ? (real_int / meta_int * 100) : (real_int > 0 ? 100 : 0);
                        let pct_rgb = meta_rgb > 0 ? (real_rgb / meta_rgb * 100) : (real_rgb > 0 ? 100 : 0);
                        let pct_300 = meta_300 > 0 ? (real_300 / meta_300 * 100) : (real_300 > 0 ? 100 : 0);"""
    html = re.sub(old_pdv, new_pdv, html)

    # 2. Update Aggregated (Top) bars
    old_agg = r"let pct_agg_rgb = agg\.meta_rgb > 0 \? \(agg\.real_rgb \/ agg\.meta_rgb \* 100\) : 0;\s*let pct_agg_600 = agg\.meta_600 > 0 \? \(agg\.real_600 \/ agg\.meta_600 \* 100\) : 0;\s*let pct_agg_ln  = agg\.meta_ln > 0 \? \(agg\.real_ln \/ agg\.meta_ln \* 100\) : 0;\s*let pct_agg_300 = agg\.meta_300 > 0 \? \(agg\.real_300 \/ agg\.meta_300 \* 100\) : 0;"
    new_agg = """let pct_agg_rgb = agg.meta_rgb > 0 ? (agg.real_rgb / agg.meta_rgb * 100) : (agg.real_rgb > 0 ? 100 : 0);
                let pct_agg_600 = agg.meta_600 > 0 ? (agg.real_600 / agg.meta_600 * 100) : (agg.real_600 > 0 ? 100 : 0);
                let pct_agg_ln  = agg.meta_ln > 0 ? (agg.real_ln / agg.meta_ln * 100) : (agg.real_ln > 0 ? 100 : 0);
                let pct_agg_300 = agg.meta_300 > 0 ? (agg.real_300 / agg.meta_300 * 100) : (agg.real_300 > 0 ? 100 : 0);"""
    html = re.sub(old_agg, new_agg, html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
