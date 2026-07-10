import matplotlib.pyplot as plt

BACKGROUND = "#0B0F19"
PANEL_BG = "#1E293B"
GRID = "#1E2433"
TEXT = "#E8ECF4"
SUBTEXT = "#8B93A7"

LINE_ACCENT = "#FFD166"   
LOS_COLOR = "#00F2FE"     
NLOS_COLOR = "#FF4B5C"  


def new_dark_figure(figsize=(10, 5), dpi=150, panel_bg=False):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(PANEL_BG if panel_bg else BACKGROUND)
    return fig, ax


def style_axes(ax, title=None, xlabel=None, ylabel=None, title_loc="center",
               grid_color=GRID, grid_alpha=0.4, grid_linestyle=":"):
    if title:
        ax.set_title(title, fontsize=12, fontweight="bold", color=TEXT,
                     pad=15, loc=title_loc)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color=TEXT, labelpad=8)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color=TEXT, labelpad=8)
    ax.tick_params(colors=SUBTEXT)
    ax.grid(True, linestyle=grid_linestyle, alpha=grid_alpha, color=grid_color)
    return ax


def style_legend(ax, loc="lower left", fontsize=9):
    """Apply consistent legend styling matching the dark theme."""
    legend = ax.legend(loc=loc, frameon=True, facecolor=BACKGROUND,
                        edgecolor=GRID, fontsize=fontsize)
    plt.setp(legend.get_texts(), color=TEXT)
    return legend