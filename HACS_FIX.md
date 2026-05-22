# Fix für HACS Version-Fehler

## Problem
```
The version 0082aab for this integration can not be used with HACS.
```

## Ursache
HACS benötigt GitHub **Releases mit semantischer Versionierung** (z.B. `v1.0.0`), nicht nur Commits.

## Lösung

### Option 1: HACS neu laden (Schnell)

1. **HACS öffnen** in Home Assistant
2. **Integrations** anwählen
3. **eNet Smart Home** suchen
4. Menü (**⋮**) → **Reload** klicken
5. Warten Sie 30 Sekunden
6. Versuchen Sie erneut zu installieren

### Option 2: Manuell löschen & neu installieren

Falls Option 1 nicht funktioniert:

1. **HACS** → Integrations → eNet Smart Home
   - Klick **REMOVE FROM HACS**

2. **Custom repositories** → Suchen Sie "enet_homeassistant"
   - Klick **DELETE**

3. **Custom repositories** → **CREATE** (neu hinzufügen)
   - Repository: `https://github.com/sweh/enet_homeassistant`
   - Category: Integration
   - **CREATE**

4. **Integrations** → Suchen Sie "eNet Smart Home"
   - **INSTALL** klicken
   - Installation sollte jetzt funktionieren ✓

### Option 3: Terminal/SSH (für Profis)

Wenn Sie SSH-Zugang zu Home Assistant haben:

```bash
# In das custom_components Verzeichnis gehen
cd /config/custom_components

# eNet Ordner löschen
rm -rf enet

# Home Assistant neustarten
sudo systemctl restart homeassistant
```

Dann in HACS erneut versuchen.

## Was wurde geändert?

Wir haben ein GitHub **Release v1.0.0** erstellt:
- ✅ Git Tag `v1.0.0` erstellt
- ✅ Release auf GitHub publiziert
- ✅ Version in manifest.json (`1.0.0`) synchronisiert
- ✅ HACS kann Integration jetzt erkennen

## Jetzt sollte es funktionieren! ✓

Nach einem der obigen Schritte:

1. **HACS** → Integrations
2. Suche: **"eNet Smart Home"**
3. **INSTALL** klicken
4. Warten auf "Installation successful"
5. **Restart Home Assistant**
6. **Settings** → **Devices & Services** → **Create Integration**
7. Wähle **eNet Smart Home**
8. Geben Sie Ihre eNet-Credentials ein

## Weitere Hilfe

Wenn es immer noch nicht funktioniert:

1. Überprüfen Sie die **Logs**:
   - Settings → System → Logs
   - Suchen Sie nach "enet"

2. Überprüfen Sie **HACS Logs**:
   - HACS → ⋮ Menu → Download Logs

3. Eröffnen Sie ein **Issue** auf GitHub:
   - github.com/sweh/enet_homekit/issues

---

**Viel Erfolg! Die Integration sollte jetzt funktionieren.** 🚀
