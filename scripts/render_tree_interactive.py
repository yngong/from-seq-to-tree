#!/usr/bin/env python3
"""
Interactive Phylogenetic Tree Renderer for Google Antigravity & Bioinformatics Tutorials.
Parses Newick trees and metadata TSV, then compiles a standalone, high-aesthetic HTML viewer.
"""

import sys
import os
import json
import csv
from Bio import Phylo

def parse_metadata(meta_path):
    metadata = {}
    if not os.path.exists(meta_path):
        return metadata
    with open(meta_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            strain = row.get('strain') or row.get('strain_name') or row.get('sample_id')
            if strain:
                metadata[strain] = row
    return metadata

def tree_to_dict(clade, metadata):
    node_id = clade.name if clade.name else ""
    meta = metadata.get(node_id, {})
    
    # Determine display group / color category
    group = meta.get('group', 'Unknown')
    if 'Root' in node_id or 'California/07/2009' in node_id:
        group = 'Root Reference'
    elif 'Vaccine' in node_id:
        group = 'Vaccine Reference'
    elif 'barcode' in node_id or 'User_Clinical_Specimen' in group:
        group = 'Clinical Specimen'
    elif 'NextstrainCladeRef' in node_id or 'Nextstrain' in group:
        group = 'Global Reference Clade'

    node_data = {
        "name": node_id,
        "branch_length": clade.branch_length if clade.branch_length is not None else 0.001,
        "confidence": clade.confidence if clade.confidence is not None else None,
        "is_leaf": clade.is_terminal(),
        "group": group,
        "metadata": meta,
        "children": [tree_to_dict(child, metadata) for child in clade.clades]
    }
    return node_data

def generate_interactive_html(tree_path, meta_path, output_html, title="Influenza A (H1N1pdm09) Phylogenetic Tree"):
    trees = list(Phylo.parse(tree_path, "newick"))
    if not trees:
        raise ValueError(f"Could not parse tree from {tree_path}")
    tree = trees[0]
    
    # Root at California/07/2009 if present
    for clade in tree.find_clades():
        if clade.name and "California/07/2009" in clade.name:
            try:
                tree.root_with_outgroup(clade)
                print(f"Successfully rooted tree on outgroup: {clade.name}")
            except Exception as e:
                print(f"Outgroup rooting skipped: {e}")
            break

    metadata = parse_metadata(meta_path)
    tree_data = tree_to_dict(tree.root, metadata)

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-cyan: #38bdf8;
            --accent-purple: #c084fc;
            --accent-emerald: #34d399;
            --accent-amber: #fbbf24;
            --accent-rose: #fb7185;
            --border-color: rgba(255, 255, 255, 0.1);
            --branch-color: #64748b;
            --node-hover: #38bdf8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}

        /* Left Sidebar */
        #sidebar {{
            width: 380px;
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            padding: 24px;
            gap: 20px;
        }}

        .logo-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(56, 189, 248, 0.12);
            color: var(--accent-cyan);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 9999px;
            padding: 4px 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            width: fit-content;
        }}

        h1 {{
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.3;
            color: #fff;
        }}

        .subtitle {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        .control-card {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .control-label {{
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }}

        input[type="text"] {{
            width: 100%;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: #fff;
            padding: 10px 12px;
            font-size: 0.85rem;
            font-family: 'JetBrains Mono', monospace;
            outline: none;
            transition: border-color 0.2s;
        }}

        input[type="text"]:focus {{
            border-color: var(--accent-cyan);
        }}

        .btn-group {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}

        button {{
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        button:hover {{
            background: var(--bg-tertiary);
            border-color: var(--accent-cyan);
            color: #fff;
        }}

        button.active {{
            background: rgba(56, 189, 248, 0.2);
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }}

        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }}

        .info-panel {{
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .info-panel h3 {{
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--accent-cyan);
        }}

        .info-panel dl {{
            font-size: 0.8rem;
            display: grid;
            grid-template-columns: 80px 1fr;
            row-gap: 6px;
            column-gap: 8px;
        }}

        .info-panel dt {{
            color: var(--text-secondary);
        }}

        .info-panel dd {{
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
            word-break: break-all;
        }}

        /* Main Viewport */
        #main {{
            flex: 1;
            position: relative;
            background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        #toolbar {{
            height: 52px;
            border-bottom: 1px solid var(--border-color);
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            z-index: 10;
        }}

        .stat-item {{
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        .stat-item span {{
            color: var(--accent-cyan);
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }}

        #tree-container {{
            flex: 1;
            overflow: auto;
            position: relative;
            cursor: grab;
        }}

        #tree-container:active {{
            cursor: grabbing;
        }}

        svg {{
            display: block;
            min-width: 100%;
            min-height: 100%;
        }}

        .branch {{
            fill: none;
            stroke: var(--branch-color);
            stroke-width: 1.5px;
            stroke-linejoin: round;
            stroke-linecap: round;
            transition: stroke 0.2s, stroke-width 0.2s;
        }}

        .leaf-node {{
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .leaf-node circle {{
            stroke-width: 2px;
            transition: r 0.2s, stroke-width 0.2s;
        }}

        .leaf-node:hover circle {{
            r: 7px;
            stroke-width: 3px;
        }}

        .leaf-label {{
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
            fill: #cbd5e1;
            cursor: pointer;
            transition: fill 0.2s, font-weight 0.2s;
            user-select: none;
        }}

        .leaf-node:hover .leaf-label {{
            fill: #fff;
            font-weight: 600;
        }}

        .highlighted .leaf-label {{
            fill: var(--accent-cyan);
            font-weight: 700;
            font-size: 12px;
        }}

        .highlighted circle {{
            stroke: #fff !important;
            stroke-width: 3px !important;
            r: 8px !important;
        }}

        .support-label {{
            font-size: 9px;
            font-family: 'JetBrains Mono', monospace;
            fill: #64748b;
            user-select: none;
        }}

        /* Tooltip */
        #tooltip {{
            position: absolute;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid var(--accent-cyan);
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 0.78rem;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.15s;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            z-index: 100;
            max-width: 320px;
        }}

        #tooltip h4 {{
            color: var(--accent-cyan);
            margin-bottom: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div id="sidebar">
        <div>
            <div class="logo-badge">🧬 Google Antigravity</div>
            <h1 style="margin-top: 10px;">{title}</h1>
            <p class="subtitle" style="margin-top: 6px;">Phylogenetic analysis generated from sequences via MAFFT and IQ-TREE Maximum Likelihood.</p>
        </div>

        <div class="control-card">
            <span class="control-label">Search Strain</span>
            <input type="text" id="searchInput" placeholder="Filter strain, vaccine, or date..." oninput="filterStrains()">
        </div>

        <div class="control-card">
            <span class="control-label">Display Mode</span>
            <div class="btn-group">
                <button id="btnPhylo" class="active" onclick="setLayout('phylogram')">Phylogram</button>
                <button id="btnClado" onclick="setLayout('cladogram')">Cladogram</button>
            </div>
            <div class="btn-group" style="margin-top: 6px;">
                <button id="btnZoomIn" onclick="zoom(1.2)">Zoom +</button>
                <button id="btnZoomOut" onclick="zoom(0.8)">Zoom -</button>
            </div>
            <button style="margin-top: 6px;" onclick="resetView()">Reset View</button>
        </div>

        <div class="control-card">
            <span class="control-label">Clade / Group Legend</span>
            <div class="legend-item">
                <div class="legend-color" style="background: #38bdf8;"></div>
                <span>Clinical Specimen (Taiwan 2023-2025)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #c084fc;"></div>
                <span>Vaccine Reference (WHO Strain)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #fbbf24;"></div>
                <span>Root Reference (A/CA/07/2009)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #34d399;"></div>
                <span>Global Reference Clade (Nextstrain)</span>
            </div>
        </div>

        <div class="info-panel" id="detailPanel">
            <h3>Node Inspector</h3>
            <p style="color: var(--text-secondary); font-size: 0.8rem;">Hover or click on any tip node to inspect its epidemiological metadata.</p>
            <dl id="metaDetails" style="display: none; margin-top: 8px;">
                <dt>Strain</dt><dd id="d-strain">-</dd>
                <dt>Group</dt><dd id="d-group">-</dd>
                <dt>Date</dt><dd id="d-date">-</dd>
                <dt>Location</dt><dd id="d-loc">-</dd>
                <dt>ID / Acc</dt><dd id="d-acc">-</dd>
            </dl>
        </div>
    </div>

    <div id="main">
        <div id="toolbar">
            <div class="stat-item">Model: <span>GTR+G4 (IQ-TREE ML)</span></div>
            <div class="stat-item">Bootstraps: <span>1,000 UFBoot</span></div>
            <div class="stat-item">Total Taxa: <span id="statTaxa">30</span></div>
            <div class="stat-item">Workflow: <span>Google Antigravity</span></div>
        </div>
        <div id="tree-container">
            <svg id="treeSvg"></svg>
        </div>
        <div id="tooltip"></div>
    </div>

    <script>
        const rawTree = {json.dumps(tree_data)};
        let currentLayout = 'phylogram';
        let scaleFactor = 1.0;
        let leavesList = [];

        const colorMap = {{
            'Clinical Specimen': '#38bdf8',
            'Vaccine Reference': '#c084fc',
            'Root Reference': '#fbbf24',
            'Global Reference Clade': '#34d399',
            'Unknown': '#94a3b8'
        }};

        // Traverse to assign vertical ranks (y-coordinates for leaves)
        let leafIndex = 0;
        function assignLeafRanks(node) {{
            if (node.is_leaf) {{
                node.yIndex = leafIndex++;
                leavesList.push(node);
            }} else {{
                node.children.forEach(assignLeafRanks);
                node.yIndex = (node.children[0].yIndex + node.children[node.children.length - 1].yIndex) / 2;
            }}
        }}

        // Calculate x-distances from root
        function calculateXPositions(node, currentDist, currentDepth) {{
            node.distFromRoot = currentDist + node.branch_length;
            node.depthFromRoot = currentDepth + 1;
            node.children.forEach(c => calculateXPositions(c, node.distFromRoot, node.depthFromRoot));
        }}

        assignLeafRanks(rawTree);
        calculateXPositions(rawTree, 0, 0);

        let maxDist = 0;
        let maxDepth = 0;
        function findMax(node) {{
            if (node.distFromRoot > maxDist) maxDist = node.distFromRoot;
            if (node.depthFromRoot > maxDepth) maxDepth = node.depthFromRoot;
            node.children.forEach(findMax);
        }}
        findMax(rawTree);

        document.getElementById('statTaxa').textContent = leavesList.length;

        const rowHeight = 28;
        const widthPadding = 120;
        const labelMargin = 20;

        function renderTree() {{
            const svg = document.getElementById('treeSvg');
            svg.innerHTML = '';

            const totalHeight = leafIndex * rowHeight + 80;
            const treeWidth = 650 * scaleFactor;
            const totalWidth = treeWidth + 600;

            svg.setAttribute('width', totalWidth);
            svg.setAttribute('height', totalHeight);

            const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            g.setAttribute('transform', `translate(50, 40)`);
            svg.appendChild(g);

            function getNodeX(node) {{
                if (currentLayout === 'phylogram') {{
                    return (node.distFromRoot / maxDist) * treeWidth;
                }} else {{
                    return (node.depthFromRoot / maxDepth) * treeWidth;
                }}
            }}

            function getNodeY(node) {{
                return node.yIndex * rowHeight;
            }}

            function drawNode(node) {{
                const x = getNodeX(node);
                const y = getNodeY(node);

                if (!node.is_leaf) {{
                    const childYs = node.children.map(getNodeY);
                    const minY = Math.min(...childYs);
                    const maxY = Math.max(...childYs);

                    // Vertical connecting line
                    const vPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                    vPath.setAttribute('d', `M ${{x}} ${{minY}} L ${{x}} ${{maxY}}`);
                    vPath.setAttribute('class', 'branch');
                    g.appendChild(vPath);

                    // Support label if available
                    if (node.confidence && node.confidence > 50) {{
                        const supText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                        supText.setAttribute('x', x - 4);
                        supText.setAttribute('y', y - 4);
                        supText.setAttribute('class', 'support-label');
                        supText.setAttribute('text-anchor', 'end');
                        supText.textContent = Math.round(node.confidence);
                        g.appendChild(supText);
                    }}

                    node.children.forEach(c => {{
                        const cx = getNodeX(c);
                        const cy = getNodeY(c);

                        // Horizontal line to child
                        const hPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                        hPath.setAttribute('d', `M ${{x}} ${{cy}} L ${{cx}} ${{cy}}`);
                        hPath.setAttribute('class', 'branch');
                        g.appendChild(hPath);

                        drawNode(c);
                    }});
                }} else {{
                    // Leaf Node
                    const color = colorMap[node.group] || '#94a3b8';
                    const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    nodeGroup.setAttribute('class', 'leaf-node');
                    nodeGroup.setAttribute('data-name', node.name);

                    // Circle
                    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                    circle.setAttribute('cx', x);
                    circle.setAttribute('cy', y);
                    circle.setAttribute('r', 5);
                    circle.setAttribute('fill', color);
                    circle.setAttribute('stroke', '#0f172a');
                    nodeGroup.appendChild(circle);

                    // Label
                    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    text.setAttribute('x', x + labelMargin);
                    text.setAttribute('y', y + 4);
                    text.setAttribute('class', 'leaf-label');
                    text.textContent = node.name;
                    nodeGroup.appendChild(text);

                    // Interactivity
                    nodeGroup.addEventListener('mouseenter', (e) => showTooltip(e, node));
                    nodeGroup.addEventListener('mouseleave', hideTooltip);
                    nodeGroup.addEventListener('click', () => selectNode(node));

                    g.appendChild(nodeGroup);
                }}
            }}

            drawNode(rawTree);
        }}

        function setLayout(layout) {{
            currentLayout = layout;
            document.getElementById('btnPhylo').classList.toggle('active', layout === 'phylogram');
            document.getElementById('btnClado').classList.toggle('active', layout === 'cladogram');
            renderTree();
        }}

        function zoom(factor) {{
            scaleFactor *= factor;
            scaleFactor = Math.max(0.5, Math.min(3.0, scaleFactor));
            renderTree();
        }}

        function resetView() {{
            scaleFactor = 1.0;
            currentLayout = 'phylogram';
            document.getElementById('btnPhylo').classList.add('active');
            document.getElementById('btnClado').classList.remove('active');
            document.getElementById('searchInput').value = '';
            filterStrains();
            renderTree();
        }}

        const tooltip = document.getElementById('tooltip');
        function showTooltip(e, node) {{
            const meta = node.metadata || {{}};
            tooltip.innerHTML = `
                <h4>${{node.name}}</h4>
                <div><strong>Group:</strong> ${{node.group}}</div>
                <div><strong>Date:</strong> ${{meta.date || 'N/A'}}</div>
                <div><strong>Region:</strong> ${{meta.country || meta.region || 'Global'}}</div>
                <div><strong>Accession:</strong> ${{meta.sample_id || 'N/A'}}</div>
            `;
            tooltip.style.opacity = 1;
            tooltip.style.left = (e.clientX + 16) + 'px';
            tooltip.style.top = (e.clientY - 20) + 'px';
        }}

        function hideTooltip() {{
            tooltip.style.opacity = 0;
        }}

        function selectNode(node) {{
            const meta = node.metadata || {{}};
            document.getElementById('metaDetails').style.display = 'grid';
            document.getElementById('d-strain').textContent = node.name;
            document.getElementById('d-group').textContent = node.group;
            document.getElementById('d-date').textContent = meta.date || 'N/A';
            document.getElementById('d-loc').textContent = (meta.country || '') + ' ' + (meta.region || '');
            document.getElementById('d-acc').textContent = meta.sample_id || 'N/A';
        }}

        function filterStrains() {{
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            document.querySelectorAll('.leaf-node').forEach(el => {{
                const name = el.getAttribute('data-name').toLowerCase();
                if (query && name.includes(query)) {{
                    el.classList.add('highlighted');
                }} else {{
                    el.classList.remove('highlighted');
                }}
            }});
        }}

        // Initial render
        renderTree();
    </script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Rendered interactive tree to: {output_html}")

if __name__ == '__main__':
    tree_file = sys.argv[1] if len(sys.argv) > 1 else "data/h1n1/h1n1_ha_tree.treefile"
    meta_file = sys.argv[2] if len(sys.argv) > 2 else "data/h1n1/h1n1_ha_metadata.tsv"
    out_file = sys.argv[3] if len(sys.argv) > 3 else "outputs/h1n1_interactive_tree.html"
    generate_interactive_html(tree_file, meta_file, out_file)
