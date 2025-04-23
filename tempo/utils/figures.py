from astroplan.plots import plot_sky, plot_airmass, plot_sky_24hr, plot_finder_image
from astroplan import FixedTarget, moon
from matplotlib import pyplot as plt


def plot_targets(target, obstime, file_prefix, observer):
    plot_airmass(FixedTarget(target, name='target'), observer, obstime)
    _moon = moon.get_body('moon', obstime, location=observer.location)
    _moon.name = 'Moon'
    moon_style = {'linestyle': '--', 'color': 'black'}
    airmass_plot_file = file_prefix + '.airmass.png'
    sky_plot_file = file_prefix + '.skyplot.png'
    ax = plot_airmass(
        _moon, observer, obstime, brightness_shading=True, style_kwargs=moon_style, altitude_yaxis=True
    )
    ax.legend()
    plt.savefig(airmass_plot_file)
    plt.clf()

    # plot_sky(target, observer, obstime)
    ax2 = plot_sky(_moon, observer, obstime)
    ax2.legend()
    plt.savefig(sky_plot_file)
    plt.clf()
    return airmass_plot_file, sky_plot_file
