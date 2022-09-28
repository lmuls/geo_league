import {Alert, AlertColor, Button, TextField} from "@mui/material";
import React, {useEffect, useState} from "react";
import styles from "../styles/NewGame.module.scss"
import Box from "@mui/material/Box";

const initialFormData = {
    game_id: undefined,
        date: undefined
}

enum Alerts {
    SUCCESS = "success",
    WARNING = "warning",
    ERROR = "error"
}

export function NewGame() {
    const [isSaving, setIsSaving] = useState<boolean>(false)
    const [formData, setFormData] = useState(initialFormData);
    const [alerts, setAlerts] = useState<JSX.Element[]>([])

    const createAlert = (type: AlertColor, message: string) => {
        const alert = (
            <Box m={2}>
                <Alert variant="filled" severity={type}>
                            {message}
                        </Alert>
            </Box>
        )

        setAlerts((alerts) => {
            return [...alerts, alert]
        })
    }


    useEffect(() => {


    }, [])

    useEffect(() => {
        const cycleAlerts = setInterval(() => {
        setAlerts((alerts) => {
                    if(alerts.length) {
                        alerts.shift()
                        return alerts
                    } else {
                        return []
                    }
                })
            }, 2000)

        return () => {
            clearInterval(cycleAlerts)
        }
    })


    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({
            ...formData,
           [e.target.name]: e.target.value})
    }

    const handleSave = async () => {
        setIsSaving(true)

        if(formData.game_id === undefined || formData.game_id === "") {
            createAlert(Alerts.WARNING, "Du må jo fylle inn en gameid da...")

            return
        }

        if(formData.date === undefined) {
            createAlert(Alerts.WARNING, "Du må fylle inn en dato. Ellers får vi ikke holdt oversikt, og da blir det dårlig stemning")
            return
        }
        
        const resp = await fetch('/new-game/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
              },
            body: JSON.stringify(formData)
        })

        if(resp.status === 201) {
            createAlert(Alerts.SUCCESS, "Game was accepted, hope you played well")
            setFormData(initialFormData)
            setIsSaving(false)
        } else {
            createAlert(Alerts.ERROR, resp.statusText)
            setIsSaving(false)
        }
    }

    return (
        <div id={styles.component}>
            <h1>Send inn nytt spill</h1>
            <form>
                <TextField name="game_id" onChange={(e) => {
                        handleChange(e)
                    }} id="outlined-basic" label="Game ID" variant="outlined" />
                <TextField
                name="date"
                    id="date"
                    label="Dato"
                    onChange={(e) => {
                        handleChange(e)
                    }}
                    type="date"
                    defaultValue="today"
                    sx={{ width: 220 }}
                    InputLabelProps={{
                    shrink: true,
                    }}
                />
                <Button onClick={handleSave} variant="contained">Send inn</Button>
            </form>
            <div className={styles.alerts}>
                {alerts}
            </div>
        </div>
    )
}