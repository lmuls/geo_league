import React, { useEffect, useRef, useState } from "react";
import styles from "../styles/NewGame.module.scss";

type FormData = {
  file?: File | null;
  date?: string;
};

type Alert = {
  id: number;
  type: "success" | "warning" | "error";
  message: string;
};

let alertId = 0;

export function NewGame() {
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [formData, setFormData] = useState<FormData>({ file: null, date: undefined });
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const addAlert = (type: Alert["type"], message: string) => {
    const id = alertId++;
    setAlerts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setAlerts((prev) => prev.filter((a) => a.id !== id));
    }, 4000);
  };

  const handleSave = async () => {
    if (!formData.file) {
      addAlert("warning", "Du må jo laste opp en fil da...");
      return;
    }
    if (!formData.date) {
      addAlert("warning", "Du må fylle inn en dato.");
      return;
    }

    setIsSaving(true);

    const fd = new FormData();
    fd.append("file", formData.file);
    fd.append("date", formData.date);

    const resp = await fetch(`${process.env.REACT_APP_DATABASE_URL}/new-game/`, {
      method: "POST",
      body: fd,
    });

    if (resp.status === 200 || resp.status === 201) {
      addAlert("success", "Spillet ble lagt til!");
      setFormData({ file: null, date: undefined });
      if (fileInputRef.current) fileInputRef.current.value = "";
    } else {
      addAlert("error", resp.statusText || "Noe gikk galt.");
    }

    setIsSaving(false);
  };

  return (
    <div className={styles.page}>
      <div className={styles.pageHeader}>
        <h1 className={styles.title}>Legg til spill</h1>
        <p className={styles.subtitle}>Last opp GeoGuessr-resultater</p>
      </div>

      <div className={styles.form}>
        <div className={styles.field}>
          <label className={styles.label}>Resultater (HTML-fil)</label>
          <label
            className={`${styles.uploadZone} ${formData.file ? styles.uploadZoneActive : ""}`}
          >
            <span className={styles.uploadIcon}>↑</span>
            {formData.file ? (
              <span className={styles.uploadFileName}>{formData.file.name}</span>
            ) : (
              <span className={styles.uploadLabel}>Klikk for å velge fil</span>
            )}
            <input
              ref={fileInputRef}
              className={styles.hiddenInput}
              type="file"
              accept=".html"
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, file: e.target.files?.[0] ?? null }))
              }
            />
          </label>
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="date">Dato</label>
          <input
            className={styles.dateInput}
            id="date"
            type="date"
            value={formData.date ?? ""}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, date: e.target.value }))
            }
          />
        </div>

        <button
          className={styles.submitButton}
          onClick={handleSave}
          disabled={isSaving}
        >
          {isSaving ? "Lagrer..." : "Send inn"}
        </button>
      </div>

      <div className={styles.alerts}>
        {alerts.map((a) => (
          <div
            key={a.id}
            className={`${styles.alert} ${
              a.type === "success"
                ? styles.alertSuccess
                : a.type === "warning"
                ? styles.alertWarning
                : styles.alertError
            }`}
          >
            {a.message}
          </div>
        ))}
      </div>
    </div>
  );
}
