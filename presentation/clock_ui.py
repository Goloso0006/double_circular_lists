from __future__ import annotations

import math
import time

import matplotlib
matplotlib.use("Agg")
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
        st.set_page_config(page_title="Clock", page_icon=":clock9:", layout="centered")
        st.title("What time is it?") 

        if "manual_time" not in st.session_state:
            current = self.__engine.get_current_time()
            st.session_state.manual_time = current.to_24_hour_format()

        st.session_state.manual_time = st.text_input(
            "Establecer hora manual (HH:MM:SS)",
            value=st.session_state.manual_time,
            max_chars=8,
            help="Ejemplo: 14:35:09",
        )

        col_start, col_stop, col_sync = st.columns(3)

        if col_start.button("Iniciar"):
            st.session_state.running = True
        if col_stop.button("Pausar"):
            st.session_state.running = False
        if col_sync.button("Sincronizar"):
            parsed_time = self.__parse_manual_time(st.session_state.manual_time)
            if parsed_time is None:
                st.error("Formato invalido. Usa HH:MM:SS con rangos 00-23:00-59:00-59.")
            else:
                self.__engine.synchronize(parsed_time)

        refresh_count = None
        if st.session_state.running:
            # Usa autorefresh cuando esta disponible y aplica fallback si no existe.
            if hasattr(st, "autorefresh"):
                refresh_count = st.autorefresh(interval=1000, key="clock_autorefresh")

        current_time = self.__engine.get_current_time()
        self.__render_analog_clock(current_time)

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

    @staticmethod
    def __parse_manual_time(raw_value: str) -> ClockTime | None:
        parts = raw_value.strip().split(":")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            return None

        hour, minute, second = (int(part) for part in parts)
        if hour < 0 or hour > 23:
            return None
        if minute < 0 or minute > 59:
            return None
        if second < 0 or second > 59:
            return None

        return ClockTime(hour=hour, minute=minute, second=second)

    def __render_analog_clock(self, current_time: ClockTime) -> None:
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_alpha(0.0)

        bezel_outer = plt.Circle((0, 0), 1.03, edgecolor="#8C949B", facecolor="#C7CCD1", linewidth=7)
        bezel_inner = plt.Circle((0, 0), 0.96, edgecolor="#626971", facecolor="#8A9199", linewidth=2)
        dial_base = plt.Circle((0, 0), 0.92, edgecolor="#D7DEE4", facecolor="#0F4E75", linewidth=2.2)
        dial_glow = plt.Circle((0, 0), 0.76, edgecolor="none", facecolor="#165F8E", alpha=0.55)
        ax.add_patch(bezel_outer)
        ax.add_patch(bezel_inner)
        ax.add_patch(dial_base)
        ax.add_patch(dial_glow)

        # Minuteria del borde: mas fina para acercar el estilo cronografo.
        for mark in range(60):
            angle = math.radians(90 - (mark * 6))
            inner_radius = 0.82 if mark % 5 == 0 else 0.855
            outer_radius = 0.90
            x_start = inner_radius * math.cos(angle)
            y_start = inner_radius * math.sin(angle)
            x_end = outer_radius * math.cos(angle)
            y_end = outer_radius * math.sin(angle)
            lw = 2.4 if mark % 5 == 0 else 0.9
            color = "#E5EBEF" if mark % 5 == 0 else "#9CB2C4"
            ax.plot([x_start, x_end], [y_start, y_end], color=color, linewidth=lw, solid_capstyle="round", zorder=4)

        # Indices horarios con acabado metalico claro.
        for hour_mark in range(12):
            angle = math.radians(90 - (hour_mark * 30))
            inner_radius = 0.69
            outer_radius = 0.80
            x_start = inner_radius * math.cos(angle)
            y_start = inner_radius * math.sin(angle)
            x_end = outer_radius * math.cos(angle)
            y_end = outer_radius * math.sin(angle)
            ax.plot([x_start, x_end], [y_start, y_end], color="#E7ECEF", linewidth=5.5, solid_capstyle="round", zorder=6)
            ax.plot([x_start, x_end], [y_start, y_end], color="#76818B", linewidth=1.2, alpha=0.75, zorder=7)

        self.__draw_subdial(ax, center=(-0.33, 0.28), radius=0.175)
        self.__draw_subdial(ax, center=(0.33, 0.28), radius=0.175)
        self.__draw_subdial(ax, center=(0.0, -0.34), radius=0.185)

        hour_angle = math.radians(90 - ((current_time.hour % 12) * 30 + current_time.minute * 0.5))
        minute_angle = math.radians(90 - (current_time.minute * 6 + current_time.second * 0.1))
        second_angle = math.radians(90 - current_time.second * 6)

        self.__draw_hand(ax, hour_angle, length=0.40, width=6.2, color="#DDE4EA")
        self.__draw_hand(ax, hour_angle, length=0.40, width=2.0, color="#6D7782")
        self.__draw_hand(ax, minute_angle, length=0.60, width=4.6, color="#DDE4EA")
        self.__draw_hand(ax, minute_angle, length=0.60, width=1.4, color="#6D7782")
        self.__draw_hand(ax, second_angle, length=0.73, width=1.7, color="#C9D5DF")
        self.__draw_hand(ax, second_angle, length=0.28, width=2.2, color="#9AA8B5")

        center_ring = plt.Circle((0, 0), 0.055, edgecolor="#CBD4DC", facecolor="#8D98A3", linewidth=2.0, zorder=20)
        center_core = plt.Circle((0, 0), 0.020, color="#4E5660", zorder=21)
        ax.add_patch(center_ring)
        ax.add_patch(center_core)

        ax.text(0, 0.44, "TISSOT", ha="center", va="center", fontsize=14, color="#F4F7FA", family="DejaVu Serif", fontweight="bold")
        ax.text(0, 0.36, "1853", ha="center", va="center", fontsize=9, color="#D8E4EF", family="DejaVu Sans")

        ax.set_xlim(-1.08, 1.08)
        ax.set_ylim(-1.08, 1.08)
        ax.set_aspect("equal")
        ax.axis("off")

        st.pyplot(fig, clear_figure=True, width="stretch")

    @staticmethod
    def __draw_hand(ax: Axes, angle: float, length: float, width: float, color: str) -> None:
        x = length * math.cos(angle)
        y = length * math.sin(angle)
        ax.plot([0, x], [0, y], color=color, linewidth=width, solid_capstyle="round", zorder=12)

    @staticmethod
    def __draw_subdial(ax: Axes, center: tuple[float, float], radius: float) -> None:
        cx, cy = center
        ring = plt.Circle((cx, cy), radius, edgecolor="#CAD6E0", facecolor="#1C628F", linewidth=2.0, zorder=3)
        fill = plt.Circle((cx, cy), radius * 0.78, edgecolor="none", facecolor="#0E4F78", zorder=3)
        ax.add_patch(ring)
        ax.add_patch(fill)

        for mark in range(12):
            angle = math.radians(90 - mark * 30)
            inner = radius * 0.65
            outer = radius * 0.90
            x0 = cx + inner * math.cos(angle)
            y0 = cy + inner * math.sin(angle)
            x1 = cx + outer * math.cos(angle)
            y1 = cy + outer * math.sin(angle)
            ax.plot([x0, x1], [y0, y1], color="#B8C7D3", linewidth=0.9, alpha=0.85, zorder=4)


def main() -> None:
    ui = ClockUI()
    ui.render()


if __name__ == "__main__":
    main()
