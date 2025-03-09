import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# K6 'http_req_duration' stats, all converted into milliseconds
stats = {
    'min': 0.84,       # ~839.57 µs
    'median': 135.36,
    'avg': 309.02,
    'p90': 860.60,
    'p95': 1240.00,    # 1.24 s ≈ 1240 ms
    'max': 5480.00     # 5.48 s ≈ 5480 ms
}

mn = stats['min']
md = stats['median']
avg = stats['avg']
p90 = stats['p90']
p95 = stats['p95']
mx = stats['max']

x_position = 1

fig, ax = plt.subplots(figsize=(5, 6))

# 1) Vertical line (whisker) for min -> max
ax.plot([x_position, x_position], [mn, mx], color='black', linewidth=2)

# 2) Multiple candle bodies
candle_width = 0.3

# Min to Max box (light gray)
rect_minmax = Rectangle(
    (x_position - candle_width / 2, mn),
    candle_width,
    mx - mn,
    facecolor='gray', alpha=0.1, edgecolor='black'
)
ax.add_patch(rect_minmax)

# p90 to p95 box (blue)
rect_9095 = Rectangle(
    (x_position - candle_width / 2, p90),
    candle_width,
    p95 - p90,
    facecolor='blue', alpha=0.3, edgecolor='black'
)
ax.add_patch(rect_9095)

# Median to p90 box (green)
rect_medp90 = Rectangle(
    (x_position - candle_width / 2, md),
    candle_width,
    p90 - md,
    facecolor='green', alpha=0.2, edgecolor='black'
)
ax.add_patch(rect_medp90)

# 3) Horizontal lines for all statistics
ax.hlines(mn, x_position - 0.4, x_position + 0.4,
          color='gray', linestyles='solid', linewidth=2,
          label=f'Min: {mn:.2f} ms')

ax.hlines(md, x_position - 0.4, x_position + 0.4,
          color='green', linestyles='dashed', linewidth=2,
          label=f'Median: {md:.2f} ms')

ax.hlines(avg, x_position - 0.4, x_position + 0.4,
          color='red', linestyles='dotted', linewidth=2,
          label=f'Average: {avg:.2f} ms')

ax.hlines(p90, x_position - 0.4, x_position + 0.4,
          color='purple', linestyles='dashdot', linewidth=2,
          label=f'p(90): {p90:.2f} ms')

ax.hlines(p95, x_position - 0.4, x_position + 0.4,
          color='orange', linestyles='dashdot', linewidth=2,
          label=f'p(95): {p95:.2f} ms')

ax.hlines(mx, x_position - 0.4, x_position + 0.4,
          color='gray', linestyles='solid', linewidth=2,
          label=f'Max: {mx:.2f} ms')

# 5) Use a log scale to handle the wide range
ax.set_yscale('log')

# (Optional) Define y-limits to ensure the min is visible but not too small
# ax.set_ylim(0.8, mx * 1.2)

# Labels and legend
ax.set_title("K6 HTTP Req Duration – Candlestick View", fontsize=12)
ax.set_ylabel("Duration (ms)")
ax.set_xticks([x_position])
ax.set_xticklabels(["HTTP Req Duration"])
ax.legend(loc='upper left')  # Move legend if it hides your candle

# Add to legend
ax.plot([], [], color='gray', alpha=0.1, label='Min-Max Range')
ax.plot([], [], color='green', alpha=0.2, label='Median-p90 Range')
ax.plot([], [], color='blue', alpha=0.3, label='p90-p95 Range')

plt.tight_layout()
plt.show()