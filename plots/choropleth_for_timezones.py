import pandas as pd
import geopandas as gpd
import pytz
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Most common UTC offsets of commit per repository
data = [
    ("+0100", 10),
    ("+1000", 1),
    ("+0200", 51),
    ("+0300", 4),
    ("+0000", 5),
    ("-0500", 2),
    ("-1000", 1),
    ("+0800", 2),
    ("-0400", 14),
    ("-0700", 9),
    ("-0600", 2),
    ("+1100", 1),
    ("+0530", 1),
    ("+0900", 1)
]
df = pd.DataFrame(data, columns=["offset", "repo_count"])

# --- Step 1: Load timezone polygons (GeoJSON) ---
gdf = gpd.read_file('timezones.geojson')

# --- Step 2: Map each tzid to its standard UTC offset (winter) ---
def tzid_to_offset(tzid):
    try:
        tz = pytz.timezone(tzid)
        dt = datetime.datetime(2020, 1, 1)
        offset = tz.utcoffset(dt)
        if offset is not None:
            total_mins = int(offset.total_seconds() // 60)
            sign = '+' if total_mins >= 0 else '-'
            hours, minutes = divmod(abs(total_mins), 60)
            return f"{sign}{hours:02d}00" if minutes == 0 else f"{sign}{hours:02d}{minutes:02d}"
    except Exception:
        return None

gdf['winter_offset'] = gdf['tzid'].apply(tzid_to_offset)

# --- Step 3: Mark regions that observe DST ---
def has_dst(tzid):
    try:
        tz = pytz.timezone(tzid)
        dt_winter = datetime.datetime(2020, 1, 1)
        dt_summer = datetime.datetime(2020, 7, 1)
        offset_winter = tz.utcoffset(dt_winter)
        offset_summer = tz.utcoffset(dt_summer)
        return offset_winter != offset_summer
    except Exception:
        return False

gdf['has_dst'] = gdf['tzid'].apply(has_dst)

# --- Step 4: Merge repo counts into the GeoDataFrame using winter_offset ---
gdf = gdf.merge(df, left_on='winter_offset', right_on='offset', how='left')

# --- Step 5: Set categorical colors for repo_count ---
repo_counts = sorted(df['repo_count'].unique())
colors = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3",
    "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999", "#1b9e77", "#d95f02"
]
color_dict = {rc: colors[i % len(colors)] for i, rc in enumerate(repo_counts)}
gdf['color'] = gdf['repo_count'].map(color_dict)
gdf['color'] = gdf['color'].fillna('lightgrey')  # color for regions with no data

# --- Step 6: Plot the map ---
fig, ax = plt.subplots(figsize=(18, 9))

# 1. Plot all regions with solid categorical color (with transparency)
gdf.plot(
    color=gdf['color'],
    edgecolor='0.6',
    linewidth=0.5,
    ax=ax,
    alpha=0.85,
    zorder=1
)

# 2. Plot DST regions with hatching, no fill (on top)
gdf[gdf['has_dst']].plot(
    ax=ax,
    facecolor="none",
    edgecolor="black",
    linewidth=0.8,
    hatch="////",
    zorder=2
)

# --- Step 7: Build a custom legend ---
patches = []
for rc in repo_counts:
    patches.append(mpatches.Patch(
        color=color_dict[rc], label=f"{rc} repo{'s' if rc > 1 else ''}"))
hatch_patch = mpatches.Patch(
    facecolor='white', edgecolor='black', hatch='////', label='DST Observed')
patches.append(hatch_patch)
patches.append(mpatches.Patch(color='lightgrey', label='No data'))

ax.legend(handles=patches, loc='lower left', frameon=True, fontsize=11, title="Most Common Repo Timezones")

ax.set_title(
    "Repo Distribution by Standard (Winter) UTC Offset\n"
    "Color: Number of repos for each standard offset.\n"
    "Striped areas: Regions observing Daylight Saving Time (DST)",
    fontsize=18, fontweight='bold'
)
ax.axis('off')

plt.tight_layout()
plt.savefig("timezone_choropleth_by_winter_offset.pdf", bbox_inches='tight')
plt.show()
