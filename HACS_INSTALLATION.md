# Installation über HACS (Home Assistant Community Store)

## Voraussetzungen

1. **Home Assistant** ist installiert und läuft
   - Docker: `homeassistant/home-assistant:latest`
   - Or: Bare Metal/NAS Installation

2. **HACS** ist installiert
   - [HACS Installation Guide](https://hacs.xyz/docs/setup/prerequisites)

## Installationsschritte

### Schritt 1: Repository als Custom Repository hinzufügen

1. Öffne **Home Assistant**
2. Gehe zu: **HACS** → Menu (☰) → **Custom repositories**
   
   ![Step 1](https://user-images.githubusercontent.com/placeholder/1.png)

3. Geben Sie folgende Details ein:
   - **Repository URL**: `https://github.com/sweh/enet_homeassistant`
   - **Category**: `Integration`

4. Klick **CREATE**

   ![Step 2](https://user-images.githubusercontent.com/placeholder/2.png)

### Schritt 2: Integration installieren

1. Gehe zu **HACS** → **Integrations**
2. Suche nach **"eNet"** oder **"eNet Smart Home"**
3. Klick auf die Integration
4. Klick **INSTALL**

   ![Step 3](https://user-images.githubusercontent.com/placeholder/3.png)

5. Warte, bis die Installation abgeschlossen ist
6. **Restart Home Assistant**
   - Settings → System → System Information → Restart

### Schritt 3: Integration konfigurieren

Nachdem Home Assistant neu gestartet ist:

1. Gehe zu: **Settings** → **Devices & Services**
2. Klick **+ CREATE INTEGRATION**
3. Suche nach **"eNet Smart Home"**
4. Klick auf die Integration

   ![Step 4](https://user-images.githubusercontent.com/placeholder/4.png)

5. Geben Sie Ihre eNet Server-Details ein:
   - **Host**: `http://10.0.1.12` (IP oder Hostname deines eNet Servers)
   - **Username**: `admin` (oder dein Benutzername)
   - **Password**: (dein eNet Passwort)
   
   ![Step 5](https://user-images.githubusercontent.com/placeholder/5.png)

6. Klick **SUBMIT**

7. Home Assistant sucht automatisch nach Geräten
   - Warte, bis die Geräte erkannt wurden
   - Es sollten alle Rollläden, Lichter und Sensoren erscheinen

### Schritt 4: Geräte überprüfen

1. Gehe zu: **Settings** → **Devices & Services**
2. Suche nach **"eNet Smart Home"**
3. Klick auf die Integration
4. Alle erkannten Geräte sollten sichtbar sein:
   - **Cover**: Rollläden/Jalousien
   - **Light**: Lichter und Dimmer
   - **Sensor**: Lichtsensoren und Temperatursensoren

   ![Step 6](https://user-images.githubusercontent.com/placeholder/6.png)

## Troubleshooting

### "Cannot Connect to eNet"

**Problem**: Integration zeigt Verbindungsfehler

**Lösungen**:
1. Überprüfe die **IP-Adresse/Hostname** des eNet Servers
   ```bash
   ping 10.0.1.12
   ```

2. Überprüfe **Benutzername und Passwort**
   - Standard-Benutzer: `admin`
   - Passwort ist das eNet Server-Passwort

3. Überprüfe **Netzwerk-Konnektivität**
   - HA und eNet Server müssen im gleichen Netzwerk sein (oder VPN)
   - Firewall-Regeln überprüfen (Port sollte offen sein)

4. Überprüfe **eNet Server Status**
   - Ist der eNet Server online?
   - Zugang über Web-Browser möglich? `http://10.0.1.12`

### "No Devices Found"

**Problem**: Integration verbunden, aber keine Geräte erkannt

**Lösungen**:
1. Überprüfe **Gerätekonfiguration** im eNet Server
   - Sind Geräte im eNet System konfiguriert?
   - Sind Kanäle (Channels) aktiv?

2. Überprüfe **Gerätetypen**
   - Nur bestimmte Gerätetypen werden unterstützt
   - Siehe [Supported Devices](#unterstützte-geräte)

3. **Logs überprüfen**:
   - Settings → System → Logs
   - Suche nach "enet"
   - Schaue nach Error-Meldungen

### "Entity Not Updating"

**Problem**: Geräte sind sichtbar, aber aktualisieren ihren Status nicht

**Lösungen**:
1. Überprüfe **Netzwerkkonnektivität**
   - Ping zum eNet Server: `ping 10.0.1.12`

2. **Firewall/Router**
   - Überprüfe, ob der Port offen ist
   - NAT/Port-Forwarding korrekt konfiguriert

3. **Integration neustart**:
   - Settings → Devices & Services
   - Klick auf eNet Integration → Optionen
   - Klick **RELOAD**

## Supported Devices

### Rollläden (Cover)
| Model | Typ | Unterstützung |
|-------|-----|--------------|
| Jung Jalousie-Aktor | CT_1F03 | ✓ Vollständig |
| Gira Blinds | CT_1F03 | ✓ Vollständig |

**Befehle**:
- Open (öffnen)
- Close (schließen)
- Set position (Position setzen 0-100%)

### Lichter & Dimmer (Light)
| Model | Typ | Unterstützung |
|-------|-----|--------------|
| Switch Actuator | CT_1F01 | ✓ An/Aus |
| Dimmer Actuator | CT_1F02 | ✓ An/Aus + Helligkeit |
| Various DIN Rail | CT_1F05/08/09 | ✓ An/Aus + Helligkeit |

**Features**:
- On/Off Steuerung
- Helligkeitsregelung (0-100%)

### Sensoren (Sensor)
| Model | Typ | Messwert |
|-------|-----|----------|
| Light Sensor | CT_1F18 | Illuminance (Lux) |
| Temperature Sensor | CT_1F19 | Temperatur (°C) |
| TADO Sensor | CT_TADO_* | Temperatur (°C) |

**Readings**:
- Lichtstärke: 0-100000+ Lux
- Temperatur: -20 bis +60°C

## Update / Deinstallation

### Update der Integration

1. Gehe zu **HACS** → **Integrations**
2. Suche nach **"eNet Smart Home"**
3. Wenn ein Update verfügbar ist, wird es angezeigt
4. Klick **UPDATE**
5. **Restart Home Assistant**

### Integration deinstallieren

1. Gehe zu **Settings** → **Devices & Services**
2. Klick auf die eNet Integration
3. Klick auf **DELETE** (Trash-Icon)
4. Bestätige die Löschung

5. Optional: Repository aus HACS entfernen
   - HACS → Integrations → eNet
   - Klick **Remove from HACS**

## Erste Schritte nach Installation

### 1. Automationen erstellen

```yaml
- alias: "Rollläden schließen bei Sonnenuntergang"
  trigger:
    - platform: sun
      event: sunset
  action:
    - service: cover.close_cover
      target:
        entity_id: cover.jalousie_living_room
```

### 2. Dashboard anpassen

1. Gehe zu **Dashboard**
2. Klick **EDIT DASHBOARD**
3. Füge Karten für deine eNet-Geräte hinzu
   - Cover Card für Rollläden
   - Light Card für Lichter
   - Sensor Card für Messwerte

### 3. Automation für Lichter

```yaml
- alias: "Licht an wenn jemand nach Hause kommt"
  trigger:
    - platform: zone
      entity_id: person.you
      zone: zone.home
      event: enter
  action:
    - service: light.turn_on
      target:
        entity_id: light.ceiling_light
      data:
        brightness: 200
```

## Support & Weitere Infos

- **GitHub Issues**: [github.com/sweh/enet_homeassistant/issues](https://github.com/sweh/enet_homeassistant/issues)
- **eNet Docs**: [enet-smarthome.com](https://www.enet-smarthome.com/de/ueber-enet/)
- **Home Assistant Docs**: [developers.home-assistant.io](https://developers.home-assistant.io/)

---

## Quick Reference

```
Installation:
1. HACS → Custom repositories → Add: github.com/sweh/enet_homeassistant
2. HACS → Integrations → Search "eNet" → Install
3. Restart Home Assistant
4. Settings → Devices & Services → Create Integration → eNet Smart Home
5. Enter eNet Server credentials
6. Geräte werden automatisch erkannt ✓

Troubleshooting:
- Cannot connect? → Check IP, username, password, network connectivity
- No devices? → Check eNet configuration, supported device types
- Not updating? → Check firewall, restart integration via RELOAD
```

**Fertig! Deine eNet-Geräte sind jetzt in Home Assistant verfügbar! 🎉**
