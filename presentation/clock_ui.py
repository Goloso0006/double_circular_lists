from __future__ import annotations

import math
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import streamlit as st

from application.clock_engine import ClockEngine
from domain.value_objects.clock_time import ClockTime
from services.time_service import TimeService


class ClockUI:
    """Capa de presentacion con Streamlit para visualizar el reloj."""

    BACKGROUND_IMAGE_URL = "https://img.lovepik.com/photo/60179/9447.jpg_wh860.jpg"

    def __init__(self) -> None:
        if "engine" not in st.session_state:
            st.session_state.engine = ClockEngine(TimeService())
        if "running" not in st.session_state:
            st.session_state.running = False
        if "has_started" not in st.session_state:
            st.session_state.has_started = False

        self.__engine: ClockEngine = st.session_state.engine

    def render(self) -> None:
        st.set_page_config(page_title="Clock", page_icon=":clock9:", layout="centered")
        self.__apply_background_style()
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

        col_toggle, col_sync = st.columns(2)
        toggle_label = "Pausar" if st.session_state.running else ("Reanudar" if st.session_state.has_started else "Iniciar")

        if col_toggle.button(toggle_label):
            st.session_state.running = not st.session_state.running
            if st.session_state.running:
                st.session_state.has_started = True
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
        fig, ax = plt.subplots(figsize=(5.8, 9.0))
        fig.patch.set_alpha(0.0)

        self.__draw_case_and_strap(ax)

        bezel_outer = Circle((0, 0), 1.03, edgecolor="#8C949B", facecolor="#C7CCD1", linewidth=7, zorder=2)
        bezel_inner = Circle((0, 0), 0.96, edgecolor="#626971", facecolor="#8A9199", linewidth=2, zorder=3)
        dial_base = Circle((0, 0), 0.92, edgecolor="#D7DEE4", facecolor="#0F4E75", linewidth=2.2, zorder=3)
        dial_glow = Circle((0, 0), 0.76, edgecolor="none", facecolor="#165F8E", alpha=0.55, zorder=3)
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

        center_ring = Circle((0, 0), 0.055, edgecolor="#CBD4DC", facecolor="#8D98A3", linewidth=2.0, zorder=20)
        center_core = Circle((0, 0), 0.020, color="#4E5660", zorder=21)
        ax.add_patch(center_ring)
        ax.add_patch(center_core)

        ax.text(0, 0.44, "TISSOT", ha="center", va="center", fontsize=14, color="#F4F7FA", family="DejaVu Serif", fontweight="bold")
        ax.text(0, 0.36, "1853", ha="center", va="center", fontsize=9, color="#D8E4EF", family="DejaVu Sans")

        ax.set_xlim(-1.26, 1.34)
        ax.set_ylim(-2.08, 2.08)
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
        ring = Circle((cx, cy), radius, edgecolor="#CAD6E0", facecolor="#1C628F", linewidth=2.0, zorder=3)
        fill = Circle((cx, cy), radius * 0.78, edgecolor="none", facecolor="#0E4F78", zorder=3)
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

    @staticmethod
    def __draw_case_and_strap(ax: Axes) -> None:
        case = FancyBboxPatch(
            (-1.02, -1.18),
            2.04,
            2.36,
            boxstyle="round,pad=0.02,rounding_size=0.30",
            linewidth=2.8,
            edgecolor="#6A7179",
            facecolor="#B9C0C7",
            zorder=1,
        )
        ax.add_patch(case)

        lug_top = Rectangle((-0.30, 1.18), 0.60, 0.10, linewidth=0, facecolor="#9AA2AA", zorder=1)
        lug_bottom = Rectangle((-0.30, -1.28), 0.60, 0.10, linewidth=0, facecolor="#9AA2AA", zorder=1)
        ax.add_patch(lug_top)
        ax.add_patch(lug_bottom)

        strap_top = FancyBboxPatch(
            (-0.36, 1.28),
            0.72,
            0.78,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=2.0,
            edgecolor="#6D747D",
            facecolor="#BDC4CB",
            zorder=0,
        )
        strap_bottom = FancyBboxPatch(
            (-0.36, -2.06),
            0.72,
            0.78,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=2.0,
            edgecolor="#6D747D",
            facecolor="#BDC4CB",
            zorder=0,
        )
        ax.add_patch(strap_top)
        ax.add_patch(strap_bottom)

        for idx in range(6):
            y_top = 1.34 + idx * 0.11
            y_bottom = -1.95 + idx * 0.11
            top_link = Rectangle((-0.30, y_top), 0.60, 0.07, linewidth=0.8, edgecolor="#7E8790", facecolor="#D0D6DB", zorder=1)
            bottom_link = Rectangle((-0.30, y_bottom), 0.60, 0.07, linewidth=0.8, edgecolor="#7E8790", facecolor="#D0D6DB", zorder=1)
            ax.add_patch(top_link)
            ax.add_patch(bottom_link)

        upper_pusher = FancyBboxPatch(
            (1.03, 0.35),
            0.22,
            0.12,
            boxstyle="round,pad=0.01,rounding_size=0.04",
            linewidth=1.5,
            edgecolor="#6E767F",
            facecolor="#B4BBC3",
            zorder=1,
        )
        lower_pusher = FancyBboxPatch(
            (1.03, -0.47),
            0.22,
            0.12,
            boxstyle="round,pad=0.01,rounding_size=0.04",
            linewidth=1.5,
            edgecolor="#6E767F",
            facecolor="#B4BBC3",
            zorder=1,
        )
        crown = Circle((1.06, 0.0), 0.13, edgecolor="#656D76", facecolor="#AAB2BA", linewidth=2.0, zorder=1)
        crown_inner = Circle((1.06, 0.0), 0.07, edgecolor="#85909A", facecolor="#D1D7DC", linewidth=1.2, zorder=1)
        ax.add_patch(upper_pusher)
        ax.add_patch(lower_pusher)
        ax.add_patch(crown)
        ax.add_patch(crown_inner)

    def __apply_background_style(self) -> None:
        st.markdown(
            f"""
            <style>
                .stApp {{
                    background-image:
                        linear-gradient(rgba(6, 10, 16, 0.72), rgba(6, 10, 16, 0.72)),
                        url('{self.BACKGROUND_IMAGE_URL}');
                    background-size: cover;
                    background-position: center center;
                    background-attachment: fixed;
                    background-repeat: no-repeat;
                }}

                .block-container {{
                    background: rgba(8, 12, 18, 0.58);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 20px;
                    padding-top: 2rem;
                    padding-bottom: 2rem;
                    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.35);
                }}

                h1, h2, h3, p, label, div {{
                    color: #F2F5F8 !important;
                }}

                .stButton > button {{
                    background: rgba(15, 22, 31, 0.82);
                    color: #F4F7FA;
                    border: 1px solid rgba(255, 255, 255, 0.14);
                    border-radius: 12px;
                    padding: 0.55rem 1rem;
                }}

                .stButton > button:hover {{
                    border-color: rgba(255, 255, 255, 0.28);
                    background: rgba(25, 34, 46, 0.9);
                }}

                .stTextInput input {{
                    background: rgba(8, 13, 20, 0.75);
                    color: #F4F7FA;
                    border-radius: 10px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    ui = ClockUI()
    ui.render()


if __name__ == "__main__":
    main()
