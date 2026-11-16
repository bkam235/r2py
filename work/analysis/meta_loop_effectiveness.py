"""Primary (plateau) and secondary (share of finals >= 0.95) objective of META_LOOP.md by scoring epoch.

Values: the production default at each epoch. Sources (IMPROVEMENT_PLAN.md and the finals files):
- default_2026_10_20: replay work/replay_default (epoch 1); curve "default with conversation" epochs 3-8;
  fresh replay work/replay_default_e7 (epoch 7, second sample).
- default_2026_11_01: work/replay_default_e8 (epoch 8); e8 sample-0 re-verified under epoch 9
  (work/ceiling_glm53/baseline_default_e8_s0_epoch9.jsonl).
- default_2026_11_12 (DeepSeek Flash): work/dsflash_{default,heldout}/finals_epoch{9,10,11,13,14}.jsonl.
  Held-out epoch 13 excludes sparse_logical's one-off crash (0.9070 / 30 of 46, as the log reads it).
Epoch 2 and 12: no measurement of the default (epoch 12 moved no score; carried, hollow).
"""
import matplotlib.pyplot as plt

BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8984"
INK, INK2 = "#0b0b0b", "#52514e"

# (epoch, value); a default flip is two points at the same epoch: old default, then new default.
plateau_train = [(1, .782), (3, .791), (4, .792), (5, .792), (6, .792), (7, .792), (8, .792), (8, .809),
                 (9, .816), (9, .881), (10, .880), (11, .881), (12, .881), (13, .865), (14, .867)]
plateau_ho = [(9, .904), (10, .907), (11, .907), (12, .907), (13, .907), (14, .907)]
share_train = [(1, .250), (7, .250), (8, .317), (9, .317), (9, .533), (10, .550), (11, .550), (12, .550),
               (13, .517), (14, .533)]
share_ho = [(9, .630), (10, .652), (11, .652), (12, .652), (13, .652), (14, .652)]
extra_samples = {"plateau": [(7, .781), (8, .800)], "share": []}  # second replay samples / two-sample mean
carried = {12}
flips = [(8, "entity-addressed\nfeedback"), (9, "DeepSeek Flash\nagent")]

plt.rcParams.update({"font.family": "Segoe UI", "font.size": 10, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True, facecolor="#fcfcfb")


def draw(ax, train, ho, extra, title, ylim, flip_y):
    ax.set_facecolor("#fcfcfb")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#d6d5cf")
    ax.grid(axis="y", color="#ebeae5", lw=1)
    ax.set_axisbelow(True)
    for series, color, label in ((train, BLUE, "training (60)"), (ho, ORANGE, "held-out (46)")):
        xs, ys = zip(*series)
        ax.plot(xs, ys, color=color, lw=2, label=label, zorder=2)
        for x, y in series:
            hollow = x in carried
            ax.plot(x, y, "o", ms=7, mfc="#fcfcfb" if hollow else color, mec="#fcfcfb" if not hollow else color,
                    mew=2, zorder=3)
        ax.annotate(f"{ys[-1]:.3f}", (xs[-1], ys[-1]), xytext=(8, 0), textcoords="offset points",
                    va="center", color=INK, fontsize=9)
    if extra:
        ex, ey = zip(*extra)
        ax.plot(ex, ey, "o", ms=6, mfc="none", mec=GREY, mew=1.5, label="other replay sample", zorder=3)
    for x, name in flips:
        ys_at = [y for e, y in train if e == x]
        if len(ys_at) < 2:  # old default not measured under this epoch
            continue
        ax.annotate("", (x, ys_at[1]), (x, ys_at[0]), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1))
        ax.text(x - 0.15, flip_y[x], f"gain: {name}", ha="right", va="center", fontsize=8.5, color=INK2)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=8)
    ax.set_ylim(*ylim)
    ax.legend(loc="upper left", frameon=False, fontsize=9)


draw(axes[0], plateau_train, plateau_ho, extra_samples["plateau"],
     "Primary: plateau of the production default (mean final score)", (0.76, 0.93), {8: .815, 9: .86})
draw(axes[1], share_train, share_ho, None,
     "Secondary: share of finals >= 0.95", (0.15, 0.72), {8: .38, 9: .45})
axes[1].text(7.3, .325, "gain: entity-addressed feedback\n(old default not re-scored\nunder epoch 8)",
             ha="right", va="center", fontsize=8.5, color=INK2)
axes[1].set_xticks(range(1, 15))
axes[1].set_xlabel("scoring epoch")
fig.text(0.01, 0.005,
         "Vertical arrows: default flips (harness gains) inside an epoch. Moves between epochs are scorer "
         "corrections (same programs). Hollow = epoch 12, not re-verified (no score moved).\n"
         "Epoch 2: default not measured. Share before epoch 9 is capped by the loop's 0.9 stop threshold. "
         "Replay noise: about ±0.03 on the plateau, ±0.09 on the share.",
         fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.05, 1, 1))
out = "work/analysis/meta_loop_effectiveness.png"
fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
print(out)
