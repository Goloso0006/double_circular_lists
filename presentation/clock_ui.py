from __future__ import annotations

import time

import streamlit as st

from application.clock_engine import ClockEngine
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
        st.set_page_config(page_title="Circular Analog Clock", page_icon="🕰️", layout="centered")
        st.title("Reloj Analogico con Lista Circular Doble")
        st.caption("Simulacion orientada a objetos con estructura de datos circular")

        col_start, col_stop, col_sync = st.columns(3)

        if col_start.button("Iniciar"):
            st.session_state.running = True
        if col_stop.button("Pausar"):
            st.session_state.running = False
        if col_sync.button("Sincronizar"):
            self.__engine.synchronize_with_system_time()

        current_time = self.__engine.get_current_time()
        st.metric(label="Hora 24h", value=current_time.to_24_hour_format())
        st.metric(label="Hora 12h", value=current_time.to_12_hour_format())

        if st.button("Retroceder 1 segundo"):
            self.__engine.move_backward_one_second()
            st.rerun()

        # Se usa rerun para simular avance continuo del reloj dentro del ciclo de Streamlit.
        if st.session_state.running:
            time.sleep(1)
            self.__engine.tick()
            st.rerun()


def main() -> None:
    ui = ClockUI()
    ui.render()


if __name__ == "__main__":
    main()
