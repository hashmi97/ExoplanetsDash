from collections import OrderedDict

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

from dataloader import DataLoader

ADDENDUM = '''Planet Name: The name given to the planet.\n Star Name: The name given to the host star.\n Discovery 
Method: The method used to discover this planet.\n Discovery Year: The year this discovery was made.\n Discovery 
Facility: The name of the discovering facility.\n Semi-Major Axis (a): [Semi-major axis](
https://en.wikipedia.org/wiki/Semi-major_and_semi-minor_axes) of an ellipse is its longest radius.\n Semi-Minor Axis 
(b): [Semi-minor axis](https://en.wikipedia.org/wiki/Semi-major_and_semi-minor_axes) of an ellipse is its shortest 
radius.\n Eccentricity (e): The eccentricity of an astronomical orbit used as a measure of its deviation from 
circularity.\n Orbital Period (Days): The number of days it takes the planet to complete a whole revolution around 
its host star.\n Planet Radius (Jupiter): The radius of the planet normalized to the radius of Jupiter.\n Planet 
Radius (Earth): The radius of the planet normalized to the radius of Earth.\n Planet Mass (Jupiter): The mass of the 
planet normalized to the mass of Jupiter.\n Planet Mass (Earth): The mass of the planet normalized to the mass of 
Earth.\n Equilibrium Temperature (Kelvin): The theoretical [temperature](
https://en.wikipedia.org/wiki/Planetary_equilibrium_temperature) that a planet would be if it were a black body being 
heated only by its parent star.\n Planet Density (g/cm3): The density of the planet.\n Star Radius (Solar): The 
radius of the host star normalized to the radius of the sun.\n Star Mass (Solar): The mass of the host star 
normalized to the mass of the sun.\n Star Distance (Parsec): The distance to this planet from our solar system 
measured in [parsecs](https://en.wikipedia.org/wiki/Parsec).\n '''
DEFAULT_PLANET_1 = 'Earth'
DEFAULT_PLANET_2 = 'HD 80606 b'

df = DataLoader().get_data().dropna(subset=['planetRadJ', 'orbitSemiMaj', 'starRadius',
                                            'planetEcce', 'starDistance'])

planetRScaler = MinMaxScaler((10, 50))
starRScaler = MinMaxScaler((60, 80))
df['scaledPlanetRadJ'] = planetRScaler.fit_transform(df['planetRadJ'].to_numpy().reshape((-1, 1)))
df['scaledStarRadius'] = starRScaler.fit_transform(df['starRadius'].to_numpy().reshape((-1, 1)))
available_planets = df.index.tolist()


def ellipse(x_center=0, y_center=0, a=1, b=1, N=1000):
    # x_center, y_center the coordinates of ellipse center
    # ax1 ax2 two orthonormal vectors representing the ellipse axis directions
    # a, b the ellipse parameters

    t = np.linspace(0, 2 * np.pi, N)
    # ellipse parameterization with respect to a system of axes of directions a1, a2
    xs = a * np.cos(t)
    ys = b * np.sin(t)
    # rotation matrix
    ax1 = [1, 0]
    ax2 = [0, 1]
    R = np.array([ax1, ax2]).T

    # coordinate of the  ellipse points with respect to the system of axes [1, 0], [0,1] with origin (0,0)
    xp, yp = np.dot(R, [xs, ys])
    x = xp + x_center
    y = yp + y_center
    return x, y


def getPlanetDetails(planetName):
    planetDetails = {}
    e = df.loc[planetName]['planetEcce']
    a = df.loc[planetName]['orbitSemiMaj']
    planetDetails['a'] = a
    planetDetails['b'] = a * np.sqrt(1 - e ** 2)
    planetDetails['starR'] = df.loc[planetName]['scaledStarRadius']
    planetDetails['starName'] = df.loc[planetName]['starName']
    planetDetails['planetR'] = df.loc[planetName]['scaledPlanetRadJ']
    planetDetails['planetName'] = planetName
    return planetDetails


def getPlanetTableDF(planetName):
    values = [planetName]

    planetRow = df.loc[planetName]

    values.append(planetRow['starName'])

    values.append(planetRow['discoveryMethod'])

    if np.isnan(planetRow['discoveryYear']):
        values.append("N/A")
    else:
        values.append(planetRow['discoveryYear'])

    values.append(planetRow['discoveryFacility'])
    values.append(f"{planetRow['orbitSemiMaj']:.2f}")
    orbitSemiMin = planetRow['orbitSemiMaj'] * (1 - planetRow['planetEcce'] ** 2) ** (1 / 2)
    values.append(f"{orbitSemiMin:.2f}")
    values.append(f"{planetRow['planetEcce']:.2f}")
    values.append(f"{planetRow['orbitalPeriod']:.3f}")
    values.append(f"{planetRow['planetRadJ']:.5f}")
    values.append(f"{planetRow['planetRadE']:.2f}")

    if np.isnan(planetRow['planetMassJ']):
        values.append("Missing Data")
        values.append("Missing Data")
    else:
        values.append(f"{planetRow['planetMassJ']:.5f}")
        values.append(f"{planetRow['planetMassE']:.2f}")

    if np.isnan(planetRow['planetEqtT']):
        values.append("Missing Data")
    else:
        values.append(f"{planetRow['planetEqtT']:.0f}")

    if np.isnan(planetRow['planetDens']):
        values.append("Missing Data")
    else:
        values.append(f"{planetRow['planetDens']:.3f}")

    values.append(f"{planetRow['starRadius']:.3f}")

    if np.isnan(planetRow['starMass']):
        values.append("Missing Data")
    else:
        values.append(f"{planetRow['starMass']:.2f}")

    values.append(f"{planetRow['starDistance']:.2f}")
    data = OrderedDict(
        [
            ("Property", ['Planet Name', 'Star Name', 'Discovery Method', 'Discovery Year', 'Discovery Facility',
                          'Semi-Major Axis (a)', 'Semi-Minor Axis (b)', 'Eccentricity (e)', 'Orbital Period',
                          'Planet Radius (Jupiter)', 'Planet Radius (Earth)', 'Planet Mass (Jupiter)',
                          'Planet Mass (Earth)', 'Equilibrium Temperature (Kelvin)', 'Planet Density (g/cm3)',
                          'Star Radius (Solar)', 'Star Mass (Solar)', 'Star Distance (Parsec)']),
            ("Value", values)
        ]
    )

    table_df = pd.DataFrame(data)

    return table_df


def generate_plot(planetName):
    params = getPlanetDetails(planetName)
    fig = go.Figure()
    # Set up the orbit
    a = params['a']
    b = params['b']
    orbit_x, orbit_y = ellipse(a=a, b=b)
    fig.add_scatter(
        x=orbit_x,
        y=orbit_y,
        mode='lines',
        name='Planet Orbit')

    # Set up the star
    fig.add_scatter(
        x=[0],
        y=[0],
        name=f"Star: {params['starName']}",
        marker=dict(size=[params['starR']],
                    color='#ffff00'),
        mode="markers")

    # Set up the planet
    fig.add_scatter(
        x=[0],
        y=[b],
        name=f"Planet: {params['planetName']}",
        marker=dict(size=[params['planetR']],
                    color='#615239'),
        mode="markers")

    # Add the Semi major axis
    fig.add_scatter(
        x=[0, a],
        y=[0, 0],
        name="Semi Major Axis",
        mode="lines",
        textposition="bottom center")
    fig.add_annotation(x=a / 2, y=0,
                       text=f"a={a}AU",
                       showarrow=False,
                       yshift=10)

    # Edit the background
    BACKGROUND_COLOR = 'rgb(214, 214, 193)'

    fig.update_layout(paper_bgcolor=BACKGROUND_COLOR, plot_bgcolor=BACKGROUND_COLOR)
    return fig
