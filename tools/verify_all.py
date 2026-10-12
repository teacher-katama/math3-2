import os
import re

base_dir = r"c:\hackMD製作"
md_files = [f for f in os.listdir(base_dir) if f.endswith(".md")]
print(f"Total MD files found: {len(md_files)}")

missing_links = []
missing_images = []

# Pattern that handles (下) inside markdown link URLs: [text](target.md#anchor)
# We can match [text](... .md ...) or markdown links properly
link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]*?\([^)]*\)[^)]*|\S+?\.md(?:#[^)]*)?)\)')

for md in sorted(md_files):
    filepath = os.path.join(base_dir, md)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. HTML img tags
    html_imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    for img in html_imgs:
        if img.startswith("http"):
            continue
        img_path = os.path.join(base_dir, img)
        if not os.path.exists(img_path):
            missing_images.append((md, img))

    # 2. Markdown img tags
    md_imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', content)
    for img in md_imgs:
        if img.startswith("http"):
            continue
        img_path = os.path.join(base_dir, img)
        if not os.path.exists(img_path):
            missing_images.append((md, img))

    # 3. Check markdown links
    # Let's extract all occurrences of [text](...) by scanning characters to balance parentheses
    i = 0
    while i < len(content):
        if content[i] == '[':
            # find matching ']'
            close_bracket = content.find(']', i)
            if close_bracket != -1 and close_bracket + 1 < len(content) and content[close_bracket + 1] == '(':
                # find balanced ')'
                open_paren = close_bracket + 1
                depth = 1
                j = open_paren + 1
                while j < len(content) and depth > 0:
                    if content[j] == '(':
                        depth += 1
                    elif content[j] == ')':
                        depth -= 1
                    j += 1
                if depth == 0:
                    url = content[open_paren + 1 : j - 1].strip()
                    if not url.startswith("http") and not url.startswith("#") and url != "":
                        target_file = url.split("#")[0].strip()
                        if target_file:
                            target_path = os.path.join(base_dir, target_file)
                            if not os.path.exists(target_path):
                                missing_links.append((md, url, target_file))
                    i = j
                    continue
        i += 1

print(f"Missing images count: {len(missing_images)}")
for md, img in missing_images:
    print(f"  [IMG ERROR] in {md}: {img}")

print(f"Missing links count: {len(missing_links)}")
for md, url, target in missing_links:
    print(f"  [LINK ERROR] in {md}: url='{url}' -> target='{target}'")

if not missing_images and not missing_links:
    print("SUCCESS: All links and images verified perfectly with 0 errors!")
