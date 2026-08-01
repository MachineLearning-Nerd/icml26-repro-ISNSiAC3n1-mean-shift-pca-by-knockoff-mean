"""Generate evidence-bearing SVGs on the configured research compute."""

import base64
import math


COLORS = ["#4f46e5", "#ef4444", "#f59e0b", "#10b981"]


def svg_frame(title: str, body: str, subtitle: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">
<rect width="960" height="540" fill="#fafafa"/>
<text x="55" y="55" font-family="system-ui" font-size="28" font-weight="700" fill="#111827">{title}</text>
<text x="55" y="83" font-family="system-ui" font-size="15" fill="#4b5563">{subtitle}</text>
{body}
</svg>'''


def bar_chart(title: str, labels: list[str], values: list[float], subtitle: str) -> str:
    bars = []
    width = 180
    gap = 75
    for index, (label, value) in enumerate(zip(labels, values)):
        x = 130 + index * (width + gap)
        height = 350 * value
        y = 450 - height
        bars.append(
            f'<rect x="{x}" y="{y:.2f}" width="{width}" height="{height:.2f}" rx="8" fill="{COLORS[index]}"/>'
            f'<text x="{x + width / 2}" y="{y - 12:.2f}" text-anchor="middle" font-family="system-ui" font-size="22" font-weight="700">{value:.3f}</text>'
            f'<text x="{x + width / 2}" y="485" text-anchor="middle" font-family="system-ui" font-size="18">{label}</text>'
        )
    body = '<line x1="80" y1="450" x2="900" y2="450" stroke="#9ca3af"/>' + ''.join(bars)
    return svg_frame(title, body, subtitle)


def line_chart(
    title: str,
    x_values: list[float],
    series: list[tuple[str, list[float]]],
    subtitle: str,
    log_x: bool = False,
    log_y: bool = False,
) -> str:
    transform_x = math.log if log_x else lambda value: value
    transform_y = math.log if log_y else lambda value: value
    xs = [transform_x(value) for value in x_values]
    ys = [transform_y(value) for _, values in series for value in values]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    sx = lambda value: 105 + 760 * (transform_x(value) - x_min) / (x_max - x_min)
    sy = lambda value: 450 - 320 * (transform_y(value) - y_min) / (y_max - y_min)
    elements = ['<line x1="105" y1="450" x2="870" y2="450" stroke="#9ca3af"/>', '<line x1="105" y1="125" x2="105" y2="450" stroke="#9ca3af"/>']
    for index, (label, values) in enumerate(series):
        points = ' '.join(f'{sx(x):.2f},{sy(y):.2f}' for x, y in zip(x_values, values))
        elements.append(f'<polyline points="{points}" fill="none" stroke="{COLORS[index]}" stroke-width="4"/>')
        for x, y in zip(x_values, values):
            elements.append(f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="5" fill="{COLORS[index]}"/>')
        elements.append(f'<rect x="{600 + index * 145}" y="98" width="18" height="5" fill="{COLORS[index]}"/><text x="{624 + index * 145}" y="106" font-family="system-ui" font-size="14">{label}</text>')
    for value in x_values:
        elements.append(f'<text x="{sx(value):.2f}" y="480" text-anchor="middle" font-family="system-ui" font-size="13">{int(value)}</text>')
    return svg_frame(title, ''.join(elements), subtitle)


def collision_diagram() -> str:
    body = '''
<line x1="120" y1="290" x2="840" y2="290" stroke="#9ca3af" stroke-width="3"/>
<circle cx="480" cy="290" r="18" fill="#4f46e5"/><circle cx="480" cy="290" r="10" fill="#ef4444"/>
<text x="480" y="245" text-anchor="middle" font-family="system-ui" font-size="26" font-weight="700">14/3</text>
<text x="480" y="340" text-anchor="middle" font-family="system-ui" font-size="17">covariance ℓ=3 and mean θ²=3 coincide</text>
<circle cx="275" cy="290" r="11" fill="#f59e0b"/><text x="275" y="265" text-anchor="middle" font-family="system-ui" font-size="18">187/60</text>
<text x="275" y="375" text-anchor="middle" font-family="system-ui" font-size="15">negative control θ²=6/5 separates by 31/20</text>
<text x="120" y="420" font-family="system-ui" font-size="15" fill="#4b5563">Exact rational arithmetic; all strengths are strictly above the BBP threshold at c=1/2.</text>'''
    return svg_frame(
        "Claim 1: exact spike-location collision",
        body,
        "Universal disjointness is falsified; the union/convergence formula is not disputed.",
    )


def generate_assets(evidence: dict) -> dict[str, str]:
    claims = {item["claim"]: item for item in evidence["claims"]}
    claim5 = claims[5]["raw"]["aggregate"]
    claim2_rows = claims[2]["raw"]["rows"]
    claim3_rows = claims[3]["raw"]["rows"]
    return {
        "headline.svg": bar_chart(
            "5% contamination at d/n=1",
            ["MS-PCA", "PCA", "Robust PCA"],
            [
                claim5["ms_mean_alignment"],
                claim5["pca_mean_alignment"],
                claim5["rpca_mean_alignment"],
            ],
            "Mean clean-PC alignment; MS/PCA: 36 trials, Robust PCA: 12 paired n=500 trials",
        ),
        "claim2_counterexample.svg": line_chart(
            "Claim 2: residual does not decay",
            [row["n"] for row in claim2_rows],
            [
                ("counterexample", [row["counterexample_median"] for row in claim2_rows]),
                ("centered control", [row["centered_control_median"] for row in claim2_rows]),
            ],
            "Median over 200 trials per size; log-log axes",
            log_x=True,
            log_y=True,
        ),
        "claim3_matching.svg": line_chart(
            "Claim 3: knockoff separates the two spikes",
            [row["n"] for row in claim3_rows],
            [
                ("covariance", [row["median_covariance_shift_over_epsilon"] for row in claim3_rows]),
                ("mean shift", [row["median_mean_shift_over_epsilon"] for row in claim3_rows]),
            ],
            "Median nearest eigenvalue displacement divided by ε=n⁻¹ᐟ²",
            log_x=True,
            log_y=True,
        ),
        "claim1_collision.svg": collision_diagram(),
    }


def emit_release_assets(evidence: dict) -> None:
    for name, svg in generate_assets(evidence).items():
        encoded = base64.b64encode(svg.encode()).decode()
        print(f"RELEASE_ASSET_BASE64_BEGIN {name}")
        print(encoded)
        print(f"RELEASE_ASSET_BASE64_END {name}")
