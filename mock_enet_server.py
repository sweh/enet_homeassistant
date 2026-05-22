"""
Mock eNet Server for testing the Home Assistant integration.

This simulates an eNet Smart Home server for development and testing
without needing access to a real eNet device.

Usage:
    python3 mock_enet_server.py

Then test with:
    python3 -c "from custom_components.enet.enet import EnetClient; 
                client = EnetClient('http://localhost:5000', 'admin', 'password');
                client.simple_login();
                print(client.get_devices())"
"""

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Mock data structures
mock_devices = [
    {
        "uid": "device_001",
        "typeID": "DVT_SJA1",  # Switch actuator
        "installationArea": "Living Room",
        "batteryState": "OK",
        "isSoftwareUpdateAvailable": False,
        "deviceChannelConfigurationGroups": [
            {
                "deviceChannels": [
                    {
                        "no": 1,
                        "channelTypeID": "CT_1F03",  # Blind
                        "effectArea": "Main Blind",
                        "outputDeviceFunctions": [
                            {
                                "uid": "func_001",
                                "typeID": "FT_INBAv3.CAPBP",
                                "currentValues": [
                                    {
                                        "valueTypeID": "VT_SCALING_RANGE_0_100_DEF_0",
                                        "value": 50
                                    }
                                ]
                            }
                        ],
                        "inputDeviceFunctions": [
                            {
                                "uid": "ifunc_001",
                                "typeID": "FT_INBAv3.SAPBP"
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        "uid": "device_002",
        "typeID": "DVT_DA1M",  # Dimmer
        "installationArea": "Bedroom",
        "batteryState": "OK",
        "isSoftwareUpdateAvailable": False,
        "deviceChannelConfigurationGroups": [
            {
                "deviceChannels": [
                    {
                        "no": 1,
                        "channelTypeID": "CT_1F02",  # Dimmer
                        "effectArea": "Ceiling Light",
                        "outputDeviceFunctions": [
                            {
                                "uid": "func_002",
                                "typeID": "FT_INDA.ADV",
                                "currentValues": [
                                    {
                                        "valueTypeID": "VT_SCALING_RANGE_0_100_DEF_0",
                                        "value": 75
                                    }
                                ]
                            }
                        ],
                        "inputDeviceFunctions": [
                            {
                                "uid": "ifunc_002",
                                "typeID": "FT_INDA.ASC"
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        "uid": "device_003",
        "typeID": "DVT_SF1S",  # Light sensor
        "installationArea": "Garden",
        "batteryState": "OK",
        "isSoftwareUpdateAvailable": False,
        "deviceChannelConfigurationGroups": [
            {
                "deviceChannels": [
                    {
                        "no": 1,
                        "channelTypeID": "CT_1F18",  # Light sensor
                        "effectArea": "Outdoor Light Level",
                        "outputDeviceFunctions": [
                            {
                                "uid": "func_003",
                                "typeID": "FT_INThScS.CAVTH1",
                                "currentValues": [
                                    {
                                        "valueTypeID": "VT_SCALING_RANGE_0_100_DEF_0",
                                        "value": 85000
                                    }
                                ]
                            }
                        ],
                        "inputDeviceFunctions": []
                    }
                ]
            }
        ]
    }
]

mock_locations = {
    "device_001": "Home:Living Room",
    "device_002": "Home:Bedroom",
    "device_003": "Home:Garden"
}

# Store for device values (for state persistence)
device_values = {}


@app.route("/jsonrpc/management", methods=["POST"])
def management():
    """Handle management requests (login, etc)."""
    data = request.get_json()
    method = data.get("method")
    
    if method == "userLogin":
        params = data.get("params", {})
        if params.get("userName") == "admin" and params.get("userPassword") == "password":
            return jsonify({
                "jsonrpc": "2.0",
                "result": {"sessionID": "mock_session_123"},
                "id": data.get("id")
            })
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -29998, "message": "Invalid credentials"},
                "id": data.get("id")
            })
    
    elif method == "setClientRole":
        return jsonify({
            "jsonrpc": "2.0",
            "result": {},
            "id": data.get("id")
        })
    
    elif method == "getAccount":
        return jsonify({
            "jsonrpc": "2.0",
            "result": {"accountName": "admin", "accountRole": "CR_VISU"},
            "id": data.get("id")
        })
    
    return jsonify({
        "jsonrpc": "2.0",
        "error": {"code": -1, "message": "Unknown method"},
        "id": data.get("id")
    })


@app.route("/jsonrpc/visualization", methods=["POST"])
def visualization():
    """Handle visualization requests (devices, values, etc)."""
    data = request.get_json()
    method = data.get("method")
    
    if method == "getLocations":
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "locations": [
                    {
                        "locationUID": "loc_001",
                        "name": "Home",
                        "deviceUIDs": [
                            {"deviceUID": "device_001"},
                            {"deviceUID": "device_002"},
                            {"deviceUID": "device_003"}
                        ],
                        "childLocations": []
                    }
                ]
            },
            "id": data.get("id")
        })
    
    elif method == "getDevicesWithParameterFilter":
        return jsonify({
            "jsonrpc": "2.0",
            "result": {"devices": mock_devices},
            "id": data.get("id")
        })
    
    elif method == "getCurrentValuesFromOutputDeviceFunction":
        # Return mock current value
        func_uid = data.get("params", {}).get("deviceFunctionUID")
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "currentValues": [
                    {
                        "valueTypeID": "VT_SCALING_RANGE_0_100_DEF_0",
                        "value": device_values.get(func_uid, 50)
                    }
                ]
            },
            "id": data.get("id")
        })
    
    elif method == "callInputDeviceFunction":
        # Store the new value
        func_uid = data.get("params", {}).get("deviceFunctionUID")
        values = data.get("params", {}).get("values", [])
        if values:
            device_values[func_uid] = values[0].get("value", 0)
        
        return jsonify({
            "jsonrpc": "2.0",
            "result": {},
            "id": data.get("id")
        })
    
    elif method == "executeAction":
        return jsonify({
            "jsonrpc": "2.0",
            "result": {},
            "id": data.get("id")
        })
    
    return jsonify({
        "jsonrpc": "2.0",
        "error": {"code": -1, "message": "Unknown method"},
        "id": data.get("id")
    })


if __name__ == "__main__":
    print("Starting Mock eNet Server on http://localhost:5000")
    print("Credentials: admin / password")
    print("\nMock devices:")
    for device in mock_devices:
        print(f"  - {device['installationArea']} ({device['typeID']})")
    
    app.run(host="localhost", port=5000, debug=True)
