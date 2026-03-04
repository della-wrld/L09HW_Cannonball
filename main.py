from math import sin, cos, radians

import altair as alt
import pandas as pd
import streamlit as st
import random


class Print_Iface:
    ## Handles plotting of the trajectory (Composition)

    def __init__(self):
        self.x_domain = (0, 200)
        self.y_domain = (0, 100)
        self.width = 700
        self.height = 400

    def plot_trajectory(self, xs, ys, title="Trajectory"):
        if not xs:
            st.warning("No trajectory points were generated.")
            return

        df = pd.DataFrame({"x": xs, "y": ys})

        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X("x:Q", scale=alt.Scale(domain=list(self.x_domain)), title="Distance (m)"),
                y=alt.Y("y:Q", scale=alt.Scale(domain=list(self.y_domain)), title="Height (m)")
            )
            .properties(width=self.width, height=self.height)
        )

        st.subheader(title)
        st.altair_chart(chart, use_container_width=True)


## Represent a cannonball, tracking its position and velocity.
class Cannonball:

    ## Create a new cannonball at the provided x position.
    def __init__(self, x):
        self._x = x
        self._y = 0
        self._vx = 0
        self._vy = 0

        # Composition: Cannonball HAS-A Print_Iface
        self.printer = Print_Iface()

    ## Move the cannon ball
    def move(self, sec, grav):
        dx = self._vx * sec
        dy = self._vy * sec

        self._vy = self._vy - grav * sec

        self._x = self._x + dx
        self._y = self._y + dy

    ## Get the current x position
    def getX(self):
        return self._x

    ## Get the current y position
    def getY(self):
        return self._y

    ## Shoot the cannon ball
    def shoot(self, angle, velocity, user_grav, step=0.1):

        self._x = 0
        self._y = 0

        self._vx = velocity * cos(angle)
        self._vy = velocity * sin(angle)

        xs = []
        ys = []

        self.move(step, user_grav)

        while self.getY() > 1e-14:
            xs.append(self.getX())
            ys.append(self.getY())
            self.move(step, user_grav)

        return xs, ys

    ## Render the plot using Print_Iface
    def render(self, xs, ys, title="Cannonball Trajectory"):
        self.printer.plot_trajectory(xs, ys, title)


## Crazyball subclass (Inheritance)
class Crazyball(Cannonball):

    def move(self, sec, grav):
        super().move(sec, grav)

        self.rand_q = random.randrange(0, 10)

        if self.getX() < 400:
            self._x += random.uniform(-0.8, 0.8)
            self._y += random.uniform(-0.8, 0.8)

            if self._y < 0:
                self._y = 0


def run_app():

    st.title("Cannonball Trajectory")

    angle_deg = st.number_input(
        "Starting angle (degrees)", min_value=0.0, max_value=90.0, value=45.0
    )

    velocity = st.selectbox("Initial velocity", options=[15, 25, 40], index=1)

    gravity_options = {
        "Earth": 9.81,
        "Moon": 1.62
    }

    gravity_name = st.selectbox("Gravity", options=list(gravity_options.keys()), index=0)
    gravity = gravity_options[gravity_name]

    step = 0.1

    col1, col2 = st.columns(2)
    simulate = col1.button("Simulate")
    simulate_crazy = col2.button("Simulate Crazy")

    angle_rad = radians(angle_deg)

    if simulate:
        ball = Cannonball(0)
        xs, ys = ball.shoot(angle_rad, velocity, gravity, step)
        ball.render(xs, ys, f"{gravity_name} Cannonball")

    if simulate_crazy:
        crazy = Crazyball(0)
        xs, ys = crazy.shoot(angle_rad, velocity, gravity, step)
        crazy.render(xs, ys, f"{gravity_name} Crazyball")


if __name__ == "__main__":
    run_app()
    