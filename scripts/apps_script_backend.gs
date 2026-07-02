const WORKOUT_SHEET = "workout_menu";
const DAILY_SHEET = "daily_menu";
const LIBRARY_HEADERS = ["id", "category", "name", "url", "point", "updated_at"];
const DAILY_HEADERS = ["id", "date", "library_id", "reps", "sets", "order_no", "updated_at"];

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents || "{}");
    verifyApiKey(payload.api_key);
    ensureHeaders();

    const action = payload.action;
    let result = {};

    if (action === "get_library") {
      result = { library: getRecords(WORKOUT_SHEET, LIBRARY_HEADERS) };
    } else if (action === "get_daily_menu") {
      const date = payload.date;
      const rows = getRecords(DAILY_SHEET, DAILY_HEADERS).filter((r) => r.date === date);
      result = { daily_menu: rows };
    } else if (action === "add_library_item") {
      appendRecord(WORKOUT_SHEET, LIBRARY_HEADERS, {
        id: Utilities.getUuid(),
        category: payload.category || "",
        name: payload.name || "",
        url: payload.url || "",
        point: payload.point || "",
        updated_at: todayString(),
      });
    } else if (action === "update_library_item") {
      updateById(WORKOUT_SHEET, LIBRARY_HEADERS, payload.id, {
        category: payload.category || "",
        name: payload.name || "",
        url: payload.url || "",
        point: payload.point || "",
        updated_at: todayString(),
      });
    } else if (action === "delete_library_item") {
      deleteById(WORKOUT_SHEET, LIBRARY_HEADERS, payload.id);
      deleteDailyByLibraryId(payload.id);
    } else if (action === "add_daily_menu_item") {
      const date = payload.date || todayString();
      const current = getRecords(DAILY_SHEET, DAILY_HEADERS).filter((r) => r.date === date);
      appendRecord(DAILY_SHEET, DAILY_HEADERS, {
        id: Utilities.getUuid(),
        date: date,
        library_id: payload.library_id || "",
        reps: payload.reps || "",
        sets: payload.sets || "",
        order_no: String(current.length + 1),
        updated_at: todayString(),
      });
    } else if (action === "clear_daily_menu") {
      clearDailyByDate(payload.date || todayString());
    } else if (action === "delete_daily_menu_by_library_id") {
      deleteDailyByLibraryId(payload.library_id || "");
    } else if (action === "seed_defaults") {
      seedDefaults(payload.library || [], payload.daily_menu || [], payload.date || todayString());
    } else {
      return jsonResponse({ ok: false, error: "Unknown action" });
    }

    return jsonResponse({ ok: true, ...result });
  } catch (err) {
    return jsonResponse({ ok: false, error: String(err) });
  }
}

function verifyApiKey(apiKey) {
  const expected = PropertiesService.getScriptProperties().getProperty("APP_API_KEY");
  if (!expected) throw new Error("APP_API_KEY is not configured");
  if (apiKey !== expected) throw new Error("Unauthorized");
}

function todayString() {
  return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd");
}

function getSheet(name) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(name);
  if (!sheet) sheet = ss.insertSheet(name);
  return sheet;
}

function ensureHeaders() {
  ensureHeaderRow(WORKOUT_SHEET, LIBRARY_HEADERS);
  ensureHeaderRow(DAILY_SHEET, DAILY_HEADERS);
}

function ensureHeaderRow(sheetName, headers) {
  const sheet = getSheet(sheetName);
  const firstRow = sheet.getRange(1, 1, 1, headers.length).getValues()[0];
  const matched = headers.every((h, i) => firstRow[i] === h);
  if (!matched) {
    sheet.clearContents();
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  }
}

function getRecords(sheetName, headers) {
  const sheet = getSheet(sheetName);
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return [];
  const values = sheet.getRange(2, 1, lastRow - 1, headers.length).getValues();
  return values.map((row) => {
    const rec = {};
    headers.forEach((h, i) => (rec[h] = String(row[i] ?? "")));
    return rec;
  });
}

function appendRecord(sheetName, headers, record) {
  const sheet = getSheet(sheetName);
  sheet.appendRow(headers.map((h) => record[h] || ""));
}

function replaceRecords(sheetName, headers, records) {
  const sheet = getSheet(sheetName);
  sheet.clearContents();
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  if (!records.length) return;
  const rows = records.map((rec) => headers.map((h) => rec[h] || ""));
  sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
}

function updateById(sheetName, headers, id, patch) {
  const records = getRecords(sheetName, headers);
  const updated = records.map((r) => (r.id === id ? { ...r, ...patch } : r));
  replaceRecords(sheetName, headers, updated);
}

function deleteById(sheetName, headers, id) {
  const records = getRecords(sheetName, headers).filter((r) => r.id !== id);
  replaceRecords(sheetName, headers, records);
}

function clearDailyByDate(date) {
  const records = getRecords(DAILY_SHEET, DAILY_HEADERS).filter((r) => r.date !== date);
  replaceRecords(DAILY_SHEET, DAILY_HEADERS, records);
}

function deleteDailyByLibraryId(libraryId) {
  const records = getRecords(DAILY_SHEET, DAILY_HEADERS).filter((r) => r.library_id !== libraryId);
  replaceRecords(DAILY_SHEET, DAILY_HEADERS, records);
}

function seedDefaults(library, dailyMenu, date) {
  const mappedLibrary = library.map((item) => ({
    id: Utilities.getUuid(),
    category: item.category || "",
    name: item.name || "",
    url: item.url || "",
    point: item.point || "",
    updated_at: todayString(),
  }));
  const nameToId = {};
  mappedLibrary.forEach((r) => (nameToId[r.name] = r.id));

  const mappedDaily = dailyMenu
    .map((item, idx) => ({
      id: Utilities.getUuid(),
      date: date,
      library_id: nameToId[item.name] || "",
      reps: item.reps || "",
      sets: item.sets || "",
      order_no: String(idx + 1),
      updated_at: todayString(),
    }))
    .filter((r) => r.library_id);

  replaceRecords(WORKOUT_SHEET, LIBRARY_HEADERS, mappedLibrary);
  replaceRecords(DAILY_SHEET, DAILY_HEADERS, mappedDaily);
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}
