import streamlit as st
from copy import deepcopy
from uuid import uuid4

from defaults import DEFAULT_LIBRARY, DEFAULT_TODAYS_MENU
from repository import sheets_repository


def init_session_state() -> None:
    refresh_session_state_from_storage()


def refresh_session_state_from_storage() -> None:
    try:
        library = sheets_repository.get_library()
        todays_menu_raw = sheets_repository.get_todays_menu()

        if not library:
            st.session_state["library"] = deepcopy(DEFAULT_LIBRARY)
            st.session_state["todays_menu"] = deepcopy(DEFAULT_TODAYS_MENU)
            return

        library_by_id = {item["id"]: item for item in library}
        todays_menu = []
        for item in todays_menu_raw:
            lib = library_by_id.get(item.get("library_id", ""))
            if not lib:
                continue
            todays_menu.append(
                {
                    "id": item["id"],
                    "library_id": item["library_id"],
                    "name": lib["name"],
                    "reps": item["reps"],
                    "sets": item["sets"],
                    "order_no": item.get("order_no", ""),
                }
            )

        st.session_state["library"] = library
        st.session_state["todays_menu"] = todays_menu
    except Exception:
        # Fallback until sheets credentials are configured.
        if "library" not in st.session_state:
            fallback_library = []
            for item in deepcopy(DEFAULT_LIBRARY):
                fallback_library.append(
                    {
                        "id": str(uuid4()),
                        "category": item["category"],
                        "name": item["name"],
                        "url": item["url"],
                        "point": item["point"],
                        "updated_at": "",
                    }
                )
            st.session_state["library"] = fallback_library
        if "todays_menu" not in st.session_state:
            name_to_library = {item["name"]: item for item in st.session_state["library"]}
            fallback_todays = []
            for item in deepcopy(DEFAULT_TODAYS_MENU):
                lib = name_to_library.get(item["name"])
                if not lib:
                    continue
                fallback_todays.append(
                    {
                        "id": str(uuid4()),
                        "library_id": lib["id"],
                        "name": item["name"],
                        "reps": item["reps"],
                        "sets": item["sets"],
                        "order_no": "",
                    }
                )
            st.session_state["todays_menu"] = fallback_todays
