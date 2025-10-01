import os 
 
html_content = '''<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>WhatsApp Drive Bot</title> 
    <style> 
        * { margin: 0; padding: 0; box-sizing: border-box; } 
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            padding: 20px; 
        } 
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            overflow: hidden; 
        } 
        .header { 
            background: linear-gradient(135deg, #25D366, #128C7E); 
            color: white; 
            padding: 30px; 
            text-align: center; 
        } 
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px; 
            font-weight: 300; 
        } 
        .header p { 
            font-size: 1.1em; 
            opacity: 0.9; 
            font-weight: 300; 
        } 
        .content { 
            padding: 40px; 
        } 
        .status-card { 
            background: #f8f9fa; 
            border-radius: 10px; 
            padding: 25px; 
            margin-bottom: 30px; 
            border-left: 5px solid #25D366; 
        } 
        .status-card h3 { 
            color: #333; 
            margin-bottom: 20px; 
            font-size: 1.3em; 
        } 
        .status-item { 
            display: flex; 
            justify-content: space-between; 
            margin: 12px 0; 
            padding: 10px 0; 
            border-bottom: 1px solid #e9ecef; 
        } 
        .status-label { 
            font-weight: 600; 
            color: #555; 
        } 
        .status-value { 
            font-weight: 600; 
        } 
        .connected { color: #28a745; } 
        .disconnected { color: #dc3545; } 
        .running { color: #28a745; } 
        .stopped { color: #6c757d; } 
        .btn-group { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; 
            margin: 25px 0; 
        } 
        .btn { 
            padding: 15px 25px; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            font-weight: 600; 
            cursor: pointer; 
            transition: all 0.3s ease; 
            text-align: center; 
        } 
        .btn-primary { 
            background: #25D366; 
            color: white; 
        } 
        .btn-primary:hover { 
            background: #128C7E; 
            transform: translateY(-2px); 
            box-shadow: 0 5px 15px rgba(0,0,0,0.2); 
        } 
        .btn-secondary { 
            background: #6c757d; 
            color: white; 
        } 
        .btn-secondary:hover { 
            background: #545b62; 
            transform: translateY(-2px); 
        } 
        .btn-danger { 
            background: #dc3545; 
            color: white; 
        } 
        .btn-danger:hover { 
            background: #c82333; 
            transform: translateY(-2px); 
        } 
    </style> 
</head> 
<body> 
    <div class="container"> 
        <div class="header"> 
            <h1>WhatsApp Drive Bot</h1> 
            <p>Automatically save WhatsApp files to Google Drive</p> 
        </div> 
        <div class="content"> 
            <div class="status-card"> 
                <h3>Bot Status</h3> 
                <div id="statusContent"> 
                    <div class="status-item"> 
                        <span class="status-label">Bot Status:</span> 
                        <span id="botStatus" class="status-value stopped">Loading...</span> 
                    </div> 
                    <div class="status-item"> 
                        <span class="status-label">WhatsApp Connection:</span> 
                        <span id="whatsappStatus" class="status-value disconnected">Disconnected</span> 
                    </div> 
                    <div class="status-item"> 
                        <span class="status-label">Google Drive Connection:</span> 
                        <span id="driveStatus" class="status-value disconnected">Disconnected</span> 
                    </div> 
                    <div class="status-item"> 
                        <span class="status-label">Last Update:</span> 
                        <span id="lastUpdate" class="status-value">-</span> 
                    </div> 
                </div> 
            </div> 
            <div class="btn-group"> 
                <button class="btn btn-primary" onclick="startBot()">Start Bot</button> 
                <button class="btn btn-danger" onclick="stopBot()">Stop Bot</button> 
                <button class="btn btn-secondary" onclick="getQRCode()">Get QR Code</button> 
                <button class="btn btn-secondary" onclick="refreshStatus()">Refresh Status</button> 
            </div> 
            <div id="qrSection" style="display: none; text-align: center; margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 10px;"> 
                <h3>Scan QR Code</h3> 
                <p>Open WhatsApp -> Linked Devices -> Scan QR Code</p> 
                <div id="qrCode" style="padding: 20px; background: white; border-radius: 5px; margin: 10px auto; max-width: 300px; display: none;">QR Code will appear here</div> 
            </div> 
        </div> 
    </div> 
    <script> 
        async function refreshStatus() { 
            try { 
                const response = await fetch('/status'); 
                const status = await response.json(); 
ECHO is on.
                document.getElementById('botStatus').textContent = status.is_running ? 'Running' : 'Stopped'; 
                document.getElementById('botStatus').className = status.is_running ? 'status-value running' : 'status-value stopped'; 
ECHO is on.
                document.getElementById('whatsappStatus').textContent = status.whatsapp_status; 
                document.getElementById('whatsappStatus').className = status.whatsapp_status === 'connected' ? 'status-value connected' : 'status-value disconnected'; 
ECHO is on.
                document.getElementById('driveStatus').textContent = status.drive_status; 
                document.getElementById('driveStatus').className = status.drive_status === 'connected' ? 'status-value connected' : 'status-value disconnected'; 
ECHO is on.
                document.getElementById('lastUpdate').textContent = new Date(status.timestamp).toLocaleString(); 
ECHO is on.
            } catch (error) { 
                console.error('Error fetching status:', error); 
            } 
        } 
ECHO is on.
        async function startBot() { 
            try { 
                const response = await fetch('/start'); 
                const result = await response.json(); 
                alert(result.message); 
                refreshStatus(); 
            } catch (error) { 
                alert('Error starting bot: ' + error.message); 
            } 
        } 
ECHO is on.
        async function stopBot() { 
            try { 
                const response = await fetch('/stop'); 
                const result = await response.json(); 
                alert(result.message); 
                refreshStatus(); 
            } catch (error) { 
                alert('Error stopping bot: ' + error.message); 
            } 
        } 
ECHO is on.
        async function getQRCode() { 
            try { 
                const response = await fetch('/qr'); 
                const result = await response.json(); 
ECHO is on.
                if (result.status === 'success') { 
                    document.getElementById('qrSection').style.display = 'block'; 
                    document.getElementById('qrCode').innerHTML = 'QR Code Data: ' + result.qr_data; 
                    document.getElementById('qrCode').style.display = 'block'; 
                } else { 
                    alert('QR code not available yet. Start the bot first.'); 
                } 
            } catch (error) { 
                alert('Error getting QR code: ' + error.message); 
            } 
        } 
ECHO is on.
        // Refresh status every 5 seconds 
        setInterval(refreshStatus, 5000); 
ECHO is on.
        // Initial load 
        refreshStatus(); 
    </script> 
</body> 
</html>''' 
 
with open('templates/index.html', 'w', encoding='utf-8') as f: 
    f.write(html_content) 
 
print("HTML template created successfully!") 
