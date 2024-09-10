import { Alert, AlertColor, Button, TextField, styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import styles from "../styles/NewGame.module.scss";
import Box from "@mui/material/Box";
import { log } from "console";

type FormData = {
  file?: File | null;
  date?: Date;
};

const initialFormData = {
  file: null,
  date: undefined,
};

let keyInc = 0;

enum Alerts {
  SUCCESS = "success",
  WARNING = "warning",
  ERROR = "error",
}

export function NewGame() {
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [alerts, setAlerts] = useState<JSX.Element[]>([]);

  const createAlert = (type: AlertColor, message: string) => {
    const alert = (
      <Box m={2} key={keyInc++}>
        <Alert variant="filled" severity={type}>
          {message}
        </Alert>
      </Box>
    );

    setAlerts((alerts) => {
      return [...alerts, alert];
    });
  };

  useEffect(() => {}, []);

  useEffect(() => {
    const cycleAlerts = setInterval(() => {
      setAlerts((alerts) => {
        if (alerts.length) {
          alerts.shift();
          return alerts;
        } else {
          return [];
        }
      });
    }, 2000);

    return () => {
      clearInterval(cycleAlerts);
    };
  });

  console.log(formData);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSave = async () => {
    setIsSaving(true);

    if (formData.file === undefined || formData.file === null) {
      createAlert(Alerts.WARNING, "Du må jo laste opp en fil da...");

      return;
    }

    if (formData.date === undefined) {
      createAlert(
        Alerts.WARNING,
        "Du må fylle inn en dato. Ellers får vi ikke holdt oversikt, og da blir det dårlig stemning"
      );
      return;
    }

    const fd = new FormData();
    fd.append("file", formData.file);
    fd.append("date", formData.date.toString());

    const resp = await fetch(
      `${process.env.REACT_APP_DATABASE_URL}/new-game/`,
      {
        method: "POST",
        body: fd,
      }
    );

    if (resp.status === 200 || resp.status === 201) {
      createAlert(Alerts.SUCCESS, "Game was accepted, hope you played well");
      setFormData(initialFormData);
      setIsSaving(false);
    } else {
      createAlert(Alerts.ERROR, resp.statusText);
      setIsSaving(false);
    }
  };

  return (
    <div id={styles.component}>
      <h1>Send inn nytt spill</h1>
      <form>
        <Button
          component="label"
          role={undefined}
          variant="contained"
          tabIndex={-1}
        >
          Upload files
          <VisuallyHiddenInput
            type="file"
            onChange={(event) => {
              setFormData((prev) => ({
                ...prev,
                file: event.target.files?.[0],
              }));
            }}
          />
        </Button>

        <TextField
          name="date"
          id="date"
          label="Dato"
          onChange={(e) => {
            handleChange(e);
          }}
          type="date"
          defaultValue="today"
          sx={{ width: 220 }}
          InputLabelProps={{
            shrink: true,
          }}
        />
        <Button onClick={handleSave} variant="contained">
          Send inn
        </Button>
      </form>
      <div className={styles.alerts}>{alerts}</div>
    </div>
  );
}

const VisuallyHiddenInput = styled("input")({
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  height: 1,
  overflow: "hidden",
  position: "absolute",
  bottom: 0,
  left: 0,
  whiteSpace: "nowrap",
  width: 1,
});
