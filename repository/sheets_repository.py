from __future__ import annotations

import base64
from datetime import date
from typing import Any, Dict, List, Optional

import requests
import streamlit as st


def _today_string() -> str:
    return date.today().isoformat()


def _config() -> Dict[str, str]:
    apps_script = st.secrets.get("apps_script", {})
    base_url = apps_script.get("web_app_url", "").strip()
    api_key = apps_script.get("api_key", "").strip()
    if not base_url:
        raise ValueError("`apps_script.web_app_url` が secrets に設定されていません。")
    if not api_key:
        raise ValueError("`apps_script.api_key` が secrets に設定されていません。")
    return {"base_url": base_url, "api_key": api_key}


def _request(action: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg = _config()
    body = {"action": action, "api_key": cfg["api_key"]}
    if payload:
        body.update(payload)
    response = requests.post(cfg["base_url"], json=body, timeout=20)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise ValueError(data.get("error", "Apps Script API error"))
    return data


@st.cache_data(ttl=30)
def get_library() -> List[Dict[str, str]]:
    data = _request("get_library")
    return data.get("library", [])


@st.cache_data(ttl=30)
def get_todays_menu(target_date: Optional[str] = None) -> List[Dict[str, str]]:
    date_key = target_date or _today_string()
    data = _request("get_daily_menu", {"date": date_key})
    return data.get("daily_menu", [])


def add_library_item(category: str, name: str, url: str, point: str) -> None:
    _request(
        "add_library_item",
        {"category": category, "name": name, "url": url, "point": point},
    )
    invalidate_cache()


def update_library_item(item_id: str, category: str, name: str, url: str, point: str) -> None:
    _request(
        "update_library_item",
        {"id": item_id, "category": category, "name": name, "url": url, "point": point},
    )
    invalidate_cache()


def delete_library_item(item_id: str) -> None:
    _request("delete_library_item", {"id": item_id})
    invalidate_cache()


def add_todays_menu_item(library_id: str, reps: str, sets: str, target_date: Optional[str] = None) -> None:
    date_key = target_date or _today_string()
    _request(
        "add_daily_menu_item",
        {"date": date_key, "library_id": library_id, "reps": reps, "sets": sets},
    )
    invalidate_cache()


def clear_todays_menu(target_date: Optional[str] = None) -> None:
    date_key = target_date or _today_string()
    _request("clear_daily_menu", {"date": date_key})
    invalidate_cache()


def delete_todays_menu_by_library_id(library_id: str) -> None:
    _request("delete_daily_menu_by_library_id", {"library_id": library_id})
    invalidate_cache()


def seed_defaults(library: List[Dict[str, str]], daily_menu: List[Dict[str, str]]) -> None:
    _request("seed_defaults", {"library": library, "daily_menu": daily_menu, "date": _today_string()})
    invalidate_cache()


# ★追加：ファイルをGAS経由でアップロードする処理
def upload_media(file_bytes: bytes, mime_type: str, file_name: str) -> str:
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    payload = {
        "file_base64": encoded,
        "mime_type": mime_type,
        "file_name": file_name
    }
    data = _request("upload_media", payload)
    return data.get("file_url", "")


def invalidate_cache() -> None:
    get_library.clear()
    get_todays_menu.clear()