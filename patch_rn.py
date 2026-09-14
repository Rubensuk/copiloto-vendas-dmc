import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Define exactly the target section to replace
    # We will use a regex to capture everything from <select id="select-rn-code" ...> up to </select>
    
    target_pattern = r'(<select id="select-rn-code"[^>]*>).*?(</select>)'
    
    replacement = r'''\1
                            <!-- Série 100 -->
                            <option value="111">111</option>
                            <option value="112">112</option>
                            <option value="113">113</option>
                            <option value="115">115</option>
                            <option value="116">116</option>
                            <option value="117">117</option>
                            <option value="118">118</option>
                            <option value="119">119</option>
                            <option value="120">120</option>
                            <option value="121">121</option>
                            <!-- Série 200 -->
                            <option value="211">211</option>
                            <option value="212">212</option>
                            <option value="217">217</option>
                            <option value="218">218</option>
                            <option value="220">220</option>
                            <option value="222">222</option>
                            <!-- Série 300 -->
                            <option value="311" selected>311</option>
                            <option value="312">312</option>
                            <option value="313">313</option>
                            <option value="314">314</option>
                            <option value="315">315</option>
                            <option value="316">316</option>
                            <option value="317">317</option>
                            <option value="318">318</option>
                            <option value="319">319</option>
                        \2'''

    # Perform the substitution, re.DOTALL is important so .*? matches newlines
    new_html = re.sub(target_pattern, replacement, html, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

if __name__ == '__main__':
    patch()
