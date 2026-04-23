from __future__ import annotations

import math
import time

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import streamlit as st

from application.clock_engine import ClockEngine
from domain.value_objects.clock_time import ClockTime
from services.time_service import TimeService


class ClockUI:
    """Capa de presentacion con Streamlit para visualizar el reloj."""

    def __init__(self) -> None:
        if "engine" not in st.session_state:
            st.session_state.engine = ClockEngine(TimeService())
        if "running" not in st.session_state:
            st.session_state.running = False

        self.__engine: ClockEngine = st.session_state.engine

    def render(self) -> None:
        st.set_page_config(page_title="Circular Analog Clock", page_icon=":clock9:", layout="centered")
        st.title("Reloj Analogico con Lista Circular Doble")
        st.caption("Simulacion orientada a objetos con estructura de datos circular")

        col_start, col_stop, col_sync = st.columns(3)

        if col_start.button("Iniciar"):
            st.session_state.running = True
        if col_stop.button("Pausar"):
            st.session_state.running = False
        if col_sync.button("Sincronizar"):
            self.__engine.synchronize_with_system_time()

        refresh_count = None
        if st.session_state.running:
            # Usa autorefresh cuando esta disponible y aplica fallback si no existe.
            if hasattr(st, "autorefresh"):
                refresh_count = st.autorefresh(interval=1000, key="clock_autorefresh")

        current_time = self.__engine.get_current_time()
        self.__render_analog_clock(current_time)
        st.metric(label="Hora 24h", value=current_time.to_24_hour_format())
        st.metric(label="Hora 12h", value=current_time.to_12_hour_format())

        if st.button("Retroceder 1 segundo"):
            self.__engine.move_backward_one_second()
            st.rerun()

        if st.session_state.running and refresh_count is not None:
            last_refresh_count = st.session_state.get("last_refresh_count")

            if last_refresh_count is None:
                st.session_state.last_refresh_count = refresh_count
            elif refresh_count != last_refresh_count:
                self.__engine.tick()
                st.session_state.last_refresh_count = refresh_count
        elif st.session_state.running:
            time.sleep(1)
            self.__engine.tick()
            st.rerun()
        else:
            st.session_state.pop("last_refresh_count", None)

    def __render_analog_clock(self, current_time: ClockTime) -> None:
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_alpha(0.0)

        # Caratula principal del reloj.
        face = plt.Circle((0, 0), 1.0, edgecolor="black", facecolor="white", linewidth=3)
        ax.add_patch(face)

        number_colors = {
            1: "#8B8E2F",
            2: "#D6452A",
            3: "#A62B3A",
            4: "#5A3D63",
            5: "#8B8E2F",
            6: "#D6452A",
            7: "#A62B3A",
            8: "#5A3D63",
            9: "#8B8E2F",
            10: "#D6452A",
            11: "#A62B3A",
            12: "#5A3D63",
        }

        for hour in range(1, 13):
            angle = math.radians(90 - (hour * 30))
            x = 0.78 * math.cos(angle)
            y = 0.78 * math.sin(angle)
            ax.text(
                x,
                y,
                str(hour),
                fontsize=34,
                ha="center",
                va="center",
                color=number_colors[hour],
                family="DejaVu Sans",
            )

        # Marcas de los minutos en el borde.
        for mark in range(60):
            angle = math.radians(90 - (mark * 6))
            inner_radius = 0.9 if mark % 5 == 0 else 0.95
            outer_radius = 1.0
            x_start = inner_radius * math.cos(angle)
            y_start = inner_radius * math.sin(angle)
            x_end = outer_radius * math.cos(angle)
            y_end = outer_radius * math.sin(angle)
            lw = 3 if mark % 5 == 0 else 1
            ax.plot([x_start, x_end], [y_start, y_end], color="black", linewidth=lw)

        hour_angle = math.radians(90 - ((current_time.hour % 12) * 30 + current_time.minute * 0.5))
        minute_angle = math.radians(90 - (current_time.minute * 6 + current_time.second * 0.1))
        second_angle = math.radians(90 - current_time.second * 6)

        self.__draw_hand(ax, hour_angle, length=0.42, width=5, color="black")
        self.__draw_hand(ax, minute_angle, length=0.62, width=4, color="black")
        self.__draw_hand(ax, second_angle, length=0.74, width=1.5, color="black")

        center = plt.Circle((0, 0), 0.03, color="black")
        ax.add_patch(center)
        ax.text(0, 0.5, "CLOCK APP", ha="center", va="center", fontsize=11, color="black", family="DejaVu Sans")

        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")
        ax.axis("off")

        st.pyplot(fig, clear_figure=True, use_container_width=True)

    @staticmethod
    def __draw_hand(ax: Axes, angle: float, length: float, width: float, color: str) -> None:
        x = length * math.cos(angle)
        y = length * math.sin(angle)
        ax.plot([0, x], [0, y], color=color, linewidth=width, solid_capstyle="round")


def main() -> None:
    ui = ClockUI()
    ui.render()


if __name__ == "__main__":
    main()
